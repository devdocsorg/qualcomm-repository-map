"""Check component coverage, evidence, README exports, source discovery, and docs."""
import ast
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
import pydoc
import re
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit

import check_sources
import map_build


def arrows(markdown):
    """Read linked diagram arrows independently of the generator's selection logic."""
    result = set()
    for graph in re.findall(r'```mermaid\n(.*?)\n```', markdown, re.S):
        links = dict(re.findall(r'click (r\d+) href "([^"]+)"', graph))
        identifiers = set(re.findall(r'^    (r\d+)\[', graph, re.M))
        assert identifiers == set(links), 'Unlinked node'
        assert len(links) <= map_build.MAX_MAP_NODES
        assert len(set(links.values())) == len(links)
        for source, label, target in re.findall(r'^    (r\d+) -->\|"([^"]+)"\| (r\d+)$', graph, re.M):
            result.add((links[source], label, links[target]))
    return result


def without_connection(markdown, connection):
    """Remove every occurrence of a connection across diagrams with local node IDs."""
    blocks = re.split(r'(```mermaid\n.*?\n```)', markdown, flags=re.S)
    for index, block in enumerate(blocks):
        if not block.startswith('```mermaid'):
            continue
        links = dict(re.findall(r'click (r\d+) href "([^"]+)"', block))
        lines = []
        for line in block.splitlines(keepends=True):
            arrow = re.fullmatch(r'    (r\d+) -->\|"([^"]+)"\| (r\d+)\n', line)
            if arrow and (links[arrow[1]], arrow[2], links[arrow[3]]) == connection:
                continue
            lines.append(line)
        blocks[index] = ''.join(lines)
    return ''.join(blocks)


def rejects(function, *args):
    """Require a validation failure for deliberately incomplete input."""
    try:
        function(*args)
    except ValueError:
        return
    raise AssertionError('Invalid input accepted')


data = map_build.load_data(map_build.DATA)
focus = 'qualcomm-linux/meta-qcom-3rdparty'
digest = hashlib.sha256(map_build.DATA.read_bytes()).hexdigest()
readme = (map_build.ROOT/'README.md').read_text()
connections = arrows(readme)
urls = {node['id']: node['url'] for node in data['repositories']}
assert readme.count('```mermaid') > 1
assert 'uses indirectly' not in readme
for title, nodes, edges in map_build.cluster_maps(data):
    assert any(e['kind'] not in map_build.AUTOMATION for e in edges), title
assert any(label == 'runs automation from' for _, label, _ in connections), 'Lost mixed integration context'
for edge in data['relationships']:
    if edge['kind'] in map_build.AUTOMATION:
        continue
    if edge['kind'] == 'uses indirectly':
        route = [edge['from'], *edge['via'], edge['to']]
        for source, target in zip(route, route[1:]):
            assert any(a == urls[source] and b == urls[target] for a, _, b in connections)
        # A separate evidenced direct use may coexist with the inherited path.
        direct = {
            (urls[candidate['from']], map_build.connection_label(candidate), urls[candidate['to']])
            for candidate in data['relationships']
            if candidate['kind'] != 'uses indirectly'
            and candidate['from'] == edge['from'] and candidate['to'] == edge['to']
        }
        assert {connection for connection in connections
                if connection[0] == urls[edge['from']] and connection[2] == urls[edge['to']]} <= direct
    else:
        label = map_build.connection_label(edge)
        assert (urls[edge['from']], label, urls[edge['to']]) in connections
for node in data['repositories']:
    assert f"]({node['url']})" in readme
    assert node['description'] in re.sub(r'<(https?://[^>]+)>', r'\1', readme)
