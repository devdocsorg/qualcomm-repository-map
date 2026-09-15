"""Check map invariants and Python docstring coverage without network access."""
import ast
import copy
import json
import tempfile
import sys
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
assert map_build.diagram(nodes, edges, focus) == map_build.diagram(nodes, edges, focus)
assert 'YOU ARE HERE' in map_build.diagram(nodes, edges, focus)
assert 'stroke-dasharray' in map_build.diagram(nodes, edges, focus)
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

reference = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else None
count = 0
for source in sorted((map_build.ROOT/'tools').glob('*.py')):
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            assert ast.get_docstring(node), f'Missing native docstring: {source.name}:{node.name}'
            if reference is not None and source.name == 'map_build.py':
                assert f'id="map_build.{node.name}"' in reference, f'Missing generated entry: {node.name}'
            count += 1
print(f'Map invariants and negative tests passed; {count} functions have native documentation')
