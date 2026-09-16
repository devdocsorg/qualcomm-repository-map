"""Check relationship preservation, nearby scope, README exports, and native docs."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import pydoc
import re
import tempfile

import map_build

data = map_build.load_data(map_build.DATA)
focus = 'qualcomm-linux/meta-qcom-3rdparty'
digest = hashlib.sha256(map_build.DATA.read_bytes()).hexdigest()
readme = (map_build.ROOT/'README.md').read_text()
graph = readme.split('```mermaid\n')[1].split('```')[0]
assert len(re.findall(r'^    r\d+\[', graph, re.M)) == len(data['repositories'])
for node in data['repositories']:
    assert graph.count(f'href "{node["url"]}"') == 1
    assert node['description'] in re.sub(r'<(https?://[^>]+)>', r'\1', readme)
for edge in data['relationships']:
    assert edge['kind'] in graph and edge['condition'] in readme
    for proof in edge['evidence']:
        assert proof['claim'] in readme and proof['url'] in readme
# Verify every directed relationship, not just node presence.
ids = {node['id']: f'r{i}' for i, node in enumerate(sorted(data['repositories'], key=lambda n: n['id']))}
for edge in data['relationships']:
    assert f'{ids[edge["from"]]} -->|"{edge["kind"]}"| {ids[edge["to"]]}' in graph
assert not list(map_build.ROOT.glob('maps/*'))
assert not list(map_build.ROOT.glob('*.html'))
assert not list((map_build.ROOT/'data').glob('*.html'))

local = map_build.render_local_view(data, focus, digest, 'a' * 40)
assert local.count('["meta-qcom-3rdparty (you are here)"]') == 1
assert local.count(' href ') == 5
assert local.count(' -->|') == 4
for summary in ('Required: base OpenEmbedded layer.', 'Optional: Qualcomm reference distro.',
                'RUBIK Pi 3 firmware, fetched by the build.'):
    assert summary in local
for excluded in ('qcom-ptool', '(private)', 'bitbake-lint-action', 'REPOSITORY_MAP.md'):
    assert excluded not in local
assert 'dataset SHA-256' not in re.sub(r'<!--.*?-->', '', local, flags=re.S)
assert f'[Full Qualcomm repository map]({map_build.CENTRAL})' in local

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
                   first.replace(map_build.END, ''), first.replace('Required:', 'Incorrect:')):
        path.write_text(broken)
        try:
            map_build.update_readme(path, local, check=True)
        except ValueError:
            assert path.read_text() == broken
        else:
            raise AssertionError('Invalid or stale README map accepted')

for mutation in ('unknown_endpoint', 'missing_evidence', 'duplicate', 'unpinned', 'missing_summary'):
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
        for edge in broken['relationships']:
            edge.pop('local_summary', None)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/'data.json'
        path.write_text(json.dumps(broken))
        try:
            loaded = map_build.load_data(path)
            map_build.render_local_view(loaded, focus, digest, 'a'*40)
        except ValueError:
            pass
        else:
            raise AssertionError(f'Invalid dataset accepted: {mutation}')

reference = pydoc.plain(pydoc.render_doc(map_build))
count = 0
for source in sorted((map_build.ROOT/'tools').glob('*.py')):
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            assert ast.get_docstring(node), f'Missing native docstring: {source.name}:{node.name}'
            if source.name == 'map_build.py':
                assert f'{node.name}(' in reference, f'Missing pydoc entry: {node.name}'
            count += 1
print(f'Preserved {len(data["repositories"])} repositories and {len(data["relationships"])} relationships; README export and negative checks pass; {count} native docstrings verified')
