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
            (urls[candidate['from']], candidate.get('local_summary') or map_build.LABELS[candidate['kind']], urls[candidate['to']])
            for candidate in data['relationships']
            if candidate['kind'] != 'uses indirectly'
            and candidate['from'] == edge['from'] and candidate['to'] == edge['to']
        }
        assert {connection for connection in connections
                if connection[0] == urls[edge['from']] and connection[2] == urls[edge['to']]} <= direct
    else:
        label = edge.get('local_summary') or map_build.LABELS[edge['kind']]
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
    for line in re.findall(r'^    r\d+ -->.*\n', local, re.M):
        rejects(map_build.validate_local_view, data, node['id'], local.replace(line, ''))
local = map_build.render_local_view(data, focus, digest, 'a'*40)
assert local.count('(you are here)') == 1
assert 'Required:' not in local and 'Optional:' not in local
assert 'qcom-ptool' in local and '(private)' not in local
assert f'[Full Qualcomm repository map]({map_build.CENTRAL})' in local

# An inherited connection alone never permits a made-up direct shortcut.
links = dict(re.findall(r'click (r\d+) href "([^"]+)"', local))
current_id = next(node for node, url in links.items() if url == urls[focus])
tool_id = next(node for node, url in links.items() if url == urls['qualcomm-linux/qcom-ptool'])
shortcut = f'    {current_id} -->|"uses indirectly"| {tool_id}\n'
invented = local.replace('    style ', shortcut + '    style ', 1)
rejects(map_build.validate_local_view, data, focus, invented)

# Adding a neighbour must change the export without changing generator allowlists.
extended = copy.deepcopy(data)
extended['repositories'].append(dict(data['repositories'][0], id='example/new-input', url='https://github.com/example/new-input'))
extended['relationships'].append(dict(next(e for e in data['relationships'] if e['from'] == focus and e['kind'] == 'depends on'), to='example/new-input'))
assert 'https://github.com/example/new-input' in map_build.render_local_view(extended, focus, digest, 'a'*40)

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

for mutation in ('unknown_endpoint', 'missing_evidence', 'duplicate', 'unpinned', 'missing_path'):
    broken = copy.deepcopy(data)
    if mutation == 'unknown_endpoint':
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
    (checkout/'build.yml').write_text('url: https://github.com/example/missing.git\n')
    subprocess.run(['git', 'add', '.'], cwd=checkout, check=True)
    subprocess.run(['git', '-c', 'user.name=Map test', '-c', 'user.email=map@example.invalid', 'commit', '-qm', 'Source fixture'], cwd=checkout, check=True)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip()
    rejects(check_sources.check, data, {'repository':focus, 'revision':revision, 'paths':['build.yml']}, checkout)
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
