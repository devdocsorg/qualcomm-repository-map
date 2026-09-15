# SPDX-License-Identifier: BSD-3-Clause
"""Configure the map's Markdown site for hosted and direct-file browsing."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

# Optional string; default 'Project name not set'.
project = "Qualcomm repository map"
# Optional list; default []. Render Markdown with MyST.
extensions = ["myst_parser", "sphinx.ext.autodoc"]
# Optional string; default 'index'. README owns the homepage content.
root_doc = "README"
# Optional integer; default 0. Preserve links to Markdown headings.
myst_heading_anchors = 4
# Optional boolean; default False. Reject unresolved cross-references.
nitpicky = True
# Optional list; default []. Do not parse build templates as documentation.
exclude_patterns = [".templates/**"]
# Optional list; default []. Resolve the additional HTML template locally.
templates_path = [".templates"]
# Optional mapping; default {}. Generate an entry point without a second source index.
html_additional_pages = {"index": "index.html"}
# Optional boolean; default True. Avoid fetch() of local files for search excerpts.
html_show_search_summary = False

# Optional mapping; theme defaults to 940px. Give diagrams and evidence tables room.
html_theme_options = {"page_width": "1280px", "sidebar_width": "220px"}

# Optional mapping; replace the full inventory sidebar with focused navigation.
html_sidebars = {"**": ["about.html", "searchfield.html", "map-navigation.html"]}

# Optional list; no local reference is defined for this external standard-library type.
nitpick_ignore = [("py:class", "pathlib.Path")]
