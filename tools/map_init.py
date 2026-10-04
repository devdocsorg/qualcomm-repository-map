"""Initialise a repository map's dataset with its name, organisations, and map repository.

Writes a dataset header ready for the inventory step: one inventory source and
observation date per organisation, and empty ``repositories``, ``relationships``,
and ``source_audits`` lists. An existing dataset that already records anything is
only replaced with ``--force``.
"""
from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path

import map_build

COVERAGE = ('Repository inventory is broader than reviewed relationships. An absent edge '
            'means no relationship has been recorded, not proof of independence.')


def inventory_url(organisation: str) -> str:
    """Return the GitHub API listing of an organisation's repositories.

    :param organisation: GitHub organisation name.
    :returns: The listing URL recorded as the organisation's inventory source.

    Example: ``inventory_url('example-org')`` returns
    ``'https://api.github.com/orgs/example-org/repos?per_page=100'``.
    """
    return f'https://api.github.com/orgs/{organisation}/repos?per_page=100'


def default_scope(name: str, organisations: list[str]) -> str:
    """Describe the inventory scope and expansion boundary for a new map.

    :param name: Map name, such as ``Example``.
    :param organisations: GitHub organisations whose repositories the map records.
    :returns: Scope text naming the organisations.
    """
    if len(organisations) > 1:
        listed, pronoun = 'organisations ' + ', '.join(organisations[:-1]) + ' and ' + organisations[-1], 'them'
    else:
        listed, pronoun = 'organisation ' + organisations[0], 'it'
    return (f'{name} repositories: public repositories in the GitHub {listed}. '
            f'Repositories outside {pronoun}, such as upstream projects, vendors, and tools, are not recorded. '
            'The map is not limited to a release or engagement.')


def new_dataset(name: str, organisations: list[str], repository: str,
                observed: str, scope: str | None = None) -> dict:
    """Build a new, empty dataset header.

    :param name: Map name, used in titles such as ``<name> repository map``.
    :param organisations: GitHub organisations whose repositories belong in the map.
    :param repository: ``owner/repo`` of the map repository itself.
    :param observed: Inventory observation date, ``YYYY-MM-DD``.
    :param scope: Scope text; a default naming the organisations when omitted.
    :returns: Dataset that passes ``map_build.load_data`` validation.
    :raises ValueError: If the name, organisations, repository, or date are invalid.
    """
    if not organisations:
        raise ValueError('At least one organisation is required')
    data = {
        'schema_version': 1,
        'name': name,
        'organisations': organisations,
        'map_repository': repository,
        'scope': scope or default_scope(name, organisations),
        'inventory_source': {organisation: inventory_url(organisation) for organisation in organisations},
        'inventory_observed': {organisation: observed for organisation in organisations},
        'coverage': COVERAGE,
        'repositories': [],
        'relationships': [],
        'source_audits': [],
    }
    map_build.validate_header(data)
    return data


def write_dataset(path: Path, data: dict) -> None:
    """Write a dataset in the repository's JSON layout.

    :param path: Dataset path.
    :param data: Dataset to write.
    """
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def main() -> None:
    """Write a new dataset header from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True, help='Map name, as in "<name> repository map"')
    parser.add_argument('--organisation', action='append', required=True,
                        help='GitHub organisation whose repositories belong in the map (repeatable)')
    parser.add_argument('--repository', required=True, help='owner/repo of this map repository')
    parser.add_argument('--observed', default=datetime.date.today().isoformat(),
                        help='Inventory observation date (default: today)')
    parser.add_argument('--scope', help='Scope text (default: names the organisations)')
    parser.add_argument('--data', type=Path, default=map_build.DATA, help='Dataset path')
    parser.add_argument('--force', action='store_true', help='Replace a dataset that already records anything')
    args = parser.parse_args()
    if args.data.exists() and not args.force:
        existing = json.loads(args.data.read_text())
        if any(existing.get(field) for field in ('repositories', 'relationships', 'source_audits')):
            parser.error(f'{args.data} already records repositories, relationships, or audits; pass --force to replace it')
    try:
        data = new_dataset(args.name, args.organisation, args.repository, args.observed, args.scope)
    except ValueError as error:
        parser.error(str(error))
    write_dataset(args.data, data)
    print(f"Initialised the {args.name} repository map for {', '.join(args.organisation)} in {args.data}")


if __name__ == '__main__':
    main()
