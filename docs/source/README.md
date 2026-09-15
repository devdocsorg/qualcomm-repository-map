# Qualcomm repository map

[Explore the ecosystem map](.generated/OVERVIEW.md), choose a repository, and
follow its nearby views. Relationship tables explain each arrow and link its
source evidence. The generated site works directly from `index.html` without a server.

```{toctree}
:hidden:

.generated/OVERVIEW
contributing/README
```

## Folders

- [.generated/](.generated/OVERVIEW.md) — Contains map views generated from the shared dataset.
- [contributing/](contributing/README.md) — Owns map editing, exports, and generator reference documentation.
- [.templates/](.templates/map-navigation.html) — Supplies the generated browser entry point and map navigation.

## Files

- [README.md](README.md) — Introduces the map and documentation navigation.
- [conf.py](conf.py) — Configures Sphinx, Python reference extraction, and local browsing.
- [Makefile](Makefile) — Owns local and CI setup, generation, and validation commands.
- [requirements.txt](requirements.txt) — Pins the documentation packages.

- [requirements.lock](requirements.lock) — Locks direct and transitive documentation dependencies for reproducible builds.
