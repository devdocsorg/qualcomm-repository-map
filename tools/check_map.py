"""Check the map tools against a synthetic fixture, then validate the live dataset.

The regression suite runs against ``tools/fixtures/repositories.json``, a fictional
dataset, so it holds for every map made from this template. It covers component
coverage, omission regressions, branch labels, indirect paths, map-size splits,
evidence rules, export provenance, out-of-organisation rejection, source discovery,
map initialisation, and inventory merging. The live ``data/repositories.json`` is
then loaded, built, and checked for an up-to-date README and valid nearby views,
without assuming that any particular repository exists; an empty dataset passes.
"""
import ast
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
import pydoc
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

import check_sources
import map_build
import map_init
import map_inventory

TOOLS = Path(__file__).resolve().parent
FIXTURE = TOOLS / 'fixtures/repositories.json'
REVISION = 'a' * 40


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


def digest_of(data):
    """Return a stand-in dataset digest for data that exists only in memory."""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def write_temporary(directory, data):
    """Write a dataset into a temporary directory and return its path."""
    path = Path(directory) / 'repositories.json'
    map_init.write_dataset(path, data)
    return path


def run_tool(*args):
    """Run a tool script and return the completed process."""
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)


def check_overview(data, readme):
    """Check a full README map against its dataset: coverage, paths, inventory, and evidence."""
    connections = arrows(readme)
    urls = {node['id']: node['url'] for node in data['repositories']}
    assert readme.startswith(f"# {data['name']} repository map\n")
    assert all(label != 'uses indirectly' for _, label, _ in connections)
    for title, nodes, edges in map_build.cluster_maps(data):
        assert any(e['kind'] not in map_build.AUTOMATION for e in edges), title
        assert len(nodes) <= map_build.MAX_MAP_NODES, title
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
                    if connection[0] == urls[edge['from']] and connection[2] == urls[edge['to']]} <= {
                (a, label.replace('&', '#38;').replace('"', '#34;').replace('|', '#124;'), b)
                for a, label, b in direct}
        else:
            label = map_build.connection_label(edge)
            label = label.replace('&', '#38;').replace('"', '#34;').replace('|', '#124;').replace('\n', ' ')
            assert (urls[edge['from']], label, urls[edge['to']]) in connections
    for node in data['repositories']:
        assert f"]({node['url']})" in readme
        assert node['description'] in re.sub(r'<(https?://[^>]+)>', r'\1', readme)
    displayed = {(e['from'], e['to'], e['kind']) for _, _, edges in map_build.cluster_maps(data) for e in edges}
    visible_edges = [e for e in data['relationships']
                     if e['kind'] not in map_build.AUTOMATION or (e['from'], e['to'], e['kind']) in displayed]
    evidence = [p for edge in visible_edges for p in edge['evidence']]
    expected_links = Counter((Path(unquote(urlsplit(p['url']).path)).name, p['url']) for p in evidence)
    actual_links = Counter(re.findall(r'^  - \[([^\]]+)\]\((https://github.com/[^)]+/blob/[^)]+)\)$', readme, re.M))
    assert actual_links == expected_links, 'Evidence or filename labels changed'
    headings = {re.sub(r'[^a-z0-9 -]', '', title.lower()).replace(' ', '-') for title in re.findall(r'^## (.+)$', readme, re.M)}
    assert set(re.findall(r'\]\(#([^)]*)\)', readme)) <= headings
    if not data['relationships']:
        assert 'No relationships are recorded yet.' in readme and '```mermaid' not in readme
    if not data['repositories']:
        assert 'No repositories are inventoried yet.' in readme


