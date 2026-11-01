# Nanodjango Static Site

A simple static site built with nanodjango, django-nanopages, and django-distill.

Deployed to GitHub Pages via GitHub Actions workflow.

## Local development

```bash
uv run website.py
```

Then visit http://localhost:8000/

## Build static files

```bash
uv run website.py manage distill generate --output-directory=output/ --collectstatic --force
```

## Deployment

Pushes to `main` trigger the workflow which builds the static site and deploys to GitHub Pages.

**Important:** After creating the repo, go to Settings → Pages and set the source to **GitHub Actions**.

Based on https://nanodjango.dev/blog/2026-10-static-site-builder/
