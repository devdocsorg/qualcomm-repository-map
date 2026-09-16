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

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/repositories.json"
CENTRAL = "https://github.com/devdocsorg/qualcomm-repository-map"
START = "<!-- repository-map:start -->"
END = "<!-- repository-map:end -->"
KINDS = {"depends on", "integrates with", "fetches source from", "uses indirectly",
         "builds with", "selects for distro", "pins release of", "configures",
         "selects branches from", "packages", "runs workflow from", "uses automation from"}


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
    return data


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
        label = edge['local_summary'] if focus else edge['kind']
        # Entity escapes keep authored labels from becoming Mermaid syntax.
        label = label.replace('&', '#38;').replace('"', '#34;').replace('|', '#124;').replace('\n', ' ')
        key = (edge['from'], edge['to'], label)
        if key not in seen:
            lines.append(f'    {identifiers[edge["from"]]} -->|"{label}"| {identifiers[edge["to"]]}')
            seen.add(key)
    if focus:
        lines.append(f'    style {identifiers[focus]} fill:#e6f3ff,stroke:#0969da,stroke-width:3px,color:#182c43')
    return '\n'.join(lines + ['```', ''])


def render_local_view(data: dict, focus: str, digest: str, revision: str) -> str:
    """Export only direct user-relevant dependencies in a nearby Mermaid block.

    Each included relationship needs a concise local_summary. Transitive
    dependencies, CI automation, and incoming users stay in the full map.
    """
    nodes = {node['id']: node for node in data['repositories']}
    if focus not in nodes:
        raise KeyError(focus)
    order = {'depends on': 0, 'integrates with': 1, 'fetches source from': 2}
    edges = [edge for edge in data['relationships'] if edge['from'] == focus
             and edge['kind'] not in {'uses indirectly', 'uses automation from', 'runs workflow from'}]
    edges.sort(key=lambda edge: (order.get(edge['kind'], 4), edge['to']))
    for edge in edges:
        if not isinstance(edge.get('local_summary'), str) or not edge['local_summary'].strip():
            raise ValueError(f"Add a concise local_summary for {edge['from']} -> {edge['to']}")
    selected = [nodes[identifier] for identifier in dict.fromkeys([focus, *(e['to'] for e in edges)])]
    result = '## Repository map\n\n' + diagram(selected, edges, focus)
    if not edges:
        result += '\nBuild dependencies have not been reviewed for this repository.\n'
    result += f'\n[Full Qualcomm repository map]({CENTRAL}).\n'
    result += f'\n<!-- Generated from {CENTRAL} at {revision}; dataset SHA-256: {digest}. -->\n'
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


def build(data: dict, digest: str) -> None:
    """Generate the full README map, with all inventory and evidence retained.

    The diagram shows every repository and distinct directed relationship.
    Expandable details preserve conditions, source claims, and inventory metadata.
    """
    nodes = sorted(data['repositories'], key=lambda node: node['id'])
    edges = sorted(data['relationships'], key=lambda edge: (edge['from'], edge['to'], edge['kind']))
    connected = {edge[end] for edge in edges for end in ('from', 'to')}
    overview = '# Qualcomm repository map\n\n' + data['scope'] + '\n\n'
    overview += f"**Coverage:** {len(nodes)} repositories, {len(connected)} with reviewed connections, {len(edges)} evidenced relationships.\n\n{data['coverage']}\n\n"
    overview += 'Click a repository node to open it. Arrows describe how repositories relate.\n\n'
    overview += diagram(nodes, edges)
    overview += '\n<details>\n<summary>Repository inventory</summary>\n\n'
    for group in sorted({node['group'] for node in nodes}):
        overview += f'## {group}\n\n'
        for node in nodes:
            if node['group'] == group:
                status = '; archived' if node['archived'] else ''
                branch = node['branch'] or 'not inventoried'
                description = re.sub(r'https?://[^\s)]+', r'<\g<0>>', node['description'])
                overview += f"- [{node['id']}]({node['url']}) — {description} (default branch: `{branch}`{status}).\n"
        overview += '\n'
    overview += '</details>\n\n<details>\n<summary>Relationship applicability and sources</summary>\n\n'
    for focus in sorted({edge['from'] for edge in edges}):
        overview += f'## {focus}\n\n'
        for edge in edges:
            if edge['from'] != focus:
                continue
            overview += f"- **{edge['kind']}** [{edge['to'].split('/')[-1]}](https://github.com/{edge['to']})\n  - {edge['condition']}\n"
            for proof in edge['evidence']:
                overview += f"  - [{proof['claim']}]({proof['url']})\n"
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
