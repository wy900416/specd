"""specd — a spec graph toolkit.

Specs are Markdown files with YAML front-matter. The CLI validates them,
builds a graph index, packs a bounded context for an agent, manages
proposal/release lifecycles, and renders a static viewer.

The package deliberately depends only on PyYAML so it can run anywhere
Python 3.11 runs.
"""

__version__ = "0.1.0"
