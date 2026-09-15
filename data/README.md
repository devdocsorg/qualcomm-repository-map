# Map dataset

`repositories.json` is the sole maintained source of repository facts and relationships.
The generator validates it before producing any output.

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
| Relationship `condition` | Required string describing branch/release applicability, optionality, and indirect paths where relevant. |
| Relationship `evidence` | Non-empty list of records with a `url`, 40-character commit `revision`, and `claim` supported by that source. |

No implicit environment settings, URL rewrites, or network requests change the data
at build time. Update inventory metadata when refreshing the organisation listing;
review relationship evidence independently. Do not copy upstream documentation
into descriptions or infer edges from names.

## Files

- [README.md](README.md) — Defines the dataset schema and evidence rules.
- [repositories.json](repositories.json) — Owns repository records and reviewed relationships.
