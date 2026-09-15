# Contributing to the Qualcomm repository map

Submit changes to `main` through this repository's pull request template.
Follow the root Code of Conduct and use SECURITY.md for private vulnerability reports.

## Where content belongs

- `data/repositories.json` owns repository identities, editorial browsing groups,
  relationship direction and type, applicability, and source evidence.
- The original repository owns build instructions, API documentation, and policies.
  Link there instead of copying those responsibilities into this map.
- Generated overview and nearby views are derived from the dataset. Correct the
  source and regenerate; do not edit exported diagrams or relationship prose.

## Prepare and review

Follow [development setup](DEVELOPMENT.md). For every relationship change, check
its source at the recorded commit. Prefer manifests, recipes, imports, and CI
configuration over stale prose when describing the current operational connection.
Distinguish required dependencies, optional integrations, indirect relationships,
source packaging, and release-specific relationships.

A repository name or shared organisation does not establish a relationship. Mark
unreviewed coverage plainly. Preserve existing verified facts when reorganising the
map, and update the evidence when a relationship changes.

Use [the PR template](https://github.com/devdocsorg/qualcomm-repository-map/compare?expand=1&template=pr_template.md)
and include validation and affected nearby views. Keep contributions under the
repository licence and retain applicable source notices.