def check_local_views(data, digest):
    """Exercise every nearby view, including incoming-only ones, and its omission regressions."""
    urls = {node['id']: node['url'] for node in data['repositories']}
    central = map_build.map_url(data)
    for node in data['repositories']:
        local = map_build.render_local_view(data, node['id'], digest, REVISION)
        arrows(local)
        map_build.validate_local_view(data, node['id'], local)
        for block in re.findall(r'```mermaid\n(.*?)```', local, re.S):
            assert block.count('(you are here)') == 1
            assert block.count(f'href "{urls[node["id"]]}"') == 1
        assert '```\n###' not in local, 'Split diagrams need a blank line before headings'
        # Export provenance: the full-map link and the source comment name the map repository.
        assert f"\n[Full {data['name']} repository map]({central}).\n" in local
        assert local.endswith(f'\n<!-- Generated from {central} at {REVISION}; dataset SHA-256: {digest}. -->\n')
        for connection in arrows(local):
            rejects(map_build.validate_local_view, data, node['id'], without_connection(local, connection))


def check_fixture():
    """Run the regression suite against the synthetic fixture dataset."""
    data = map_build.load_data(FIXTURE)
    digest = hashlib.sha256(FIXTURE.read_bytes()).hexdigest()
    organisation = data['organisations'][0]
    focus = f'{organisation}/meta-fixture-3rdparty'
    tool = f'{organisation}/fixture-ptool'
    urls = {node['id']: node['url'] for node in data['repositories']}
    readme = map_build.render_overview(data, digest)
    check_overview(data, readme)
    check_local_views(data, digest)
    connections = arrows(readme)
    assert readme.count('```mermaid') > 1
    assert 'uses indirectly' not in readme
    assert any(label == 'runs automation from' for _, label, _ in connections), 'Lost mixed integration context'
    assert '## Package automation' not in readme, 'Standalone automation diagram kept'
    assert 'The standalone package workflow claim' not in readme
    assert 'builds #38; signs #34;test#34; #124; images with' in readme, 'Authored label not escaped'
    assert '(kirkstone)' in readme, 'Branch label missing'
    assert 'not inventoried`; archived' in readme and '<https://example.invalid/retired>' in readme
    with tempfile.TemporaryDirectory() as tmp:
        map_build.build(data, digest, Path(tmp) / 'README.md')
        assert (Path(tmp) / 'README.md').read_text() == readme

    local = map_build.render_local_view(data, focus, digest, REVISION)
    assert 'Required:' not in local and 'Optional:' not in local
    assert 'fixture-ptool' in local and '(private)' not in local
    assert 'builds on (kirkstone)' in local
    assert 'reviewed for this repository' in map_build.render_local_view(data, f'{organisation}/pkg-beta', digest, REVISION)

    # The same connection can occur in several diagrams with different local IDs.
    repeated = local + re.sub(r'\br(\d+)\b', lambda match: f'r{int(match[1]) + 100}', local)
    map_build.validate_local_view(data, focus, repeated)
    for connection in arrows(repeated):
        rejects(map_build.validate_local_view, data, focus, without_connection(repeated, connection))

    # An inherited connection alone never permits a made-up direct shortcut.
    # Node IDs are local to each diagram, so inject it into the diagram showing the tool.
    block = next(block for block in re.findall(r'```mermaid\n.*?\n```', local, re.S)
                 if f'href "{urls[tool]}"' in block)
    links = dict(re.findall(r'click (r\d+) href "([^"]+)"', block))
    current_id = next(node for node, url in links.items() if url == urls[focus])
    tool_id = next(node for node, url in links.items() if url == urls[tool])
    shortcut = f'    {current_id} -->|"uses indirectly"| {tool_id}\n'
    invented = local.replace(block, block.replace('    style ', shortcut + '    style ', 1), 1)
    assert invented != local
    rejects(map_build.validate_local_view, data, focus, invented)

    # Adding a neighbour must change the export without changing generator allowlists.
    extended = copy.deepcopy(data)
    template = next(e for e in data['relationships'] if e['from'] == focus and e['kind'] == 'depends on' and not e.get('branches'))
    added = f'{organisation}/example-new-input'
    extended['repositories'].append(dict(data['repositories'][0], id=added, url=f'https://github.com/{added}'))
    extended['relationships'].append(dict(template, to=added))
    expanded = map_build.render_local_view(extended, focus, digest, REVISION)
    assert f'https://github.com/{added}' in expanded
    # Enough neighbours to exceed the node limit must split the view, not drop connections.
    inputs = [f'{organisation}/example-input-{number}' for number in range(map_build.MAX_MAP_NODES)]
    for identifier in inputs:
        extended['repositories'].append(dict(data['repositories'][0], id=identifier, url=f'https://github.com/{identifier}'))
        extended['relationships'].append(dict(template, to=identifier))
    expanded = map_build.render_local_view(extended, focus, digest, REVISION)
    assert all(f'https://github.com/{identifier}' in expanded for identifier in inputs)
    blocks = re.findall(r'```mermaid\n(.*?)```', expanded, re.S)
    assert len(blocks) > 1 and '### Connections (1/' in expanded
    assert all(block.count('(you are here)') == 1 for block in blocks)
    assert '```\n###' not in expanded
    map_build.validate_local_view(extended, focus, expanded)
    # The full map splits large groups into numbered parts within the node limit.
    titles = [title for title, _, _ in map_build.cluster_maps(extended)]
    parts = [title for title in titles if title.startswith('Yocto builds and releases (')]
    assert len(parts) > 1 and parts == [f'Yocto builds and releases ({i}/{len(parts)})' for i in range(1, len(parts) + 1)]
    check_overview(extended, map_build.render_overview(extended, digest))

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
                       first.replace(map_build.END, ''), first.replace('(you are here)', '(wrong)')):
            path.write_text(broken)
            try:
                map_build.update_readme(path, local, check=True)
            except ValueError:
                assert path.read_text() == broken
            else:
                raise AssertionError('Invalid or stale README map accepted')
        # The exporter requires a full commit SHA before touching any README.
        path.write_text(authored)
        result = run_tool(TOOLS/'map_build.py', '--export', focus, '--readme', path, '--revision', 'main')
        assert result.returncode == 2 and 'full commit SHA' in result.stderr
        assert path.read_text() == authored

    mutations = {
        'outside_organisation': lambda d: d['repositories'].append(
            dict(d['repositories'][0], id='example/upstream', url='https://github.com/example/upstream')),
        'empty_branches': lambda d: d['relationships'][0].update(branches=[]),
        'default_branch_label': lambda d: next(e for e in d['relationships'] if e['from'] == focus).update(
            branches=[next(r['branch'] for r in d['repositories'] if r['id'] == focus), 'other']),
        'unknown_endpoint': lambda d: d['relationships'][0].update(to='absent/repository'),
        'self_edge': lambda d: d['relationships'][0].update(to=d['relationships'][0]['from']),
        'unknown_kind': lambda d: d['relationships'][0].update(kind='inspired by'),
        'missing_evidence': lambda d: d['relationships'][0].update(evidence=[]),
        'duplicate': lambda d: d['relationships'].append(copy.deepcopy(d['relationships'][0])),
        'unpinned': lambda d: d['relationships'][0]['evidence'][0].update(revision='main'),
        'evidence_elsewhere': lambda d: d['relationships'][0]['evidence'][0].update(url='https://example.invalid/file'),
        'missing_path': lambda d: next(e for e in d['relationships'] if e['kind'] == 'uses indirectly').pop('via'),
        'broken_path': lambda d: next(e for e in d['relationships'] if e['kind'] == 'uses indirectly').update(via=[tool]),
        'missing_name': lambda d: d.pop('name'),
        'no_organisations': lambda d: d.update(organisations=[]),
        'invalid_organisation': lambda d: d.update(organisations=[*d['organisations'], 'not/an-org']),
        'invalid_map_repository': lambda d: d.update(map_repository='https://github.com/example/map'),
        'inventory_not_per_organisation': lambda d: d['inventory_observed'].pop(organisation),
        'inventory_date': lambda d: d['inventory_observed'].update({organisation: 'yesterday'}),
        'audit_unmapped': lambda d: d['source_audits'][0].update(repository='absent/repository'),
        'audit_unpinned': lambda d: d['source_audits'][0].update(revision='main'),
        'audit_no_paths': lambda d: d['source_audits'][0].update(paths=[]),
        'audit_no_source': lambda d: d['source_audits'][0].pop('source_repository'),
        'schema_version': lambda d: d.update(schema_version=2),
    }
    for name, mutate in mutations.items():
        broken = copy.deepcopy(data)
        mutate(broken)
        with tempfile.TemporaryDirectory() as tmp:
            try:
                map_build.load_data(write_temporary(tmp, broken))
            except ValueError:
                continue
            raise AssertionError(f'Invalid dataset accepted: {name}')
    # Organisations come from the data: the same repository is valid once its owner is listed.
    widened = copy.deepcopy(data)
    mutations['outside_organisation'](widened)
    widened['organisations'].append('example')
    for field in ('inventory_source', 'inventory_observed'):
        widened[field]['example'] = data[field][organisation]
    with tempfile.TemporaryDirectory() as tmp:
        map_build.load_data(write_temporary(tmp, widened))
    return data


