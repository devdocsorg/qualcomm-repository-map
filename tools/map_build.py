"""Generate the full README map and export nearby README blocks.

The JSON dataset owns repository facts and the map's identity: its name, the
GitHub organisations whose repositories it records, and the map repository.
Mermaid README blocks are derived output. Map generation is independent of
Sphinx and produces no website pages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/repositories.json"
START = "<!-- repository-map:start -->"
END = "<!-- repository-map:end -->"
KINDS = {"depends on", "integrates with", "fetches source from", "uses indirectly",
         "builds with", "selects for distro", "pins release of", "configures",
         "selects branches from", "packages", "runs workflow from", "uses automation from"}
AUTOMATION = {'uses automation from', 'runs workflow from'}
MAX_MAP_NODES = 24
# GitHub organisation names: alphanumeric words joined by single hyphens.
ORGANISATION = re.compile(r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*')
LABELS = {'depends on': 'builds on', 'integrates with': 'can combine with',
          'fetches source from': 'fetches sources from', 'builds with': 'builds with',
          'selects for distro': 'includes in Linux images', 'pins release of': 'pins a release of',
          'configures': 'configures', 'selects branches from': 'selects branches from',
          'packages': 'packages sources from', 'runs workflow from': 'runs workflows from',
          'uses automation from': 'runs automation from'}


def connection_label(edge: dict) -> str:
    """Return a relationship's connection verb, naming the branches it is limited to.

    :param edge: Relationship record, with an optional ``local_summary`` and ``branches``.
    :returns: Short label such as ``builds on (scarthgap, kirkstone)``.

    Example: a ``depends on`` edge with ``branches: ['kirkstone']`` reads
    ``builds on (kirkstone)``.
    """
    label = edge.get('local_summary') or LABELS[edge['kind']]
    if edge.get('branches'):
        label += f" ({', '.join(edge['branches'])})"
    return label


def slug(identifier: str) -> str:
    """Return a filesystem-safe name for an owner/repository identifier.

    :param identifier: Repository identifier, such as ``example-org/example-layer``.
    :returns: Identifier with the slash replaced by two hyphens.
    :raises ValueError: If the identifier contains unsupported characters.

    Example: ``slug('example-org/example-layer')`` returns ``'example-org--example-layer'``.
    """
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", identifier):
        raise ValueError(f"Invalid repository identifier: {identifier}")
    return identifier.replace("/", "--")


def map_url(data: dict) -> str:
    """Return the URL of the map repository recorded in a dataset.

    :param data: Dataset with a ``map_repository`` field.
    :returns: The map repository's GitHub URL, used for central links.

    Example: ``map_url({'map_repository': 'example-org/repository-map'})`` returns
    ``'https://github.com/example-org/repository-map'``.
    """
    return f"https://github.com/{data['map_repository']}"


def validate_header(data: dict) -> None:
    """Check the dataset's identity, scope, and inventory fields.

    :param data: Parsed dataset.
    :raises ValueError: For a missing name, an invalid organisation list or map
        repository, or inventory fields that do not cover the organisations.

    ``inventory_source`` and ``inventory_observed`` are either one string each,
    for a map inventoried from a single listing, or objects with one entry per
    organisation.
    """
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported dataset schema version")
    for field in ("name", "scope", "coverage"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"Missing dataset {field}")
    organisations = data.get("organisations")
    if (not isinstance(organisations, list) or not organisations
            or len(set(organisations)) != len(organisations)
            or not all(isinstance(o, str) and ORGANISATION.fullmatch(o) for o in organisations)):
        raise ValueError("organisations must be a non-empty list of unique GitHub organisation names")
    if not isinstance(data.get("map_repository"), str):
        raise ValueError("Missing map_repository")
    slug(data["map_repository"])
    for field in ("inventory_source", "inventory_observed"):
        value = data.get(field)
        values = list(value.values()) if isinstance(value, dict) else [value]
        if isinstance(value, dict) and set(value) != set(organisations):
            raise ValueError(f"{field} needs exactly one entry per organisation")
        if not all(isinstance(v, str) and v for v in values):
            raise ValueError(f"Missing {field}")
        if field == "inventory_observed" and not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) for v in values):
            raise ValueError("inventory_observed dates use the YYYY-MM-DD form")
    for field in ("repositories", "relationships", "source_audits"):
        if not isinstance(data.get(field), list):
            raise ValueError(f"{field} must be a list")


def validate_source_audits(data: dict) -> None:
    """Check that every source audit names a mapped repository and pinned paths.

    :param data: Dataset whose repositories have been validated.
    :raises ValueError: For an unmapped repository, an invalid source repository,
        an unpinned revision, or a missing or empty path list.
    """
    ids = {node["id"] for node in data["repositories"]}
    for audit in data["source_audits"]:
        if not isinstance(audit, dict) or audit.get("repository") not in ids:
            raise ValueError(f"Source audit for an unmapped repository: {audit}")
        slug(audit.get("source_repository") or "")
        if not re.fullmatch(r"[0-9a-f]{40}", str(audit.get("revision"))):
            raise ValueError(f"Source audit must pin a commit: {audit['repository']}")
        paths = audit.get("paths")
        if not isinstance(paths, list) or not paths or not all(isinstance(p, str) and p for p in paths):
            raise ValueError(f"Source audit needs a non-empty list of paths: {audit['repository']}")


def load_data(path: Path) -> dict:
    """Read and validate a dataset before producing any output.

    :param path: JSON dataset path.
    :returns: Parsed dataset with valid unique repositories and evidenced edges.
    :raises ValueError: For an invalid header, IDs outside the dataset's
        organisations, duplicate edges, missing evidence, or malformed audits.
    :raises OSError: If the dataset cannot be read.

    Example: ``load_data(DATA)['schema_version']`` returns ``1``.
    """
    data = json.loads(path.read_text())
    validate_header(data)
    organisations = set(data["organisations"])
    ids, default_branch = set(), {}
    for node in data["repositories"]:
        slug(node["id"])
        if node["id"] in ids or not node["url"].startswith("https://"):
            raise ValueError(f"Duplicate repository or invalid URL: {node['id']}")
        if node["id"].split("/")[0] not in organisations:
            raise ValueError(f"Only repositories owned by the map's organisations belong in the map: {node['id']}")
        if not node["description"] or not node["group"]:
            raise ValueError(f"Missing repository description/group: {node['id']}")
        ids.add(node["id"])
        default_branch[node["id"]] = node.get("branch")
    seen = set()
    for edge in data["relationships"]:
        key = (edge["from"], edge["to"], edge["kind"], edge["condition"])
        if edge["from"] not in ids or edge["to"] not in ids or edge["from"] == edge["to"]:
            raise ValueError(f"Unknown repository or self-edge: {key}")
        if key in seen or edge["kind"] not in KINDS or not edge["condition"]:
            raise ValueError(f"Duplicate or invalid relationship: {key}")
        branches = edge.get("branches")
        if branches is not None and (not isinstance(branches, list) or not branches
                                     or not all(isinstance(b, str) and b for b in branches)):
            raise ValueError(f"Relationship branches must be a non-empty list of names: {key}")
        if branches and default_branch.get(edge["from"]) in branches:
            raise ValueError(f"A relationship on the default branch takes no branches label: {key}")
        if not edge["evidence"]:
            raise ValueError(f"Missing relationship evidence: {key}")
        for proof in edge["evidence"]:
            if not re.fullmatch(r"[0-9a-f]{40}", proof["revision"]):
                raise ValueError(f"Evidence must pin a commit: {key}")
            if not proof["url"].startswith("https://github.com/") or f"/blob/{proof['revision']}/" not in proof["url"] or not proof["claim"]:
                raise ValueError(f"Invalid evidence URL or claim: {key}")
        seen.add(key)
    relationship_paths(data)
    validate_source_audits(data)
    return data


def relationship_paths(data: dict, focus: str | None = None) -> list[tuple[dict, list[dict]]]:
    """Resolve recorded connections into verified paths through their intermediates.

    :param data: Validated shared dataset.
    :param focus: Restrict to incident build/component connections when supplied.
    :returns: Original relationships paired with their directly evidenced steps.
    :raises ValueError: If an indirect relationship has no valid recorded path.

    A focus -> provider -> tool path replaces a misleading direct indirect-use arrow.
    """
    result = []
    for edge in data['relationships']:
        if focus is not None and (focus not in (edge['from'], edge['to']) or edge['kind'] in AUTOMATION):
            continue
        if edge['kind'] != 'uses indirectly':
            result.append((edge, [edge]))
            continue
        via = edge.get('via')
        if not isinstance(via, list) or not via:
            raise ValueError(f"Indirect connection needs a recorded via path: {edge['from']} -> {edge['to']}")
        route = [edge['from'], *via, edge['to']]
        if len(set(route)) != len(route):
            raise ValueError('Indirect path contains a cycle')
        steps = []
        for source, target in zip(route, route[1:]):
            candidates = [e for e in data['relationships'] if e['from'] == source and e['to'] == target
                          and e['kind'] not in AUTOMATION | {'uses indirectly'}]
            if not candidates:
                raise ValueError(f'Missing recorded path step: {source} -> {target}')
            steps.append(sorted(candidates, key=lambda e: (e['kind'] != 'depends on', e['kind']))[0])
        result.append((edge, steps))
    return result


def diagram(nodes: list[dict], edges: list[dict], focus: str | None = None) -> str:
    """Render linked Mermaid nodes and directed, labelled relationships.

    :param nodes: Repositories to show, each with a canonical URL.
    :param edges: Reviewed relationships between the selected nodes.
    :param focus: Current repository to highlight, or None for the full map.
    :returns: A fenced Mermaid flowchart with a clickable link on every node.
    """
    identifiers = {node['id']: f'r{i}' for i, node in enumerate(nodes)}
    lines = ['```mermaid', 'flowchart LR']
    for node in nodes:
        short = node['id'].split('/')[-1]
        label = short if sum(n['id'].split('/')[-1] == short for n in nodes) == 1 else node['id']
        if node['id'] == focus:
            label += ' (you are here)'
        lines.append(f'    {identifiers[node["id"]]}["{label}"]')
        lines.append(f'    click {identifiers[node["id"]]} href "{node["url"]}" _blank')
    seen = set()
    for edge in edges:
        label = connection_label(edge)
        # Entity escapes keep authored labels from becoming Mermaid syntax.
        label = label.replace('&', '#38;').replace('"', '#34;').replace('|', '#124;').replace('\n', ' ')
        key = (edge['from'], edge['to'], label)
        if key not in seen:
            lines.append(f'    {identifiers[edge["from"]]} -->|"{label}"| {identifiers[edge["to"]]}')
            seen.add(key)
    if focus:
        lines.append(f'    style {identifiers[focus]} fill:#e6f3ff,stroke:#0969da,stroke-width:3px,color:#182c43')
    return '\n'.join(lines + ['```', ''])


def validate_local_view(data: dict, focus: str, markdown: str) -> None:
    """Reject omitted component connections, broken indirect paths, or invented arrows.

    :param data: The authoritative relationship dataset.
    :param focus: Repository whose complete component neighbourhood is checked.
    :param markdown: Generated or edited README map block.
    :raises ValueError: If a node, connection, label, or indirect step is missing.
    """
    urls = {node['id']: node['url'] for node in data['repositories']}
    arrows, shown = set(), set()
    for graph in re.findall(r'```mermaid\n(.*?)\n```', markdown, re.S):
        links = dict(re.findall(r'click (r\d+) href "([^"]+)"', graph))
        identifiers = set(re.findall(r'^    (r\d+)\[', graph, re.M))
        if identifiers != set(links):
            raise ValueError('Every repository node must have a link')
        shown.update(links.values())
        for source, label, target in re.findall(r'^    (r\d+) -->\|"([^"]+)"\| (r\d+)$', graph, re.M):
            arrows.add((links[source], label, links[target]))
    allowed = set()
    for edge in data['relationships']:
        if edge['kind'] in AUTOMATION | {'uses indirectly'}:
            continue
        label = connection_label(edge)
        label = label.replace('&', '#38;').replace('"', '#34;').replace('|', '#124;').replace('\n', ' ')
        allowed.add((urls[edge['from']], label, urls[edge['to']]))
        if focus in (edge['from'], edge['to']) and (urls[edge['from']], label, urls[edge['to']]) not in arrows:
            raise ValueError(f"Missing component connection: {edge['from']} -> {edge['to']}")
    if urls[focus] not in shown or not arrows <= allowed:
        raise ValueError('Missing current repository or unrecorded map connection')
    for edge in data['relationships']:
        if edge['kind'] != 'uses indirectly' or focus not in (edge['from'], edge['to']):
            continue
        route = [edge['from'], *edge['via'], edge['to']]
        for source, target in zip(route, route[1:]):
            if not any(a == urls[source] and b == urls[target] for a, _, b in arrows):
                raise ValueError(f'Missing indirect path step: {source} -> {target}')


def render_local_view(data: dict, focus: str, digest: str, revision: str) -> str:
    """Export every incident build/component connection with its verified path.

    :param data: Validated dataset.
    :param focus: Repository whose nearby map is exported.
    :param digest: SHA-256 of the dataset file, recorded in the provenance comment.
    :param revision: Map repository commit the export is generated from.
    :returns: Nearby map Markdown, linking the full map and recording its source.
    :raises KeyError: If the focus repository is not in the dataset.
    """
    nodes = {node['id']: node for node in data['repositories']}
    if focus not in nodes:
        raise KeyError(focus)
    paths = relationship_paths(data, focus)
    parts, edges, selected = [], [], {focus}
    for _, path in paths:
        identifiers = {e[end] for e in path for end in ('from', 'to')} | {focus}
        if len(identifiers) > MAX_MAP_NODES:
            raise ValueError('A recorded path exceeds the map size limit; revise its presentation')
        if edges and len(selected | identifiers) > MAX_MAP_NODES:
            parts.append((selected, edges))
            edges, selected = [], {focus}
        edges.extend(path)
        selected.update(identifiers)
    parts.append((selected, edges))
    result = '## Repository map\n\n'
    for index, (identifiers, connections) in enumerate(parts, 1):
        if len(parts) > 1:
            result += ('\n' if index > 1 else '') + f'### Connections ({index}/{len(parts)})\n\n'
        selected_nodes = [nodes[focus], *(nodes[key] for key in sorted(identifiers - {focus}))]
        result += diagram(selected_nodes, connections, focus)
    if not paths:
        result += '\nBuild/component connections have not been reviewed for this repository.\n'
    result += f"\n[Full {data['name']} repository map]({map_url(data)}).\n"
    result += f'\n<!-- Generated from {map_url(data)} at {revision}; dataset SHA-256: {digest}. -->\n'
    validate_local_view(data, focus, result)
    return result


def update_readme(readme: Path, block: str, check: bool = False) -> None:
    """Replace only the final marked README block; fail on ambiguous boundaries.

    :param readme: Existing root README to update.
    :param block: Generated nearby map Markdown.
    :param check: Compare without writing, raising ValueError if stale.
    :raises ValueError: For malformed markers, non-final maps, or stale output.
    """
    original = readme.read_text()
    if START not in original and END not in original:
        before = original.rstrip() + '\n\n'
    else:
        if original.count(START) != 1 or original.count(END) != 1:
            raise ValueError('README must contain exactly one map marker pair')
        before, rest = original.split(START)
        if END not in rest:
            raise ValueError('Map end marker must follow start marker')
        _, after = rest.split(END)
        if after.strip():
            raise ValueError('Repository map must be at the bottom of the README')
    updated = before + START + '\n\n' + block.rstrip() + '\n\n' + END + '\n'
    if check:
        if updated != original:
            raise ValueError('README map differs from the recorded dataset and generator')
    else:
        readme.write_text(updated)


def cluster_maps(data: dict) -> list[tuple[str, list[dict], list[dict]]]:
    """Separate relationships by purpose and keep each diagram small.

    :param data: Validated repository and relationship dataset.
    :returns: Named maps, each containing its repository nodes and relationships.

    Kernel automation stays with kernel integration. Standalone automation groups
    are omitted. Large component groups split at source boundaries where possible.
    """
    nodes = {node['id']: node for node in data['repositories']}
    titles = ['Yocto builds and releases', 'Kernel integration', 'Source packaging',
              'Layer automation', 'Build and validation automation',
              'Package automation', 'Other automation']
    groups = {title: [] for title in titles}
    connections = {(e['from'], e['to'], e['kind']): e
                   for _, path in relationship_paths(data) for e in path}
    for edge in connections.values():
        area = nodes[edge['from']]['group']
        if area == 'Kernel integration':
            title = 'Kernel integration'
        elif edge['kind'] in AUTOMATION:
            title = {'Layers and releases': 'Layer automation',
                     'Packaging': 'Package automation',
                     'Images and build tooling': 'Build and validation automation',
                     'Boot and firmware': 'Build and validation automation',
                     'Validation': 'Build and validation automation',
                     'Other repositories': 'Other automation'}.get(area, area + ' automation')
        else:
            title = {'Layers and releases': 'Yocto builds and releases',
                     'Packaging': 'Source packaging'}.get(area, area + ' relationships')
        groups.setdefault(title, []).append(edge)

    maps = []
    for title, edges in groups.items():
        # Omit standalone automation diagrams, preserving mixed component maps.
        if not edges or all(edge['kind'] in AUTOMATION for edge in edges):
            continue
        parts, current, selected = [], [], set()
        for source in sorted({edge['from'] for edge in edges}):
            outgoing = sorted((edge for edge in edges if edge['from'] == source),
                              key=lambda edge: (edge['to'], edge['kind'], edge['condition']))
            endpoints = {source, *(edge['to'] for edge in outgoing)}
            if current and len(selected | endpoints) > MAX_MAP_NODES:
                parts.append(current)
                current, selected = [], set()
            for edge in outgoing:
                endpoints = {edge['from'], edge['to']}
                if len(selected | endpoints) > MAX_MAP_NODES:
                    parts.append(current)
                    current, selected = [], set()
                current.append(edge)
                selected.update(endpoints)
        if current:
            parts.append(current)
        for i, part in enumerate(parts, 1):
            label = f'{title} ({i}/{len(parts)})' if len(parts) > 1 else title
            identifiers = {edge[end] for edge in part for end in ('from', 'to')}
            maps.append((label, [nodes[key] for key in sorted(identifiers)], part))
    return maps


def render_overview(data: dict, digest: str) -> str:
    """Render the full README map: component maps, inventory, and evidence.

    :param data: Validated dataset; its ``name`` titles the map.
    :param digest: SHA-256 of the dataset file, recorded in a source comment.
    :returns: The README Markdown.

    Indirect records follow existing paths. Standalone automation diagrams and
    their relationship text are omitted; mixed component diagrams retain context.
    An empty dataset renders a README that says nothing is recorded yet.
    """
    nodes = sorted(data['repositories'], key=lambda node: node['id'])
    maps = cluster_maps(data)
    displayed = {(e['from'], e['to'], e['kind']) for _, _, edges in maps for e in edges}
    edges = sorted((edge for edge in data['relationships'] if edge['kind'] not in AUTOMATION
                    or (edge['from'], edge['to'], edge['kind']) in displayed),
                   key=lambda edge: (edge['from'], edge['to'], edge['kind']))
    components = sum(edge['kind'] not in AUTOMATION for edge in edges)
    overview = f"# {data['name']} repository map\n\n" + data['scope'] + '\n\n'
    overview += f"**Coverage:** {len(nodes)} repositories; {components} recorded build/component relationships.\n\n{data['coverage']}\n\n"
    if not data['relationships']:
        overview += 'No relationships are recorded yet.\n'
    elif not maps:
        overview += 'No build/component relationships are recorded yet.\n'
    else:
        overview += 'Click a repository node to open it. Indirect connections follow the actual path through their provider.\n\n'
    for title, _, _ in maps:
        anchor = re.sub(r'[^a-z0-9 -]', '', title.lower()).replace(' ', '-')
        overview += f'- [{title}](#{anchor})\n'
    for title, selected, connections in maps:
        overview += f'\n## {title}\n\n' + diagram(selected, connections)
    overview += '\n## Reference details\n'
    if not nodes:
        overview += '\nNo repositories are inventoried yet.\n'
    else:
        overview += '\n<details>\n<summary>Repository inventory</summary>\n\n'
        for group in sorted({node['group'] for node in nodes}):
            overview += f'### {group}\n\n'
            for node in nodes:
                if node['group'] == group:
                    status = '; archived' if node['archived'] else ''
                    branch = node['branch'] or 'not inventoried'
                    description = re.sub(r'https?://[^\s)]+', r'<\g<0>>', node['description'])
                    overview += f"- [{node['id']}]({node['url']}) — {description} (default branch: `{branch}`{status}).\n"
            overview += '\n'
        overview += '</details>\n'
    if edges:
        overview += '\n<details>\n<summary>Relationship applicability and sources</summary>\n\n'
        for focus in sorted({edge['from'] for edge in edges}):
            overview += f'### {focus}\n\n'
            for edge in edges:
                if edge['from'] != focus:
                    continue
                target = next(node for node in nodes if node['id'] == edge['to'])
                if edge['kind'] == 'uses indirectly':
                    relation = 'through ' + ' → '.join(f"[{identifier.split('/')[-1]}]({next(n['url'] for n in nodes if n['id'] == identifier)})" for identifier in edge['via'])
                else:
                    relation = connection_label(edge)
                overview += f"- **{relation}** [{edge['to'].split('/')[-1]}]({target['url']})\n  - {edge['condition']}\n"
                for proof in edge['evidence']:
                    filename = Path(unquote(urlsplit(proof['url']).path)).name
                    overview += f"  - [{filename}]({proof['url']})\n"
            overview += '\n'
        overview += '</details>\n'
    overview += '\n[Map data and updates](data/README.md).\n'
    overview += f'\n<!-- Dataset SHA-256: {digest}. -->\n'
    return overview


def build(data: dict, digest: str, readme: Path = ROOT / 'README.md') -> None:
    """Write the full README map generated from a validated dataset.

    :param data: Validated dataset.
    :param digest: SHA-256 of the dataset file.
    :param readme: README path to write, the map repository's root README by default.
    """
    readme.write_text(render_overview(data, digest))


def main() -> None:
    """Build the full map or update/check a recipient README at a pinned revision."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', help='Exact repository identifier to export')
    parser.add_argument('--readme', type=Path, help='Existing recipient root README')
    parser.add_argument('--revision', help='Central map commit identifying the export source')
    parser.add_argument('--check', action='store_true', help='Verify the README block without writing')
    args = parser.parse_args()
    data = load_data(DATA)
    digest = hashlib.sha256(DATA.read_bytes()).hexdigest()
    if args.export:
        if args.readme is None or not args.revision or not re.fullmatch('[0-9a-f]{40}', args.revision):
            parser.error('Export requires --readme and --revision with a full commit SHA')
        subprocess.run(['git', 'cat-file', '-e', args.revision + '^{commit}'], cwd=ROOT, check=True)
        subprocess.run(['git', 'diff', '--exit-code', args.revision, '--', 'data', 'tools'], cwd=ROOT, check=True)
        update_readme(args.readme, render_local_view(data, args.export, digest, args.revision), args.check)
        print(f'{"Verified" if args.check else "Updated"} README map for {args.export}')
    else:
        if args.check or args.readme or args.revision:
            parser.error('--check, --readme, and --revision require --export')
        build(data, digest)
        print(f"Generated full README map: {len(data['repositories'])} repositories")


if __name__ == '__main__':
    main()