displayed = {(e['from'], e['to'], e['kind']) for _, _, edges in map_build.cluster_maps(data) for e in edges}
visible_edges = [e for e in data['relationships'] if e['kind'] not in map_build.AUTOMATION or (e['from'], e['to'], e['kind']) in displayed]
evidence = [p for edge in visible_edges for p in edge['evidence']]
expected_links = Counter((Path(unquote(urlsplit(p['url']).path)).name, p['url']) for p in evidence)
actual_links = Counter(re.findall(r'^  - \[([^\]]+)\]\((https://github.com/[^)]+/blob/[^)]+)\)$', readme, re.M))
assert actual_links == expected_links, 'Evidence or filename labels changed'
assert 'The uses field calls automation from' not in readme
headings = {re.sub(r'[^a-z0-9 -]', '', title.lower()).replace(' ', '-') for title in re.findall(r'^## (.+)$', readme, re.M)}
assert set(re.findall(r'\]\(#([^)]*)\)', readme)) <= headings
assert not list(map_build.ROOT.glob('maps/*'))
assert not list(map_build.ROOT.glob('*.html'))

# Exercise all neighbourhoods, including those with incoming-only connections.
for node in data['repositories']:
    local = map_build.render_local_view(data, node['id'], digest, 'a'*40)
    arrows(local)
    map_build.validate_local_view(data, node['id'], local)
    for block in re.findall(r'```mermaid\n(.*?)```', local, re.S):
        assert block.count('(you are here)') == 1
        assert block.count(f'href "{urls[node["id"]]}"') == 1
    assert '```\n###' not in local, 'Split diagrams need a blank line before headings'
    for connection in arrows(local):
        rejects(map_build.validate_local_view, data, node['id'], without_connection(local, connection))
local = map_build.render_local_view(data, focus, digest, 'a'*40)
assert 'Required:' not in local and 'Optional:' not in local
assert 'qcom-ptool' in local and '(private)' not in local
assert f'[Full Qualcomm repository map]({map_build.CENTRAL})' in local

# The same connection can occur in several diagrams with different local IDs.
repeated = local + re.sub(r'\br(\d+)\b', lambda match: f'r{int(match[1]) + 100}', local)
map_build.validate_local_view(data, focus, repeated)
for connection in arrows(repeated):
    rejects(map_build.validate_local_view, data, focus, without_connection(repeated, connection))

# An inherited connection alone never permits a made-up direct shortcut.
# Node IDs are local to each diagram, so inject it into the diagram showing the tool.
block = next(block for block in re.findall(r'```mermaid\n.*?\n```', local, re.S)
             if f'href "{urls["qualcomm-linux/qcom-ptool"]}"' in block)
links = dict(re.findall(r'click (r\d+) href "([^"]+)"', block))
current_id = next(node for node, url in links.items() if url == urls[focus])
tool_id = next(node for node, url in links.items() if url == urls['qualcomm-linux/qcom-ptool'])
shortcut = f'    {current_id} -->|"uses indirectly"| {tool_id}\n'
invented = local.replace(block, block.replace('    style ', shortcut + '    style ', 1), 1)
assert invented != local
rejects(map_build.validate_local_view, data, focus, invented)

# Adding a neighbour must change the export without changing generator allowlists.
extended = copy.deepcopy(data)
extended['repositories'].append(dict(data['repositories'][0], id='qualcomm-linux/example-new-input', url='https://github.com/qualcomm-linux/example-new-input'))
extended['relationships'].append(dict(next(e for e in data['relationships'] if e['from'] == focus and e['kind'] == 'depends on'), to='qualcomm-linux/example-new-input'))
expanded = map_build.render_local_view(extended, focus, digest, 'a'*40)
assert 'https://github.com/qualcomm-linux/example-new-input' in expanded
# Enough neighbours to exceed the node limit must split the view, not drop connections.
template = next(e for e in data['relationships'] if e['from'] == focus and e['kind'] == 'depends on')
for number in range(map_build.MAX_MAP_NODES):
    extended['repositories'].append(dict(data['repositories'][0], id=f'qualcomm-linux/example-input-{number}',
                                         url=f'https://github.com/qualcomm-linux/example-input-{number}'))
    extended['relationships'].append(dict(template, to=f'qualcomm-linux/example-input-{number}'))
