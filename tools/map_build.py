"""Generate the Qualcomm ecosystem overview and nearby repository views.

The JSON dataset owns repository facts. Markdown, SVG, and exported nearby views
are derived outputs. The generator runs without network access.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/repositories.json"
OUTPUT = ROOT / "docs/source/.generated"
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


def diagram(nodes: list[dict], edges: list[dict], focus: str) -> str:
    """Render an accessible SVG showing directed relationships around one repo.

    :param nodes: Selected repository records.
    :param edges: Incident relationship records.
    :param focus: Identifier to highlight as the reader's current repository.
    :returns: Self-contained SVG text with labels and no external assets.

    Example: ``diagram(*nearby(load_data(DATA), 'qualcomm-linux/meta-qcom'), 'qualcomm-linux/meta-qcom')``.
    """
    neighbours = [n for n in nodes if n["id"] != focus]
    height = max(240, len(neighbours) * 130 + 60)
    centre = height / 2
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 {height}" role="img" aria-labelledby="title desc">',
           f'<title id="title">Repository neighbourhood: {html.escape(focus)}</title>',
           '<desc id="desc">The highlighted repository is your current location. Arrows follow the direction of each labelled relationship. The accompanying table provides applicability and evidence.</desc>',
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#48617a"/></marker></defs>',
           '<rect width="1080" height="100%" rx="14" fill="#f6f8fc"/>',
           '<g font-family="sans-serif" font-size="15" fill="#182c43">',
           f'<rect x="20" y="{centre-52}" width="370" height="104" rx="12" fill="#dbeafe" stroke="#1554ae" stroke-width="3"/>',
           f'<text x="40" y="{centre-18}" font-weight="bold" fill="#1554ae">YOU ARE HERE</text>']
    for i, line in enumerate(textwrap.wrap(focus, 36, break_long_words=False)):
        out.append(f'<text x="40" y="{centre+10+i*20}">{html.escape(line)}</text>')
    for i, node in enumerate(neighbours):
        y = 60 + i * 130
        incident = [e for e in edges if node["id"] in (e["from"], e["to"])]
        for j, edge in enumerate(incident):
            offset = (j - (len(incident)-1)/2) * 22
            optional = edge["kind"] in {"integrates with", "selects for distro", "uses indirectly"}
            dash = ' stroke-dasharray="6 4"' if optional else ''
            marker = 'marker-end' if edge['from'] == focus else 'marker-start'
            out.append(f'<path d="M 390 {centre+offset} C 480 {centre+offset}, 500 {y+35+offset}, 680 {y+35+offset}" fill="none" stroke="#48617a" stroke-width="2" {marker}="url(#arrow)"{dash}/>')
            out.append(f'<rect x="443" y="{y+8+offset}" width="218" height="22" rx="4" fill="#f6f8fc"/>')
            out.append(f'<text x="450" y="{y+24+offset}" font-size="13">{html.escape(edge["kind"])}</text>')
        out.append(f'<rect x="680" y="{y}" width="380" height="76" rx="10" fill="white" stroke="#a3b3c5"/>')
        for j, line in enumerate(textwrap.wrap(node['id'], 38, break_long_words=False)):
            out.append(f'<text x="698" y="{y+29+j*20}">{html.escape(line)}</text>')
    if not neighbours:
        out.append('<text x="450" y="130">No reviewed relationships recorded.</text>')
    out.append('</g></svg>')
    return '\n'.join(out)+'\n'


def relation_table(edges: list[dict]) -> str:
    """Format direction, applicability, and source evidence for relationships.

    :param edges: Validated relationship records.
    :returns: Markdown table with one row per relationship.

    Example: ``relation_table([])`` returns a table header with no data rows.
    """
    lines = ['| From | Relationship | To | When it applies | Evidence |', '| --- | --- | --- | --- | --- |']
    for edge in edges:
        proofs = ' · '.join(f"[{index+1}]({proof['url']})" for index, proof in enumerate(edge['evidence']))
        values = [edge['from'], edge['kind'], edge['to'], edge['condition'], proofs]
        lines.append('| ' + ' | '.join(v.replace('|','\\|').replace('\n',' ') for v in values) + ' |')
    return '\n'.join(lines)+'\n'


def render_view(data: dict, focus: str, image_name: str, digest: str, revision: str | None = None) -> str:
    """Generate a nearby view from the shared data, including revision provenance.

    :param data: Validated dataset.
    :param focus: Current repository identifier.
    :param image_name: Relative SVG filename beside this Markdown page.
    :param digest: SHA-256 of the source dataset.
    :param revision: Optional central repository commit used by an exported view.
    :returns: Markdown guide with a map, relationship evidence, and navigation.

    Example: ``render_view(load_data(DATA), 'qualcomm-linux/meta-qcom-3rdparty', 'map.svg', 'digest')``.
    """
    nodes, edges = nearby(data, focus)
    central = 'https://github.com/devdocsorg/qualcomm-repository-map'
    text = f'# Repository map: {focus}\n\n**You are here:** `{focus}`. This view shows recorded nearby repositories, including\nboth incoming and outgoing relationships. Dashed lines mean optional or indirect\nrelationships; the table states when each connection applies.\n\n![Nearby repositories for {focus}]({image_name})\n\n'
    text += relation_table(edges) if edges else 'No reviewed relationships are recorded yet. This does not establish independence.\n'
    text += '\n## Nearby repositories\n\n'
    for node in nodes:
        description = re.sub(r"(https?://[^\s)]+)", r"<\1>", node['description'].strip())
        text += f"- [{node['id']}]({node['url']}) — {description}\n"
    text += f'\n## Full ecosystem map\n\nReturn to the [Qualcomm repository map]({central}) for the wider ecosystem,\nother nearby views, and the locally browsable site. Relationship claims apply to\nthe linked evidence revisions; use release-compatible revisions for a build.\n'
    text += f'\nGenerated from `data/repositories.json` (SHA-256 `{digest}`).\n'
    if revision:
        text += f'Source: [central map revision `{revision[:12]}`]({central}/tree/{revision}).\n'
    text += 'Edit the shared dataset and regenerate this view to change relationships.\n'
    return text


def build(data: dict, digest: str) -> None:
    """Generate the overview and every repository's nearby Markdown/SVG pair.

    :param data: Validated dataset.
    :param digest: SHA-256 identifying the dataset used for generated views.
    :returns: None; writes deterministic output under ``docs/source/.generated``.
    :raises OSError: If generated files cannot be written.

    Example: ``build(load_data(DATA), hashlib.sha256(DATA.read_bytes()).hexdigest())``.
    """
    OUTPUT.mkdir(exist_ok=True)
    for old in OUTPUT.iterdir():
        if old.suffix in {'.md', '.svg'}:
            old.unlink()
    nodes = sorted(data['repositories'], key=lambda n: n['id'])
    edges = data['relationships']
    connected = {e[end] for e in edges for end in ('from','to')}
    overview = '# Qualcomm repository ecosystem\n\n' + data['scope'] + '\n\n'
    overview += f"**Coverage:** {len(nodes)} repositories in the inventory, {len(connected)} with reviewed relationships, and {len(edges)} evidenced connections.\n\n{data['coverage']}\n\n"
    overview += 'Start with a view below, then follow repository links to explore its neighbours.\n\n'
    for focus in ['qualcomm-linux/meta-qcom','qualcomm-linux/meta-qcom-3rdparty','qualcomm-linux/kernel-config','qualcomm-linux/pkg-kgsl','qualcomm-linux/pkg-gbm-msm-backend']:
        overview += f'- [{focus}]({slug(focus)}.md)\n'
    overview += '\n## Connected pathways\n\nEach diagram highlights one starting repository. The nearby pages supply branch\nconditions and evidence for every arrow.\n\n'
    for focus in ['qualcomm-linux/meta-qcom','qualcomm-linux/kernel-config','qualcomm-linux/pkg-kgsl']:
        overview += f'### {focus}\n\n[Explore this area]({slug(focus)}.md)\n\n![{focus} relationships]({slug(focus)}.svg)\n\n'
    overview += '\n## Repository inventory\n\nGroups organise browsing; they are not dependency claims. Repository names link\nto nearby views, which link to the original repository and evidence.\n\n'
    for group in sorted({n['group'] for n in nodes}):
        overview += f'### {group}\n\n| Repository | Relationship coverage |\n| --- | --- |\n'
        for node in nodes:
            if node['group']==group:
                state='Reviewed connections' if node['id'] in connected else 'Connections not yet reviewed'
                if node['archived']:state+='; archived'
                overview+=f"| [{node['id']}]({slug(node['id'])}.md) | {state} |\n"
        overview+='\n'
    overview += '## Relationship evidence\n\n'+relation_table(edges)
    overview += '\n```{toctree}\n:hidden:\n\n'
    overview += '\n'.join(slug(n['id']) for n in nodes)+'\n```\n'
    (OUTPUT/'OVERVIEW.md').write_text(re.sub(r'\n{3,}', '\n\n', overview))
    for node in nodes:
        focus=node['id']; name=slug(focus)
        (OUTPUT/f'{name}.svg').write_text(diagram(*nearby(data,focus),focus))
        page=render_view(data,focus,f'{name}.svg',digest)
        page+='\n[Back to the ecosystem overview](OVERVIEW.md).\n'
        neighbours,_=nearby(data,focus)
        for neighbour in neighbours:
            if neighbour['id'] != focus:
                page+=f"\n[Explore {neighbour['id']}]({slug(neighbour['id'])}.md).\n"
        (OUTPUT/f'{name}.md').write_text(page)


def main() -> None:
    """Build all views or export one nearby view into a repository's docs.

    :returns: None; writes generated files and prints a coverage summary.
    :raises SystemExit: For invalid command-line arguments.
    :raises ValueError: For invalid source data or export revisions.

    Example: ``python tools/map_build.py --export qualcomm-linux/meta-qcom-3rdparty --destination /tmp/nearby --revision <commit>``.
    """
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export',help='Exact repository identifier to export')
    parser.add_argument('--destination',type=Path,help='Directory receiving REPOSITORY_MAP.md and repository-map.svg')
    parser.add_argument('--revision',help='Central map commit identifying the export source')
    args=parser.parse_args()
    data=load_data(DATA); digest=hashlib.sha256(DATA.read_bytes()).hexdigest()
    if args.export:
        if args.destination is None or not args.revision or not re.fullmatch('[0-9a-f]{40}',args.revision):
            parser.error('Export requires --destination and --revision with a full commit SHA')
        subprocess.run(["git", "cat-file", "-e", args.revision + "^{commit}"], cwd=ROOT, check=True)
        subprocess.run(["git", "diff", "--exit-code", args.revision, "--", "data", "tools"], cwd=ROOT, check=True)
        nodes,edges=nearby(data,args.export)
        args.destination.mkdir(parents=True,exist_ok=True)
        (args.destination/'repository-map.svg').write_text(diagram(nodes,edges,args.export))
        (args.destination/'REPOSITORY_MAP.md').write_text(render_view(data,args.export,'repository-map.svg',digest,args.revision))
        print(f'Exported {args.export}: {len(nodes)} repositories, {len(edges)} relationships')
    else:
        build(data,digest)
        print(f"Generated {len(data['repositories'])} nearby views and {len(data['relationships'])} relationships")


if __name__=='__main__':
    main()
