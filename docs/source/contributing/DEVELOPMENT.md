# Set up your development environment

Use Git, Make, Python 3.12 or newer, uv, and a browser. Setup needs network access;
the generator and built site do not.

## 1. Prepare the checkout and tools

```sh
git clone https://github.com/devdocsorg/qualcomm-repository-map.git
cd qualcomm-repository-map
git switch -c map/my-change
make -f docs/source/Makefile setup
```

The Makefile pins the Python environment and installs the documentation packages.
It is the shared entry point for local use and CI.

## 2. Edit and build

Edit `data/repositories.json`, following its adjacent schema guide. Preserve the
relationship direction and record the branch/release condition and commit-pinned
source evidence. Add neighbouring upstream repositories when verified connections
cross organisation boundaries.

```sh
make -f docs/source/Makefile html
```

Expected result: a validated dataset, generated overview and nearby views, extracted
Python function reference, and a strict Sphinx build at `docs/site/index.html`.
Open that file directly in a browser, navigate the overview and nearby pages, and
search for a repository name. Repeat after copying `docs/site/` elsewhere with
networking disabled. External source links require network access.

## 3. Export a nearby view

After committing a reviewed dataset and generator, export a view to the target
repository's contributor-selected documentation home:

```sh
python tools/map_build.py --export qualcomm-linux/meta-qcom-3rdparty \
  --destination ../meta-qcom-3rdparty/docs/source/user \
  --revision "$(git rev-parse HEAD)"
```

This writes `REPOSITORY_MAP.md` and `repository-map.svg`. The page records the
central map commit and dataset digest, highlights the current repository, and
links the full map. Include the exported page in the target site's navigation,
rebuild its site, and commit the source snapshot and generated site together.
Update nearby views by rerunning the same export from a reviewed central commit.
Do not edit a relationship independently in the target repository.

## 4. Validate and submit

The build checks invalid/duplicate relationships, missing evidence, neighbour
selection, deterministic output, and Python documentation coverage. Sphinx's native
`autodoc` extension extracts every named function from `tools/map_build.py`,
including internal helpers; `check_map.py` fails if any function lacks a docstring.
The generator reference is derived from those comments rather than handwritten API prose.

Commit the source and regenerated `docs/site/`, then run:

```sh
make -f docs/source/Makefile check
```

CI runs the same command to reject stale output. The initial coverage is explicitly
reported in the map; broadening inventory does not claim all relationships have
been reviewed.

The shared `check` target also opens a copied site with Playwright and networking
disabled. It checks navigation, anchors, resources, and a search-result click.
It uses system Chromium when available; otherwise run
`make -f docs/source/Makefile browser` to install Playwright's user-local browser.
CI installs its browser before invoking the same check target.

Direct documentation dependencies are declared in `docs/source/requirements.txt`;
`docs/source/requirements.lock` also pins their transitive dependencies. After an
intentional tool update, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run setup, and rebuild before committing both source and output.

The setup target recreates the documentation-only `.venv` from the lockfile.
Keep project dependencies and custom tools in their own environments.
