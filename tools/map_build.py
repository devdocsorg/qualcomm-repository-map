"""Generate the full Qualcomm README map and export nearby README blocks.

The JSON dataset owns repository facts. Mermaid README blocks are derived output.
Map generation is independent of Sphinx and produces no website pages.
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
CENTRAL = "https://github.com/devdocsorg/qualcomm-repository-map"
START = "<!-- repository-map:start -->"
END = "<!-- repository-map:end -->"
KINDS = {"depends on", "integrates with", "fetches source from", "uses indirectly",
         "builds with", "selects for distro", "pins release of", "configures",
         "selects branches from", "packages", "runs workflow from", "uses automation from"}
AUTOMATION = {'uses automation from', 'runs workflow from'}
MAX_MAP_NODES = 24
LABELS = {'depends on': 'builds on', 'integrates with': 'can combine with',
          'fetches source from': 'fetches sources from', 'builds with': 'builds with',
          'selects for distro': 'includes in Linux images', 'pins release of': 'pins a release of',
          'configures': 'configures', 'selects branches from': 'selects branches from',
          'packages': 'packages sources from', 'runs workflow from': 'runs workflows from',
          'uses automation from': 'runs automation from'}


def slug(identifier: str) -> str:
    """Return a filesystem-safe name for an owner/repository identifier.

    :param identifier: Repository identifier, such as ``qualcomm-linux/meta-qcom``.
    :returns: Identifier with the slash replaced by two hyphens.
    :raises ValueError: If the identifier contains unsupported characters.

    Example: ``slug('qualcomm-linux/meta-qcom')`` returns ``'qualcomm-linux--meta-qcom'``.
    """
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", identifier):
        raise ValueError(f"Invalid repository identifier: {identifier}")
    return identifier.replace("/", "--")


def load_data(path: Path) -> dict:
    """Read and validate a dataset before producing any output.

    :param path: JSON dataset path.
    :returns: Parsed dataset with valid unique repositories and evidenced edges.
    :raises ValueError: For invalid IDs, duplicate edges, or missing evidence.
    :raises OSError: If the dataset cannot be read.

    Example: ``load_data(DATA)['schema_version']`` returns ``1``.
    """
    data = json.loads(path.read_text())
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported dataset schema version")
    ids = set()
    for node in data["repositories"]:
        slug(node["id"])
        if node["id"] in ids or not node["url"].startswith("https://"):
            raise ValueError(f"Duplicate repository or invalid URL: {node['id']}")
        if not node["description"] or not node["group"]:
            raise ValueError(f"Missing repository description/group: {node['id']}")
        ids.add(node["id"])
    seen = set()
    for edge in data["relationships"]:
        key = (edge["from"], edge["to"], edge["kind"], edge["condition"])
        if edge["from"] not in ids or edge["to"] not in ids or edge["from"] == edge["to"]:
            raise ValueError(f"Unknown repository or self-edge: {key}")
        if key in seen or edge["kind"] not in KINDS or not edge["condition"]:
            raise ValueError(f"Duplicate or invalid relationship: {key}")
        if not edge["evidence"]:
            raise ValueError(f"Missing relationship evidence: {key}")
        for proof in edge["evidence"]:
            if not re.fullmatch(r"[0-9a-f]{40}", proof["revision"]):
                raise ValueError(f"Evidence must pin a commit: {key}")
            if not proof["url"].startswith("https://github.com/") or f"/blob/{proof['revision']}/" not in proof["url"] or not proof["claim"]:
                raise ValueError(f"Invalid evidence URL or claim: {key}")
        seen.add(key)
    relationship_paths(data)
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
        label = edge.get('local_summary') or LABELS[edge['kind']]
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
        label = edge.get('local_summary') or LABELS[edge['kind']]
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
    """Export every incident build/component connection with its verified path."""
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
            result += f'### Connections ({index}/{len(parts)})\n\n'
        selected_nodes = [nodes[focus], *(nodes[key] for key in sorted(identifiers - {focus}))]
        result += diagram(selected_nodes, connections, focus)
    if not paths:
        result += '\nBuild/component connections have not been reviewed for this repository.\n'
    result += f'\n[Full Qualcomm repository map]({CENTRAL}).\n'
    result += f'\n<!-- Generated from {CENTRAL} at {revision}; dataset SHA-256: {digest}. -->\n'
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


def build(data: dict, digest: str) -> None:
    """Generate component maps and their evidence, retaining the complete inventory.

    Indirect records follow existing paths. Standalone automation diagrams and
    their relationship text are omitted; mixed component diagrams retain context.
    """
    nodes = sorted(data['repositories'], key=lambda node: node['id'])
    maps = cluster_maps(data)
    displayed = {(e['from'], e['to'], e['kind']) for _, _, edges in maps for e in edges}
    edges = sorted((edge for edge in data['relationships'] if edge['kind'] not in AUTOMATION
                    or (edge['from'], edge['to'], edge['kind']) in displayed),
                   key=lambda edge: (edge['from'], edge['to'], edge['kind']))
    components = sum(edge['kind'] not in AUTOMATION for edge in edges)
    overview = '# Qualcomm repository map\n\n' + data['scope'] + '\n\n'
    overview += f"**Coverage:** {len(nodes)} repositories; {components} recorded build/component relationships.\n\n{data['coverage']}\n\n"
    overview += 'Click a repository node to open it. Indirect connections follow the actual path through their provider.\n\n'
    for title, _, _ in maps:
        anchor = re.sub(r'[^a-z0-9 -]', '', title.lower()).replace(' ', '-')
        overview += f'- [{title}](#{anchor})\n'
    for title, selected, connections in maps:
        overview += f'\n## {title}\n\n' + diagram(selected, connections)
    overview += '\n## Reference details\n'
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
    overview += '</details>\n\n<details>\n<summary>Relationship applicability and sources</summary>\n\n'
    for focus in sorted({edge['from'] for edge in edges}):
        overview += f'### {focus}\n\n'
        for edge in edges:
            if edge['from'] != focus:
                continue
            target = next(node for node in nodes if node['id'] == edge['to'])
            if edge['kind'] == 'uses indirectly':
                relation = 'through ' + ' → '.join(f"[{identifier.split('/')[-1]}]({next(n['url'] for n in nodes if n['id'] == identifier)})" for identifier in edge['via'])
            else:
                relation = edge.get('local_summary') or LABELS[edge['kind']]
            overview += f"- **{relation}** [{edge['to'].split('/')[-1]}]({target['url']})\n  - {edge['condition']}\n"
            for proof in edge['evidence']:
                filename = Path(unquote(urlsplit(proof['url']).path)).name
                overview += f"  - [{filename}]({proof['url']})\n"
        overview += '\n'
    overview += '</details>\n\n[Map data and updates](data/README.md).\n'
    overview += f'\n<!-- Dataset SHA-256: {digest}. -->\n'
    (ROOT/'README.md').write_text(overview)


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
