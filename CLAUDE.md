# Qualcomm repository map

Read README.md and the contributor guides before changing the map. Keep verified
repository facts and relationships in data/repositories.json. Every relationship
needs a source URL pinned to a revision, its direction, type, and applicability.
Do not infer dependencies from names, shared organisations, or a similar purpose.

Generate the overview and nearby views with tools/map_build.py. Do not edit the
generated Markdown, SVGs, or site by hand. Preserve one source for each fact.
Run the shared Makefile build and validation before committing generated output.
Keep this resource scoped to the Qualcomm ecosystem, independent of an engagement
or release. Keep evidence dates in dataset metadata rather than living guidance.
