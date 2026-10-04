"""Add an organisation's public repositories to the map's inventory.

Reads a GitHub repository listing saved with
``gh api --paginate --slurp "orgs/<organisation>/repos?per_page=100"`` and merges it
into the dataset: new public repositories gain records, existing records keep their
reviewed description and group while their default branch and archived status are
refreshed, and the organisation's inventory source and observation date are updated.
Private repositories are skipped. Recorded repositories missing from the listing are
reported, not removed, because relationships may still cite them.
"""
from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path

import map_build
import map_init

GROUP = 'Other repositories'
UNREVIEWED = 'Repository purpose needs review; open the repository for its maintained documentation.'


def listing_records(listing) -> list[dict]:
    """Flatten a saved GitHub listing into repository objects.

    :param listing: Parsed ``gh api`` output: a list of repositories, or a list of
        pages (lists) of repositories as ``--slurp`` writes it.
    :returns: Repository objects from every page.
    :raises ValueError: If the listing has another shape.
    """
    if not isinstance(listing, list):
        raise ValueError('A repository listing is a JSON list')
    records = []
    for item in listing:
        records.extend(item if isinstance(item, list) else [item])
    if not all(isinstance(item, dict) and 'full_name' in item for item in records):
        raise ValueError('Every listing entry needs a full_name')
    return records


def merge_inventory(data: dict, organisation: str, listing, observed: str) -> tuple[list[str], list[str]]:
    """Merge one organisation's listing into a dataset in place.

    :param data: Dataset with a valid header.
    :param organisation: One of the dataset's organisations.
    :param listing: Parsed ``gh api`` listing for that organisation.
    :param observed: Observation date of the listing, ``YYYY-MM-DD``.
    :returns: Added repository IDs and recorded IDs absent from the listing.
    :raises ValueError: If the organisation is not listed in the dataset or the
        listing holds another owner's repository.
    """
    if organisation not in data['organisations']:
        raise ValueError(f'{organisation} is not one of the map organisations: {data["organisations"]}')
    entries = sorted(listing_records(listing), key=lambda item: item['full_name'])
    for item in entries:
        if item['full_name'].split('/')[0] != organisation:
            raise ValueError(f"Listing for {organisation} contains {item['full_name']}")
    for field, value in (('inventory_source', map_init.inventory_url(organisation)), ('inventory_observed', observed)):
        if not isinstance(data[field], dict):
            # A single-listing record becomes one entry per organisation.
            source = data[field]
            data[field] = {name: map_init.inventory_url(name) if field == 'inventory_source' else source
                           for name in data['organisations']}
        data[field][organisation] = value
    records = {node['id']: node for node in data['repositories']}
    listed, added = set(), []
    for item in entries:
        identifier = item['full_name']
        if item.get('private'):
            continue
        listed.add(identifier)
        branch, archived = item.get('default_branch'), bool(item.get('archived'))
        if identifier in records:
            records[identifier].update(branch=branch, archived=archived)
            continue
        record = {'id': identifier, 'url': f'https://github.com/{identifier}',
                  'description': (item.get('description') or '').strip() or UNREVIEWED,
                  'group': GROUP, 'branch': branch, 'archived': archived}
        data['repositories'].append(record)
        added.append(identifier)
    missing = sorted(identifier for identifier in records
                     if identifier.split('/')[0] == organisation and identifier not in listed)
    map_build.validate_header(data)
    return added, missing


def main() -> None:
    """Merge a saved listing into the dataset from the command line."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--organisation', required=True, help='Map organisation the listing belongs to')
    parser.add_argument('--listing', type=Path, required=True, help='Saved gh api repository listing (JSON)')
    parser.add_argument('--observed', default=datetime.date.today().isoformat(),
                        help='Date the listing was saved (default: today)')
    parser.add_argument('--data', type=Path, default=map_build.DATA, help='Dataset path')
    args = parser.parse_args()
    data = map_build.load_data(args.data)
    try:
        added, missing = merge_inventory(data, args.organisation, json.loads(args.listing.read_text()), args.observed)
    except ValueError as error:
        parser.error(str(error))
    map_init.write_dataset(args.data, data)
    map_build.load_data(args.data)
    print(f'{args.organisation}: {len(added)} repositories added; '
          f"{sum(node['id'].split('/')[0] == args.organisation for node in data['repositories'])} inventoried")
    for identifier in missing:
        print(f'Recorded but absent from the listing: {identifier}')


if __name__ == '__main__':
    main()