def check_source_discovery(data):
    """Check source audits: organisation filter, transfers, binaries, automation, and forks."""
    organisation = data['organisations'][0]
    focus = f'{organisation}/meta-fixture-3rdparty'
    resolved = []
    transfers = {'https://github.com/old-owner/fixture-ptool': f'https://github.com/{organisation}/fixture-ptool',
                 'https://github.com/old-owner/kernel-config': f'https://github.com/{organisation}/kernel-config'}

    def canonical(url):
        """Stand in for GitHub's redirects so the suite needs no network access."""
        resolved.append(url)
        return transfers.get(url, url)

    real_canonical, check_sources.canonical = check_sources.canonical, canonical
    try:
        with tempfile.TemporaryDirectory() as tmp:
            checkout = Path(tmp)
            subprocess.run(['git', 'init', '-q', str(checkout)], check=True)
            files = {
                'build.yml': f'url: https://github.com/{organisation}/example-missing.git\nurl: https://github.com/example/upstream.git\n',
                'notes.md': f'https://github.com/{organisation}/example-missing\n',
                'binary.bin': b'\0' + f'https://github.com/{organisation}/example-missing'.encode(),
                'transfer.yml': 'url: https://github.com/old-owner/fixture-ptool.git\n',
                'transfer-unmapped.yml': 'url: https://github.com/old-owner/kernel-config.git\n',
                '.github/workflows/check.yml': f'uses: {data["organisations"][1]}/reusable-workflows/x.yml@main\n'
                                               f'# https://github.com/{organisation}/example-missing\n'
                                               f'url: https://github.com/{data["organisations"][1]}/reusable-workflows\n',
                'ci/check.yml': f'url: https://github.com/{data["organisations"][1]}/reusable-workflows\n',
                'mapped.yml': f'url: https://github.com/{organisation}/meta-fixture.git\n',
            }
            for name, content in files.items():
                (checkout/name).parent.mkdir(parents=True, exist_ok=True)
                (checkout/name).write_bytes(content if isinstance(content, bytes) else content.encode())
            subprocess.run(['git', 'add', '.'], cwd=checkout, check=True)
            subprocess.run(['git', '-c', 'user.name=Map test', '-c', 'user.email=map@example.invalid',
                            'commit', '-qm', 'Source fixture'], cwd=checkout, check=True)
            revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip()

            def audit(repository, *paths, source=None):
                """Build an audit record for the fixture checkout."""
                return {'repository': repository, 'source_repository': source or repository,
                        'revision': revision, 'paths': list(paths)}

            # Source discovery is independent of rendered-map coverage.
            rejects(check_sources.check, data, audit(focus, 'build.yml'), checkout)
            check_sources.check(data, audit(focus, 'mapped.yml'), checkout)
            # Repositories outside the organisations are resolved, then skipped.
            check_sources.check(data, audit(f'{organisation}/meta-fixture', 'notes.md', 'binary.bin', 'transfer.yml'), checkout)
            assert 'https://github.com/old-owner/fixture-ptool' in resolved
            assert not any(url.startswith(f'https://github.com/{organisation}/') for url in resolved)
            # A repository transferred into an organisation counts once resolved.
            rejects(check_sources.check, data, audit(f'{organisation}/meta-fixture', 'transfer-unmapped.yml'), checkout)
            # Workflows may reference the automation the repository runs; other files may not.
            checkers = f'{organisation}/kernel-checkers'
            check_sources.check(data, audit(checkers, '.github'), checkout)
            rejects(check_sources.check, data, audit(checkers, 'ci/check.yml'), checkout)
            # The audited fork's own source links do not make it a separate dependency.
            fork_audit = audit(focus, 'build.yml', source=f'{organisation}/example-missing')
            resolved.clear()
            check_sources.check(data, fork_audit, checkout)
            assert resolved == ['https://github.com/example/upstream']
            rejects(check_sources.check, data, {**fork_audit, 'paths': ['build.yml', 'absent.yml']}, checkout)
            rejects(check_sources.check, data, {**fork_audit, 'source_repository': f'{organisation}/example-another'}, checkout)
    finally:
        check_sources.canonical = real_canonical
    assert check_sources.references('url: https://git.yoctoproject.org/meta-security\n# https://github.com/example/ignored') == {'https://git.yoctoproject.org/meta-security'}
    assert check_sources.references('wget https://raw.githubusercontent.com/example/tool/main/x.sh') == {'https://github.com/example/tool'}


