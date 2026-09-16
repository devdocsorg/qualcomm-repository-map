"""Check audited repository references against the map, using pinned source files."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

import map_build


def references(text: str) -> set[str]:
    """Extract repository URLs from build declarations and executable download commands."""
    text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('#'))
    urls = set(re.findall(r'(?:https?|git)://github\.com/[\w.-]+/[\w.-]+', text))
    urls.update(re.findall(r'https?://git\.yoctoproject\.org/[\w.-]+', text))
    urls.update(re.findall(r'^\s*url:\s*[\'\"]?(https?://[^\s\'\"]+)', text, re.M))
    return {url.replace('git://', 'https://').removesuffix('.git').rstrip('/') for url in urls}


def check(data: dict, audit: dict, checkout: Path) -> None:
    """Fail when a repository referenced by the reviewed source is absent from its map."""
    revision = audit['revision']
    files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', revision, '--', *audit['paths']], cwd=checkout, text=True).splitlines()
    if not files:
        raise ValueError(f"No source files found for {audit['repository']}")
    urls = {node['url'].rstrip('/'): node['id'] for node in data['repositories']}
    neighbours = {edge['to'] for edge in data['relationships'] if edge['from'] == audit['repository'] and edge['kind'] not in map_build.AUTOMATION}
    found = set()
    for file in files:
        if file.endswith(('.md', '.patch')):
            continue
        text = subprocess.check_output(['git', 'show', f'{revision}:{file}'], cwd=checkout, text=True)
        for url in references(text):
            if urls.get(url) == audit['repository']:
                continue
            if url not in urls or urls[url] not in neighbours:
                raise ValueError(f"Unmapped repository reference in {audit['repository']}:{file}: {url}")
            found.add(urls[url])
    print(f"Source audit: {audit['repository']}: {len(files)} files, {len(found)} mapped repository references")


def main() -> None:
    """Use existing checkouts, or fetch the recorded public snapshots for CI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', action='append', default=[], help='Map repository ID=local checkout')
    args = parser.parse_args()
    checkouts = dict(item.split('=', 1) for item in args.checkout)
    data = map_build.load_data(map_build.DATA)
    with tempfile.TemporaryDirectory(prefix='map-source-audit-') as temp:
        for audit in data['source_audits']:
            checkout = Path(checkouts.get(audit['repository'], Path(temp)/map_build.slug(audit['repository'])))
            if audit['repository'] not in checkouts:
                subprocess.run(['git', 'init', '-q', str(checkout)], check=True)
                subprocess.run(['git', '-C', str(checkout), 'fetch', '-q', '--depth=1',
                                f"https://github.com/{audit['source_repository']}.git", audit['revision']], check=True)
            check(data, audit, checkout)


if __name__ == '__main__':
    main()
