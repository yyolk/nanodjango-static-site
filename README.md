# Nanodjango Static Site — Model-based Blog Branch

This branch illustrates the **model + admin UI + distill_func** approach for dated blog posts, as shown in the original [nanodjango static site builder post](https://nanodjango.dev/blog/2026-10-static-site-builder/).

It coexists with the file-based nanopages content.

## Local development (admin UI)

```bash
git checkout blog-model-admin-distill
uv run website.py
```

Then:

1. Visit http://localhost:8000/admin/
2. Log in (nanodjango creates a superuser on first run; check the terminal for credentials or use the defaults).
3. Create `Post` objects (title, slug, body). The slug is pre-populated from the title.
4. Visit http://localhost:8000/blog/ to see the list and individual posts.

The SQLite database is created locally and can be committed if you want the content to travel with the repo (as suggested in the original post). For a pure static workflow you can treat it as a build artifact and `.gitignore` it, loading data via fixtures instead.

## Build static files

After creating posts in the admin:

```bash
uv run website.py manage distill generate --output-directory=output/ --collectstatic --force
```

This freezes the blog list and detail pages (plus the nanopages content) into the `output/` directory.

## Deployment

Pushes to `main` (not this branch) trigger the GitHub Pages workflow. Merge or cherry-pick if you want this approach on the live site.

**Note:** This branch keeps the same `FORCE_SCRIPT_NAME` / distill monkey-patch as main so absolute links work under the GitHub Pages project path.

Based on https://nanodjango.dev/blog/2026-10-static-site-builder/