def check_initialisation():
    """Check map_init and map_inventory, and that an empty or unrelated map renders."""
    data = map_init.new_dataset('Example', ['example-org', 'example-labs'], 'example-org/repository-map', '2026-01-01')
    assert 'example-org and example-labs' in data['scope']
    assert data['inventory_source'] == {name: map_init.inventory_url(name) for name in ('example-org', 'example-labs')}
    assert data['inventory_observed'] == {'example-org': '2026-01-01', 'example-labs': '2026-01-01'}
    rejects(map_init.new_dataset, 'Example', [], 'example-org/repository-map', '2026-01-01')
    rejects(map_init.new_dataset, 'Example', ['example-org'], 'not a repository', '2026-01-01')
    rejects(map_init.new_dataset, '', ['example-org'], 'example-org/repository-map', '2026-01-01')
    with tempfile.TemporaryDirectory() as tmp:
        path = write_temporary(tmp, data)
        empty = map_build.load_data(path)
        readme = map_build.render_overview(empty, digest_of(empty))
        assert readme.startswith('# Example repository map\n')
        assert 'No relationships are recorded yet.' in readme and 'No repositories are inventoried yet.' in readme
        assert '<details>' not in readme
        check_overview(empty, readme)

        listing = [[{'full_name': 'example-org/beta', 'description': 'Beta tools', 'default_branch': 'main',
                     'archived': False, 'private': False},
                    {'full_name': 'example-org/secret', 'description': 'Private', 'default_branch': 'main',
                     'archived': False, 'private': True}],
                   [{'full_name': 'example-org/alpha', 'description': None, 'default_branch': 'trunk',
                     'archived': True, 'private': False}]]
        added, missing = map_inventory.merge_inventory(empty, 'example-org', listing, '2026-02-01')
        assert added == ['example-org/alpha', 'example-org/beta'] and missing == []
        records = {node['id']: node for node in empty['repositories']}
        assert set(records) == {'example-org/alpha', 'example-org/beta'}
        assert records['example-org/alpha'] == {
            'id': 'example-org/alpha', 'url': 'https://github.com/example-org/alpha',
            'description': map_inventory.UNREVIEWED, 'group': map_inventory.GROUP,
            'branch': 'trunk', 'archived': True}
        assert empty['inventory_observed'] == {'example-org': '2026-02-01', 'example-labs': '2026-01-01'}
        map_init.write_dataset(path, empty)
        inventoried = map_build.load_data(path)
        readme = map_build.render_overview(inventoried, digest_of(inventoried))
        assert 'No relationships are recorded yet.' in readme and 'Repository inventory' in readme
        check_overview(inventoried, readme)
        check_local_views(inventoried, digest_of(inventoried))

        # A refresh keeps reviewed text, updates inventory status, and reports removals.
        records['example-org/beta'].update(description='Reviewed beta description', group='Packaging')
        refreshed = [{'full_name': 'example-org/beta', 'description': 'Changed upstream', 'default_branch': 'develop',
                      'archived': True, 'private': False}]
        added, missing = map_inventory.merge_inventory(empty, 'example-org', refreshed, '2026-03-01')
        assert added == [] and missing == ['example-org/alpha']
        assert records['example-org/beta'] == {
            'id': 'example-org/beta', 'url': 'https://github.com/example-org/beta',
            'description': 'Reviewed beta description', 'group': 'Packaging', 'branch': 'develop', 'archived': True}
        rejects(map_inventory.merge_inventory, empty, 'example-other', refreshed, '2026-03-01')
        rejects(map_inventory.merge_inventory, empty, 'example-labs', refreshed, '2026-03-01')
        rejects(map_inventory.listing_records, {'full_name': 'example-org/beta'})

        # A single-listing inventory record becomes one entry per organisation.
        single = dict(copy.deepcopy(data), inventory_source='https://example.invalid/listing', inventory_observed='2025-12-01')
        map_inventory.merge_inventory(single, 'example-labs', [], '2026-02-01')
        assert single['inventory_observed'] == {'example-org': '2025-12-01', 'example-labs': '2026-02-01'}
        assert set(single['inventory_source']) == {'example-org', 'example-labs'}

        # The command-line tools write the same dataset and refuse to overwrite records.
        cli = Path(tmp) / 'cli.json'
        result = run_tool(TOOLS/'map_init.py', '--name', 'Example', '--organisation', 'example-org',
                          '--organisation', 'example-labs', '--repository', 'example-org/repository-map',
                          '--observed', '2026-01-01', '--data', cli)
        assert result.returncode == 0, result.stderr
        assert json.loads(cli.read_text()) == data
        assert run_tool(TOOLS/'map_init.py', '--name', 'Example', '--organisation', 'Not_Valid',
                        '--repository', 'example-org/repository-map', '--data', Path(tmp)/'invalid.json').returncode == 2
        listing_path = Path(tmp) / 'listing.json'
        listing_path.write_text(json.dumps(listing))
        result = run_tool(TOOLS/'map_inventory.py', '--organisation', 'example-org', '--listing', listing_path,
                          '--observed', '2026-02-01', '--data', cli)
        assert result.returncode == 0 and '2 repositories added' in result.stdout, result.stderr
        assert len(map_build.load_data(cli)['repositories']) == 2
        result = run_tool(TOOLS/'map_init.py', '--name', 'Example', '--organisation', 'example-org',
                          '--repository', 'example-org/repository-map', '--data', cli)
        assert result.returncode == 2 and '--force' in result.stderr
        assert len(map_build.load_data(cli)['repositories']) == 2


