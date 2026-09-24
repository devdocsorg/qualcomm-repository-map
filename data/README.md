# Map dataset

`repositories.json` is the sole maintained source of repository facts and relationships.
The generator validates it before producing any output.
The [canonical specification](https://github.com/devdocsorg/qli2-example-repo/blob/main/SPECIFICATION.md#repository-maps)
owns the map requirements; this page owns the dataset schema and maintenance commands.

## Schema

| Field | Type and meaning |
| --- | --- |
| `schema_version` | Required integer, currently `1`; unsupported versions fail. |
| `scope` | Required string defining the inventory scope and expansion boundary. |
| `inventory_source`, `inventory_observed` | Required source URL and observation date for the repository inventory; these do not date every edge. |
| `coverage` | Required string explaining the limits of relationship review. |
| `repositories` | Required list of unique repository records. |
| Repository `id`, `url` | Required `owner/name` identifier and canonical HTTPS repository URL. |
| Repository `description`, `group` | Required purpose and editorial browsing group; groups do not assert dependencies. |
| Repository `branch` | Default branch string, or `null` if not inventoried; not a build revision. |
| Repository `archived` | Required boolean for inventory status. |
| `relationships` | Required list of directed relationships. |
| Relationship `from`, `to`, `kind` | Required repository IDs and a supported type declared in the generator. Both endpoints must exist. |
| Relationship `local_summary` | Optional short connection verb; overrides the default verb for its relationship type. |
| Relationship `branches` | Optional non-empty list of branch names. Set it when the relationship holds only on those branches of the `from` repository; every diagram adds them to the connection label. |
| Relationship `condition` | Required string describing branch/release applicability, optionality, and indirect paths where relevant. |
| Relationship `via` | Required ordered intermediate repository IDs for an indirect connection; each step must have a recorded direct relationship. |
| `source_audits` | Reviewed repository, source repository, pinned revision, and paths checked for missing build references. |
| Relationship `evidence` | Non-empty list of records with a `url`, 40-character commit `revision`, and `claim` supported by that source. |

No implicit environment settings, URL rewrites, or network requests change the data
at build time. Update inventory metadata when refreshing the organisation listing;
review relationship evidence independently. Do not copy upstream documentation
into descriptions or infer edges from names.
Record only repositories owned by Qualcomm's GitHub organisations (`qualcomm-linux`
and `qualcomm`, listed in `QUALCOMM_ORGS`), and relationships between them. Upstream
projects, board vendors, and tools are not map repositories, even when a Qualcomm
repository builds with them; the generator rejects them and the source audit skips
their references.

## Files

- [README.md](README.md) — Defines the dataset schema and evidence rules.
- [repositories.json](repositories.json) — Owns repository records and reviewed relationships.

## Update the map

Use Python 3.12 or newer. The generator uses only the standard library. From the repository root:

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
remains in the dataset. No separate map pages or HTML copies are generated.

To update a nearby map at the bottom of a recipient root README from a committed
dataset and generator:

```sh
python3 tools/map_build.py --export qualcomm-linux/meta-qcom-3rdparty \
  --readme ../meta-qcom-3rdparty/README.md \
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
revision and dataset digest stay in a source comment.

Review manifests, included build configurations, selected recipes, and build
commands when updating relationships. Record their source revisions and paths in
`source_audits`. `check_sources.py` fetches those pinned snapshots and fails on
unmapped repository URLs; this checks the recorded scope, not every repository in
the inventory. Refresh the audit when those sources change. Review includes and
conditional applicability alongside the URL check. An indirect record needs
source evidence that the current repository actually selects the parent's input.

`check_map.py` checks all nearby views and rejects missing incoming, optional,
build-tool, and indirect connections. It also verifies that newly recorded
neighbours appear without an allowlist. Run both checks before exporting a view.

The nearby map lives only in the recipient README. Sphinx neither reads nor writes
it; no map source page, generated website copy, or intermediate snapshot is needed.
Access to this private repository is required to update the map; exported public
repository links work independently.

Python's native `pydoc` reads the generator's function documentation:

```sh
python3 -m pydoc tools.map_build
```

The validator checks that every named function has a native docstring and appears
in pydoc output. No separate documentation website is maintained for the tools.

[Back to the map](../README.md).
