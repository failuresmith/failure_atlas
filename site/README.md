# Failure Atlas Documentation System

This repository includes a minimal static documentation generator for the atlas.

## Goals

- expose FP/FM/GR/PM artifacts as one navigable structure
- support filtering by failure domain and mechanism
- provide synchronous client-side search with a modal overlay
- keep output fully static for GitHub Pages deployment

## Architecture

- `site/build.py`
  - scans repository markdown artifacts
  - extracts metadata using this priority:
    1. YAML frontmatter
    2. inline metadata lines
    3. filename ID inference
    4. heading/title inference
    5. fallback defaults
  - enriches domain/mechanism + relationships from `failure_index.md` and `taxonomy.md`
  - generates:
    - `docs/index.html`
    - `docs/entries/*.html`
    - `docs/assets/styles.css`
    - `docs/assets/app.js`
    - `docs/search-index.json`
    - `docs/manifest.json`

- `site/templates/*.html`
  - Jinja templates for index and entry pages

- `site/static/*`
  - calm, documentation-first CSS
  - vanilla JS for filtering + modal search

## Local development

From repository root:

```bash
python -m pip install -r site/requirements.txt
python site/build.py
python -m http.server 8000 --directory docs
```

Then open `http://localhost:8000`.

## Rebuild workflow

- Push to `main` triggers `.github/workflows/deploy-pages.yml`
- Workflow installs generator dependencies
- Builds static output into `docs/`
- Publishes `docs/` to GitHub Pages using the official `upload-pages-artifact` + `deploy-pages` actions

## Notes / assumptions

- Incomplete markdown metadata is tolerated; generator falls back to inferred values.
- FM entries are generated from `lab/failure_modes/FM_XXX_*/spec.md` (or `README.md` fallback), with links to directory/spec/results when present.
- AGENTS.md files are intentionally excluded from indexing.