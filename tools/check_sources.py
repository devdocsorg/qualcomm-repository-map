"""Check audited repository references against the map, using pinned source files."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.error
import urllib.request
from functools import cache
from urllib.parse import urlsplit

import map_build


def references(text: str) -> set[str]:
    """Extract repository URLs from build declarations and executable download commands."""
    text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('#'))
    urls = set(re.findall(r'(?:https?|git)://github\.com/[\w.-]+/[\w.-]+', text))
    urls.update('https://github.com/' + repo for repo in
                re.findall(r'https://raw\.githubusercontent\.com/([\w.-]+/[\w.-]+)/', text))
    urls.update(re.findall(r'https?://git\.yoctoproject\.org/[\w.-]+', text))
    urls.update(re.findall(r'^\s*url:\s*[\'\"]?(https?://[^\s\'\"]+)', text, re.M))
    return {url.replace('git://', 'https://').removesuffix('.git').rstrip('/') for url in urls}


@cache
def canonical(url: str) -> str:
    """Follow a GitHub repository's redirects, so a transferred repository resolves to its current owner."""
    request = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'repository-map-source-audit'})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            final = response.url
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return url  # Private or deleted repositories cannot be resolved.
        raise
    return 'https://github.com/' + '/'.join(urlsplit(final).path.strip('/').split('/')[:2])


def check(data: dict, audit: dict, checkout: Path) -> None:
    """Fail when a repository referenced by the reviewed source is absent from its map.

    Only references to repositories owned by the dataset's ``organisations`` count;
    a reference elsewhere on GitHub is first resolved through its redirects, so a
    repository transferred into one of those organisations still counts. Binary
    files are skipped. Files under ``.github/`` may also reference the automation
    the audited repository runs.
    """
    organisations = set(data['organisations'])
    revision = audit['revision']
    for path in audit['paths']:
        present = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', revision, '--', path], cwd=checkout, text=True)
        if not present.strip():
            raise ValueError(f"Missing audited source path in {audit['repository']} at {revision}: {path}")
    files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', revision, '--', *audit['paths']], cwd=checkout, text=True).splitlines()
    if not files:
        raise ValueError(f"No source files found for {audit['repository']}")
    urls = {node['url'].rstrip('/'): node['id'] for node in data['repositories']}
    outgoing = [edge for edge in data['relationships'] if edge['from'] == audit['repository']]
    neighbours = {edge['to'] for edge in outgoing if edge['kind'] not in map_build.AUTOMATION}
    # Workflows may also reference the automation they run.
    workflow_neighbours = neighbours | {edge['to'] for edge in outgoing}
    found = set()
    for file in files:
        if file.endswith(('.md', '.patch')):
            continue
        data_bytes = subprocess.check_output(['git', 'show', f'{revision}:{file}'], cwd=checkout)
        if b'\0' in data_bytes:
            continue  # Binary files hold no build declarations.
        text = data_bytes.decode(errors='replace')
        allowed = workflow_neighbours if file.startswith('.github/') else neighbours
        for url in references(text):
            if urlsplit(url).netloc == 'github.com' and urlsplit(url).path.strip('/').split('/')[0] not in organisations:
                url = canonical(url)  # A repository transferred into a map organisation still counts.
            parts = urlsplit(url)
            if parts.netloc != 'github.com' or parts.path.strip('/').split('/')[0] not in organisations:
                continue  # Only the map organisations' repositories belong in the map.
            if urls.get(url) == audit['repository'] or url == f"https://github.com/{audit.get('source_repository', audit['repository'])}":
                continue
            if url not in urls or urls[url] not in allowed:
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
