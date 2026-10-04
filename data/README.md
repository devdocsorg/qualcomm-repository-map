# Map dataset

`repositories.json` is the sole maintained source of the map's identity, repository
facts, and relationships. The generator validates it before producing any output.
This page owns the dataset schema and the maintenance commands.

## Schema

| Field | Type and meaning |
| --- | --- |
| `schema_version` | Required integer, currently `1`; unsupported versions fail. |
| `name` | Required map name. Titles read “`<name>` repository map”, and every nearby map links to the “Full `<name>` repository map”. |
| `organisations` | Required non-empty list of the GitHub organisations whose repositories belong in the map. |
| `map_repository` | Required `owner/repo` of this map repository; nearby maps link to it and record it as their source. |
| `scope` | Required string defining the inventory scope and expansion boundary. |
| `inventory_source`, `inventory_observed` | Required repository listing URL and observation date (`YYYY-MM-DD`) for the inventory: objects with one entry per organisation, or one string each for a map inventoried from a single listing. These do not date every edge. |
| `coverage` | Required string explaining the limits of relationship review. |
| `repositories` | Required list of unique repository records. |
| Repository `id`, `url` | Required `owner/name` identifier, owned by one of the `organisations`, and canonical HTTPS repository URL. |
| Repository `description`, `group` | Required purpose and editorial browsing group; groups do not assert dependencies. |
| Repository `branch` | Default branch string, or `null` if not inventoried; not a build revision. |
| Repository `archived` | Required boolean for inventory status. |
| `relationships` | Required list of directed relationships. |
| Relationship `from`, `to`, `kind` | Required repository IDs and a supported type declared in the generator. Both endpoints must exist. |
| Relationship `local_summary` | Optional short connection verb; overrides the default verb for its relationship type. |
| Relationship `branches` | Optional non-empty list of branch names. Set it only when the relationship does not hold on the `from` repository's default branch, naming the maintained branches where it does; every diagram adds them to the connection label. Relationships on the default branch carry no `branches`. Trial or staging branches are not mapped. |
| Relationship `condition` | Required string describing branch/release applicability, optionality, and indirect paths where relevant. |
| Relationship `via` | Required ordered intermediate repository IDs for an indirect connection; each step must have a recorded direct relationship. |
| Relationship `evidence` | Non-empty list of records with a `url`, 40-character commit `revision`, and `claim` supported by that source. |
| `source_audits` | Required list of reviewed sources. Each records a mapped `repository`, the `source_repository` it was read from, a 40-character commit `revision`, and a non-empty list of `paths` checked for missing build references. |

No implicit environment settings, URL rewrites, or network requests change the data
at build time. Update inventory metadata when refreshing an organisation's listing;
review relationship evidence independently. Do not copy upstream documentation
into descriptions or infer edges from names.
Record only repositories owned by the organisations listed in the data, and
relationships between them. Upstream projects, vendors, and tools are not map
repositories, even when a mapped repository builds with them; the generator rejects
them and the source audit skips their references.

## Files

- [README.md](README.md) — Defines the dataset schema and evidence rules.
- [repositories.json](repositories.json) — Owns the map's identity, repository records, and reviewed relationships.

## Create a new map

A new map starts from the repository-map template, so its tools, checks, CI, and
this guide arrive together. Use Python 3.12 or newer; the tools use only the
standard library. Replace the placeholders in angle brackets.

1. Create the map repository from the template and clone it:

   ```sh
   gh repo create <owner>/<map-repository> --private \
     --template <template-owner>/<template-repository> --clone
   cd <map-repository>
   ```

2. Initialise the dataset with the map's name, every organisation whose
   repositories belong in it, and the map repository itself. This writes a new
   header, records each organisation's inventory source and date, and leaves
   `repositories`, `relationships`, and `source_audits` empty:

   ```sh
   python3 tools/map_init.py --name "<Name>" \
     --organisation <organisation> [--organisation <organisation> ...] \
     --repository <owner>/<map-repository>
   ```

   `--scope` replaces the default scope text. The command refuses to replace a
   dataset that already records anything unless given `--force`.

