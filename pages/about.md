---
title: About
---

# About This Site

This site was generated as a demonstration of using Django as a simple static site builder.

### How it works

1. Content lives in `pages/` as Markdown or HTML files with optional frontmatter.
2. `website.py` registers the pages directory with nanodjango.
3. `django-distill` generates static files to the `output/` directory.
4. GitHub Actions builds and deploys the output to GitHub Pages.

You can run it locally with:

```bash
uv run website.py
```

Or build statically:

```bash
uv run website.py manage distill generate --output-directory=output/ --collectstatic --force
```

Based on the example from the [nanodjango blog](https://nanodjango.dev/blog/2026-10-static-site-builder/).
