"""Generate the Qualcomm ecosystem overview and nearby repository views.

The JSON dataset owns repository facts. Linked Markdown, HTML, and exported nearby views
are derived outputs. The generator runs without network access.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from markdown_it import MarkdownIt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/repositories.json"
OUTPUT = ROOT / "maps"
CENTRAL = "https://github.com/devdocsorg/qualcomm-repository-map"
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


def nearby(data: dict, focus: str) -> tuple[list[dict], list[dict]]:
    """Select the focus repository and all recorded incoming/outgoing neighbours.

    :param data: Validated dataset.
    :param focus: Exact owner/repository identifier.
    :returns: Selected repositories and incident relationships, in stable order.
    :raises KeyError: If the focus repository is absent.

    Example: ``nearby(load_data(DATA), 'qualcomm-linux/meta-qcom-3rdparty')`` selects its local view.
    """
    nodes = {node["id"]: node for node in data["repositories"]}
    if focus not in nodes:
        raise KeyError(focus)
    edges = [e for e in data["relationships"] if focus in (e["from"], e["to"])]
    selected = {focus}
    for edge in edges:
        selected.update((edge["from"], edge["to"]))
    return [nodes[key] for key in sorted(selected)], sorted(edges, key=str)



def repo_link(node: dict, short: bool = False) -> str:
    """Link a canonical repository, optionally omitting its owner from the label."""
    label = node['id'].split('/')[-1] if short else node['id']
    return f"[{label}]({node['url']})"


def connections(data: dict, focus: str, explore_prefix: str) -> str:
    """Group neighbours by direction and role, with evidence available on demand."""
    selected_nodes, edges = nearby(data, focus)
    nodes = {node['id']: node for node in selected_nodes}
    if not edges:
        return 'Connections have not been reviewed for this repository.\n'
    result, details = '', ''
    for direction, title in (('from', 'Uses'), ('to', 'Used by')):
        selected = [edge for edge in edges if edge[direction] == focus]
        if not selected:
            continue
        result += f'## {title}\n\n'
        for kind in sorted({edge['kind'] for edge in selected}):
            result += f'### {kind.capitalize()}\n\n'
            for edge in selected:
                if edge['kind'] != kind:
                    continue
                other = edge['to' if direction == 'from' else 'from']
                node = nodes[other]
                short = sum(n['id'].split('/')[-1] == other.split('/')[-1] for n in selected_nodes) == 1
                link = repo_link(node, short=short)
                result += f'- {link} · [Explore]({explore_prefix}{slug(other)}.md)\n'
                urls = dict.fromkeys(proof['url'] for proof in edge['evidence'])
                proofs = ' · '.join(f'[source {i+1}]({url})' for i, url in enumerate(urls))
                details += f'- {title}: {link} — **{kind}**\n  - {edge["condition"]}\n  - {proofs}\n'
            result += '\n'
    result += '<details>\n<summary>Applicability and sources</summary>\n\n' + details + '\n</details>\n'
    return result


def render_view(data: dict, focus: str, digest: str, revision: str | None = None) -> str:
    """Render the current repository once, its neighbours, and expandable evidence."""
    node = next(node for node in data['repositories'] if node['id'] == focus)
    prefix = f'{CENTRAL}/blob/{revision}/maps/' if revision else ''
    result = f'# {repo_link(node, short=True)}\n\n' + node['description'] + '\n\n'
    result += connections(data, focus, prefix)
    overview = CENTRAL if revision else '../README.md'
    result += f'\n[Back to the ecosystem map]({overview}).\n'
    result += f'\n<!-- Dataset SHA-256: {digest}; revision: {revision or "this checkout"}. -->\n'
    return result



def render_local_view(data: dict, focus: str, digest: str, revision: str) -> str:
    """Export a short dependency table; keep full evidence in the central map.

    Each included relationship needs a local_summary in the shared dataset.
    CI automation and incoming users remain available through the details link.
    """
    nodes = {node['id']: node for node in data['repositories']}
    order = {'depends on': 0, 'integrates with': 1, 'fetches source from': 2,
             'uses indirectly': 3}
    edges = [edge for edge in data['relationships'] if edge['from'] == focus
             and edge['kind'] not in {'uses automation from', 'runs workflow from'}]
    edges.sort(key=lambda edge: (order.get(edge['kind'], 4), edge['to']))
    result = f"# Repository map\n\nYou are here: **[{focus.split('/')[-1]}]({nodes[focus]['url']})**.\n\n"
    if edges:
        result += '| Repository | Used for |\n| --- | --- |\n'
    else:
        result += 'Build dependencies have not been reviewed for this repository.\n'
    for edge in edges:
        summary = edge.get('local_summary')
        if not isinstance(summary, str) or not summary.strip():
            raise ValueError(f"Add a concise local_summary for {edge['from']} -> {edge['to']}")
        node = nodes[edge['to']]
        label = node['id'].split('/')[-1]
        if sum(other['to'].split('/')[-1] == label for other in edges) > 1:
            label = node['id']
        summary = summary.replace('|', '\\|').replace('\n', ' ')
        result += f"| [{label}]({node['url']}) | {summary} |\n"
    result += f'\n[Full map and relationship details]({CENTRAL}/blob/{revision}/maps/{slug(focus)}.md) (private).\n'
    result += f'\n<!-- Generated from {CENTRAL} at {revision}; dataset SHA-256: {digest}. -->\n'
    return result


def html_page(markdown: str, title: str) -> str:
    """Render the same linked map as standalone HTML for direct file browsing."""
    body = MarkdownIt('commonmark').render(markdown)
    body = re.sub(r'href="(?!https?://)([^"#]+)\.md"',
                  lambda match: 'href="' + ('../index' if match[1] == '../README' else match[1]) + '.html"', body)
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title><style>'
            'body{font:17px/1.6 system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1.5rem;color:#182c43;background:#fff}'
            'a{color:#0752a0;text-underline-offset:.18em}a:hover{color:#733cab}a:focus-visible{outline:3px solid #b87b00}'
            'h1{font-size:1.8rem;overflow-wrap:anywhere}h2{margin-top:2.5rem;border-bottom:1px solid #cbd5e1}'
            'li{margin:.5rem 0}li li{font-size:.9rem;color:#43546a}code{overflow-wrap:anywhere}'
            '</style></head><body><main>' + body + '</main></body></html>\n')


def build(data: dict, digest: str) -> None:
    """Generate the root map and linked nearby pages from the sole dataset."""
    OUTPUT.mkdir(exist_ok=True)
    for old in OUTPUT.iterdir():
        if old.suffix in {'.md', '.html'}:
            old.unlink()
    nodes = sorted(data['repositories'], key=lambda node: node['id'])
    connected = {edge[end] for edge in data['relationships'] for end in ('from', 'to')}
    overview = '# Qualcomm repository map\n\n' + data['scope'] + '\n\n'
    overview += f"**Coverage:** {len(nodes)} repositories, {len(connected)} with reviewed connections, {len(data['relationships'])} evidenced relationships.\n\n{data['coverage']}\n\n"
    overview += 'Repository names open the repository. **Explore** links move through its neighbourhood. Open `index.html` for local browsing without a server; external repository and evidence links need network access.\n\n'
    overview += '## Connected repositories\n\n'
    for focus in ('qualcomm-linux/meta-qcom', 'qualcomm-linux/meta-qcom-3rdparty', 'qualcomm-linux/kernel-config', 'qualcomm-linux/pkg-kgsl'):
        overview += f'### [{focus}](https://github.com/{focus})\n\n'
        _, edges = nearby(data, focus)
        edges = [edge for edge in edges if edge['from'] == focus
                 and edge['kind'] not in {'uses automation from', 'runs workflow from'}]
        for kind in sorted({edge['kind'] for edge in edges}):
            targets = sorted({edge['to'] for edge in edges if edge['kind'] == kind})
            links = [f"[{target.split('/')[-1]}](https://github.com/{target})" for target in targets]
            overview += f"- **{kind.capitalize()}:** " + ' · '.join(links) + '\n'
        overview += f'\n[Explore connections](maps/{slug(focus)}.md).\n\n'
    overview += '## All repositories\n\nGroups organise browsing; they do not assert dependencies.\n\n'
    for group in sorted({node['group'] for node in nodes}):
        overview += f'### {group}\n\n'
        for node in nodes:
            if node['group'] != group:
                continue
            state = '' if node['id'] in connected else ' · connections not yet reviewed'
            if node['archived']:
                state += ' · archived'
            overview += f"- {repo_link(node)} · [Explore](maps/{slug(node['id'])}.md){state}\n"
        overview += '\n'
    overview += '[Map data and updates](data/README.md) · [Licence](LICENSE)\n'
    (ROOT/'README.md').write_text(overview)
    (ROOT/'index.html').write_text(html_page(overview, 'Qualcomm repository map'))
    # Include the small maintenance note in the offline copy so every local link resolves.
    (ROOT/'data/README.html').write_text(html_page((ROOT/'data/README.md').read_text(), 'Map data and updates'))
    for node in nodes:
        name = slug(node['id'])
        page = render_view(data, node['id'], digest)
        (OUTPUT/f'{name}.md').write_text(page)
        (OUTPUT/f'{name}.html').write_text(html_page(page, node['id']))


def main() -> None:
    """Build the map or export a nearby Markdown snapshot at a recorded commit."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', help='Exact repository identifier to export')
    parser.add_argument('--destination', type=Path, help='Directory receiving REPOSITORY_MAP.md')
    parser.add_argument('--revision', help='Central map commit identifying the export source')
    args = parser.parse_args()
    data = load_data(DATA)
    digest = hashlib.sha256(DATA.read_bytes()).hexdigest()
    if args.export:
        if args.destination is None or not args.revision or not re.fullmatch('[0-9a-f]{40}', args.revision):
            parser.error('Export requires --destination and --revision with a full commit SHA')
        subprocess.run(['git', 'cat-file', '-e', args.revision + '^{commit}'], cwd=ROOT, check=True)
        subprocess.run(['git', 'diff', '--exit-code', args.revision, '--', 'data', 'tools'], cwd=ROOT, check=True)
        args.destination.mkdir(parents=True, exist_ok=True)
        (args.destination/'REPOSITORY_MAP.md').write_text(render_local_view(data, args.export, digest, args.revision))
        print(f'Exported linked nearby map for {args.export}')
    else:
        build(data, digest)
        print(f"Generated {len(data['repositories'])} linked nearby maps")


if __name__ == '__main__':
    main()
