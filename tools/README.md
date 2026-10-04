# Map generation tools

[Map maintenance, new-map, and README export commands](../data/README.md).

- [map_init.py](map_init.py) writes a new dataset header from the map's name, organisations, and map repository.
- [map_inventory.py](map_inventory.py) merges an organisation's saved GitHub repository listing into the inventory.
- [map_build.py](map_build.py) generates the clustered Mermaid maps in the README and updates nearby maps directly in recipient READMEs.
- [check_sources.py](check_sources.py) checks reviewed build-source references against the dataset.
- [check_map.py](check_map.py) runs the regression suite against the [fixture dataset](fixtures/repositories.json), then validates this map's dataset, README, and nearby views.

The map's name, organisations, and repository come from the dataset; nothing in the
tools names a particular map. The tools use Python's standard library and generate
no HTML or documentation pages.
