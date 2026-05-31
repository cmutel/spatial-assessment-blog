# Spatial Assessment Blog

Source for [chris.mutel.org](https://chris.mutel.org) — a Pelican static site about life cycle assessment and Brightway.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

| Command | Description |
|---|---|
| `make html` | Build the site into `output/` |
| `make devserver` | Build, serve, and auto-reload on changes |
| `make serve` | Serve the existing `output/` at http://localhost:8000 |
| `make publish` | Build with production settings |
| `make github` | Deploy to GitHub Pages |

## Writing posts

Content lives in `content/<year>/` as `.rst` files. Math is rendered with MathJax 3 via the local `plugins/render_math` plugin. Use the RST `.. math::` directive for display math and `:math:` for inline.

Display math example:

```rst
.. math::

    h = CB \cdot \text{diag}(A^{-1}f)
```

MathJax extensions (e.g. `color`, `physics`) can be enabled in `pelicanconf.py`:

```python
MATH_JAX = {
    'tex_extensions': ['color', 'physics'],
}
```