def check_live():
    """Validate the map's own dataset and README without assuming any repository exists."""
    data = map_build.load_data(map_build.DATA)
    digest = hashlib.sha256(map_build.DATA.read_bytes()).hexdigest()
    readme = (map_build.ROOT/'README.md').read_text()
    assert readme == map_build.render_overview(data, digest), 'README.md is out of date; run tools/map_build.py'
    check_overview(data, readme)
    check_local_views(data, digest)
    assert not list(map_build.ROOT.glob('maps/*'))
    assert not list(map_build.ROOT.glob('*.html'))
    return data


def check_docstrings():
    """Require a native docstring on every tool function and a pydoc entry for the generator."""
    reference = pydoc.plain(pydoc.render_doc(map_build))
    count = 0
    for source in sorted(TOOLS.glob('*.py')):
        for node in ast.walk(ast.parse(source.read_text())):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                assert ast.get_docstring(node), f'Missing native docstring: {source.name}:{node.name}'
                if source.name == 'map_build.py':
                    assert f'{node.name}(' in reference, f'Missing pydoc entry: {node.name}'
                count += 1
    return count


fixture = check_fixture()
check_source_discovery(fixture)
check_initialisation()
live = check_live()
count = check_docstrings()
print(f'Fixture regression suite passes ({len(fixture["repositories"])} repository views, source discovery, '
      f'initialisation, inventory); live {live["name"]} map: {len(live["repositories"])} repository views and '
      f'{len(live["source_audits"])} source audits valid; {count} native docstrings pass')
