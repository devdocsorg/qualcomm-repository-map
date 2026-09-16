# Map maintenance

This private repository contains the Qualcomm repository map, its source data, and
its generation tools. Keep the reader-facing content focused on repository links
and verified relationships. Do not add a generic documentation-site scaffold.

Read data/README.md before editing. Generate the clustered Mermaid README maps from
data/repositories.json with tools/map_build.py. Export nearby Mermaid blocks
directly into recipient root READMEs. Every repository node must have a clickable
link. Do not create map website pages or connect map export to Sphinx. Run
tools/check_map.py before committing generated output.
