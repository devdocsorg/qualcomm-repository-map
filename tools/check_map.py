"""Check map invariants and Python docstring coverage without network access."""
import ast
import copy
import json
import tempfile
import pydoc
import re
from urllib.parse import unquote, urlsplit
from pathlib import Path

import map_build

data = map_build.load_data(map_build.DATA)
focus = 'qualcomm-linux/meta-qcom-3rdparty'
nodes, edges = map_build.nearby(data, focus)
expected_neighbours = {'qualcomm-linux/meta-qcom', 'openembedded/openembedded-core',
                       'qualcomm-linux/meta-qcom-distro', 'qualcomm-linux/qcom-ptool',
                       'rubikpi-ai/boot-assets'}
assert expected_neighbours <= {node['id'] for node in nodes}
assert len(edges) >= 5
assert all(focus in (edge['from'], edge['to']) for edge in edges)
view = map_build.render_view(data, focus, 'test-digest')
assert '**You are here: [' in view
assert '![' not in view and '<svg' not in view
assert view.count(' → **') == len(edges), 'Every edge must appear once with its own type'
for edge in edges:
    assert f"[{edge['from']}](https://github.com/{edge['from']}) → **{edge['kind']}** → [{edge['to']}](https://github.com/{edge['to']})" in view
    for endpoint in ('from', 'to'):
        identifier = edge[endpoint]
        assert f'[{identifier}](https://github.com/{identifier})' in view
    assert edge['condition'] in view
    for proof in edge['evidence']:
        assert proof['url'] in view
# Local readers see only build relationships and one occurrence of the current name.
local = map_build.render_local_view(data, focus, 'test-digest', 'a' * 40)
assert local.count('[meta-qcom-3rdparty]') == 1
assert local.count('| [') == 5
assert 'Required: base OpenEmbedded layer.' in local
assert 'Optional: Qualcomm reference distro.' in local
assert 'RUBIK Pi 3 firmware, fetched by the build.' in local
assert 'Partition tools, supplied through meta-qcom.' in local
assert 'bitbake-lint-action' not in local and 'evidence 1' not in local
assert 'dataset SHA-256' not in re.sub(r'<!--.*?-->', '', local, flags=re.S)
assert 'Full map and relationship details' in local
missing_summary = copy.deepcopy(data)
for edge in missing_summary['relationships']:
    edge.pop('local_summary', None)
try:
    map_build.render_local_view(missing_summary, focus, 'test-digest', 'a' * 40)
except ValueError:
    pass
else:
    raise AssertionError('Local export accepted missing summaries')

# Incoming edges must also appear when the user starts at a provider repository.
provider_nodes, provider_edges = map_build.nearby(data, 'rubikpi-ai/boot-assets')
assert len(provider_nodes) == 2 and provider_edges[0]['from'] == focus

for mutation in ('unknown_endpoint', 'missing_evidence', 'duplicate', 'unpinned'):
    broken = copy.deepcopy(data)
    if mutation == 'unknown_endpoint':
        broken['relationships'][0]['to'] = 'absent/repository'
    elif mutation == 'missing_evidence':
        broken['relationships'][0]['evidence'] = []
    elif mutation == 'duplicate':
        broken['relationships'].append(copy.deepcopy(broken['relationships'][0]))
    else:
        broken['relationships'][0]['evidence'][0]['revision'] = 'main'
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp)/'invalid.json'
        path.write_text(json.dumps(broken))
        try:
            map_build.load_data(path)
        except ValueError:
            pass
        else:
            raise AssertionError(f'Invalid data accepted: {mutation}')

reference = pydoc.plain(pydoc.render_doc(map_build))
count = 0
for source in sorted((map_build.ROOT/'tools').glob('*.py')):
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            assert ast.get_docstring(node), f'Missing native docstring: {source.name}:{node.name}'
            if source.name == 'map_build.py':
                assert f'{node.name}(' in reference, f'Missing native pydoc entry: {node.name}'
            count += 1
print(f'Map invariants and negative tests passed; {count} functions have native documentation')

# Every generated local link must survive a checkout opened with file://.
for page in [map_build.ROOT/'index.html', map_build.ROOT/'data/README.html', *map_build.OUTPUT.glob('*.html')]:
    content = page.read_text()
    assert not re.search(r'<(?:img|svg|script|iframe)\b', content), f'Unexpected picture or runtime: {page}'
    for href in re.findall(r'href="([^"]+)"', content):
        target = urlsplit(href)
        if not target.scheme and target.path:
            assert (page.parent/unquote(target.path)).is_file(), f'Broken local link: {page}: {href}'
print('All map names are linked; local navigation and evidence preservation passed')
