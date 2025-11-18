## Repo snapshot

This repository is a small Jekyll-based static site that catalogs MQSS components.
- Key files/directories:
  - `_config.yml` — declares a `components` collection.
  - `_components/*.md` — component pages (Jekyll collection). Each file uses YAML frontmatter with keys like `title`, `languages`, `frameworks`, `links` (e.g. `links.github`, `links.docs`), and `maintainers`.
  - `_layouts/default.html` — page template that iterates `site.components` and renders fields and `component.content`.
  - `assets/js/github-stars.js` — client-side fetch of GitHub API to display repo star counts. Expects `links.github` to point to `https://github.com/owner/repo`.
  - `assets/css/style.css` — styles; component grid is controlled by `.component-grid` (currently `grid-template-columns: repeat(3, 1fr)`).
  - `_site/` — generated site output.

## Big picture for an AI coding agent

- This is a content-first static site (Jekyll). Changes are source edits (Markdown, Liquid templates, CSS, JS) and then site is generated into `_site`.
- Main data model: each component is a Markdown file in `_components/` whose YAML frontmatter supplies structured metadata. The Liquid templates expect arrays for `languages` and `frameworks`, and nested `links` with `github` (used by `github-stars.js`).
- Common tasks the agent will perform:
  - Add or update a component: create/modify `_components/<name>.md` with frontmatter and body content.
  - Tweak presentation: edit `_layouts/default.html` or `assets/css/style.css`.
  - Fix GitHub star fetching: update `assets/js/github-stars.js` (watch for rate limits/CORS and the exact `links.github` format).

## Project-specific conventions and examples

- Frontmatter example (use this when adding components):

```yaml
---
title: "Example Component"
languages: ["python"]
frameworks: ["qiskit"]
links:
  docs: "https://example.org/docs"
  github: "https://github.com/owner/repo"
maintainers: ["TUM (CDA)"]
---

Short descriptive content here.
```

- Template expectations:
  - `_layouts/default.html` loops `site.components` and references `component.links.github`, `component.links.docs`, `component.maintainers`, `component.languages`, `component.frameworks` and `component.content`.
  - Keep `links.github` in `https://github.com/owner/repo` format so `assets/js/github-stars.js` can extract owner/repo.

## Build / preview / debug

- This repo is configured for Jekyll (see `_config.yml`). Typical local preview commands (depending on your environment):
  - `jekyll build` -> outputs to `_site/`
  - `jekyll serve --livereload` -> serve locally and watch for changes

If the project uses Bundler, prefix with `bundle exec` (e.g. `bundle exec jekyll serve`). If you're unsure, try `jekyll --version` and fall back to `bundle exec jekyll` when Gemfile/Bundler is present.

## Integration points & gotchas

- GitHub stars are fetched client-side from the public GitHub API. This works without auth but is subject to strict rate limits (60 requests/hour per IP). When previewing lots of components, consider mocking or caching results.
- The Liquid `relative_url` filter is used throughout; generate the site with Jekyll so links resolve correctly.

## When changing design or layout

- Update `assets/css/style.css` for visual changes; `.component-grid` governs the column count. Keep mobile/responsive considerations in mind.
- If you change the frontmatter shape (rename keys), update `_layouts/default.html` accordingly and search all `_components` for compatibility.

## Files to inspect for more context

- `_config.yml`, `_layouts/default.html`, `_components/*.md`, `assets/js/github-stars.js`, `assets/css/style.css`, `_site/` (built output).

---
If anything above is unclear or you'd like me to include a short checklist for adding a new component (validation steps, quick linting), tell me which part to expand and I'll update this file.