3. Inventory each organisation's repositories. Save the organisation's listing
   with the GitHub CLI and merge it:

   ```sh
   gh api --paginate --slurp "orgs/<organisation>/repos?per_page=100" > /tmp/<organisation>.json
   python3 tools/map_inventory.py --organisation <organisation> --listing /tmp/<organisation>.json
   ```

   New public repositories gain records with their GitHub description (or a
   needs-review placeholder), default branch, and archived status, in the
   `Other repositories` group. Private repositories are skipped. Review the new
   records' descriptions and groups before committing.

4. Build and check:

   ```sh
   python3 tools/map_build.py
   python3 tools/check_map.py
   python3 tools/check_sources.py
   ```

5. Commit the dataset and the generated README together and push.

Relationships are then added as each repository is reviewed, following the next
section.

## Update the map

From the repository root:

```sh
python3 tools/map_build.py
python3 tools/check_map.py
python3 tools/check_sources.py
```

Edit the dataset and regenerate; commit the dataset and README together. The root
README contains smaller Mermaid maps grouped by relationship purpose and repository
area, with clickable repository nodes. Large clusters split into numbered parts
with at most 24 nodes each. Shared providers can appear in several maps, while
shared path steps are drawn once within each diagram. Repositories without recorded relationships stay
in the inventory. Expandable sections preserve inventory, applicability, and source evidence.
Standalone automation diagrams and their corresponding text are omitted;
automation connections in mixed component diagrams remain. All records stay in
the dataset. Evidence links use source filenames as their labels; claim text
remains in the dataset. No separate map pages or HTML copies are generated. A map
with no relationships yet says so in place of the diagrams.

Refresh an organisation's inventory by saving a new listing and running
`tools/map_inventory.py` again. Existing records keep their reviewed description
and group; their default branch and archived status are updated. Recorded
repositories missing from the listing are reported for review, not removed.

To update a nearby map at the bottom of a recipient root README from a committed
dataset and generator:

```sh
python3 tools/map_build.py --export <owner>/<repository> \
  --readme ../<repository>/README.md \
  --revision "$(git rev-parse HEAD)"
```

The exporter replaces only the final `repository-map:start` / `repository-map:end`
block, or appends one when no markers exist. It preserves all other README content
and refuses an ambiguous marker pair or content after the map. Add `--check` to
verify an existing export without modifying it. Reproduce the export by checking
out the revision recorded in the block and running the same command.

The nearby Mermaid map covers every recorded build/component connection touching
the current repository in either direction, including optional integrations and
verified indirect paths. Indirect connections follow their recorded intermediates;
do not draw a redundant shortcut. Use short connection verbs, not labels such as
“required” alone. Split large views without dropping connections. The source
revision and dataset digest stay in a source comment, and the map's `name` and
`map_repository` form its link to the full map.

Review manifests, included build configurations, selected recipes, and build
commands when updating relationships. Record their source revisions and paths in
`source_audits`. `check_sources.py` fetches those pinned snapshots and fails on
unmapped references to repositories owned by the organisations listed in the data;
this checks the recorded scope, not every repository in the inventory. A reference
to a repository elsewhere on GitHub is resolved through its redirects first, so a
repository transferred into one of the organisations still counts. Binary files are
skipped, and workflow files under `.github/` may also reference the automation the
repository runs. Refresh the audit when those sources change. Review includes and
conditional applicability alongside the URL check. An indirect record needs
source evidence that the current repository actually selects the parent's input.

`check_map.py` runs its regression suite against a fictional fixture dataset
(`tools/fixtures/repositories.json`), so it holds for any map: it rejects missing
incoming, optional, build-tool, and indirect connections, verifies that newly
recorded neighbours appear without an allowlist, and covers branch labels, map-size
splits, evidence rules, export provenance, out-of-organisation rejection, source
discovery, initialisation, and inventory merging. It then validates this map's own
dataset: it loads, the README matches the generator's output, and every nearby view
is complete. An empty dataset passes. Run both checks before exporting a view.

The nearby map lives only in the recipient README. Sphinx neither reads nor writes
it; no map source page, generated website copy, or intermediate snapshot is needed.
Access to the map repository is required to update the map; exported repository
links work independently.

Python's native `pydoc` reads the generator's function documentation:

```sh
python3 -m pydoc tools.map_build
```

The validator checks that every named function has a native docstring and appears
in pydoc output. No separate documentation website is maintained for the tools.

[Back to the map](../README.md).