expanded = map_build.render_local_view(extended, focus, digest, 'a'*40)
assert all(f'https://github.com/qualcomm-linux/example-input-{number}' in expanded for number in range(map_build.MAX_MAP_NODES))
blocks = re.findall(r'```mermaid\n(.*?)```', expanded, re.S)
assert len(blocks) > 1
assert all(block.count('(you are here)') == 1 for block in blocks)
assert '```\n###' not in expanded

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp)/'README.md'
    authored = '# Layer\n\n[Contributing](CONTRIBUTING.md).\n\n## Files\n\n- [README](README.md)\n'
    path.write_text(authored)
    map_build.update_readme(path, local)
    first = path.read_text()
    assert first.startswith(authored) and first.rstrip().endswith(map_build.END)
    map_build.update_readme(path, local, check=True)
    map_build.update_readme(path, local)
    assert path.read_text() == first
    for broken in (first+'\n## Extra section\n', first+map_build.START,
                   first.replace(map_build.END, ''), first.replace('adds third-party board support to', 'wrong')):
        path.write_text(broken)
        try:
            map_build.update_readme(path, local, check=True)
        except ValueError:
            assert path.read_text() == broken
        else:
            raise AssertionError('Invalid or stale README map accepted')

for mutation in ('outside_qualcomm', 'empty_branches', 'default_branch_label', 'unknown_endpoint', 'missing_evidence', 'duplicate', 'unpinned', 'missing_path'):
    broken = copy.deepcopy(data)
    if mutation == 'outside_qualcomm':
        broken['repositories'].append(dict(broken['repositories'][0], id='example/upstream', url='https://github.com/example/upstream'))
    elif mutation == 'empty_branches':
        broken['relationships'][0]['branches'] = []
    elif mutation == 'default_branch_label':
        edge = next(e for e in broken['relationships'] if e['from'] == focus)
        edge['branches'] = [next(r['branch'] for r in broken['repositories'] if r['id'] == focus), 'other']
    elif mutation == 'unknown_endpoint':
        broken['relationships'][0]['to'] = 'absent/repository'
    elif mutation == 'missing_evidence':
        broken['relationships'][0]['evidence'] = []
    elif mutation == 'duplicate':
        broken['relationships'].append(copy.deepcopy(broken['relationships'][0]))
    elif mutation == 'unpinned':
        broken['relationships'][0]['evidence'][0]['revision'] = 'main'
    else:
        next(e for e in broken['relationships'] if e['kind'] == 'uses indirectly').pop('via')
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/'data.json'
        path.write_text(json.dumps(broken))
        rejects(map_build.load_data, path)

# Source discovery is independent of rendered-map coverage.
with tempfile.TemporaryDirectory() as tmp:
    checkout = Path(tmp)
    subprocess.run(['git', 'init', '-q', str(checkout)], check=True)
    (checkout/'build.yml').write_text('url: https://github.com/qualcomm-linux/example-missing.git\nurl: https://github.com/example/upstream.git\n')
    subprocess.run(['git', 'add', '.'], cwd=checkout, check=True)
    subprocess.run(['git', '-c', 'user.name=Map test', '-c', 'user.email=map@example.invalid', 'commit', '-qm', 'Source fixture'], cwd=checkout, check=True)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip()
    rejects(check_sources.check, data, {'repository':focus, 'revision':revision, 'paths':['build.yml']}, checkout)
    # The audited fork's own source links do not make it a separate dependency.
    fork_audit = {'repository':focus, 'source_repository':'qualcomm-linux/example-missing', 'revision':revision, 'paths':['build.yml']}
    check_sources.check(data, fork_audit, checkout)
    rejects(check_sources.check, data, {**fork_audit, 'paths':['build.yml', 'absent.yml']}, checkout)
    rejects(check_sources.check, data, {**fork_audit, 'source_repository':'qualcomm-linux/example-another'}, checkout)
assert check_sources.references('url: https://git.yoctoproject.org/meta-security\n# https://github.com/example/ignored') == {'https://git.yoctoproject.org/meta-security'}

reference = pydoc.plain(pydoc.render_doc(map_build))
count = 0
for source in sorted((map_build.ROOT/'tools').glob('*.py')):
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            assert ast.get_docstring(node), f'Missing native docstring: {source.name}:{node.name}'
            if source.name == 'map_build.py':
                assert f'{node.name}(' in reference, f'Missing pydoc entry: {node.name}'
            count += 1
print(f'{len(data["repositories"])} repository views checked; component coverage, omission regressions, source discovery, evidence, exports, and {count} native docstrings pass')
