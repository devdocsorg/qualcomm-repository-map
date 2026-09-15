# Map tools

Run the shared documentation Makefile from the repository root. The generator
reads the dataset and writes derived map pages; validation rejects malformed
relationships and missing Python function documentation.

## Files

- [README.md](README.md) — Introduces the generator and validation tools.
- [map_build.py](map_build.py) — Generates the ecosystem overview, nearby diagrams, and revisioned exports.
- [check_map.py](check_map.py) — Checks relationship validation, neighbour selection, deterministic rendering, and native documentation coverage.
