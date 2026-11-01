# Nanodjango Static Site — Model-based Blog Branch

This branch illustrates the **model + admin UI + distill_func** approach for dated blog posts, as shown in the original [nanodjango static site builder post](https://nanodjango.dev/blog/2026-10-static-site-builder/).

It coexists with the file-based nanopages content.

## Local development (admin UI)

```bash
git checkout blog-model-admin-distill
uv run website.py
```

On first run, nanodjango will create a local SQLite database and a superuser (default password is often `password` or prompted).

Then visit:

- http://localhost:8000/ — the site
- http://localhost:8000/admin/ — Django admin (create Posts here)

Create a few posts in the admin. The slug is auto-prepopulated from the title.

## Build static files

After you have posts in the database:

```bash
uv run website.py manage distill generate --output-directory=output/ --collectstatic --force
```

This generates:

- `/blog/` — list of posts from the database
- `/blog/<slug>/` — individual posts

The `distill_func` on the detail view yields the current slugs so distill knows which pages to freeze.

## Notes

- The SQLite database (`db.sqlite3`) holds the post content. It is not committed by default. You can commit it if you want the content to travel with the repo, or treat it as a local/build artifact.
- The same `FORCE_SCRIPT_NAME` / distill monkey-patch as `main` is present so absolute links work under a GitHub Pages project path.
- File-based pages under `pages/` continue to work via nanopages.

## Deployment

Pushes to `main` (not this branch) trigger the GitHub Pages workflow. This branch is for illustration and local experimentation.

Based on https://nanodjango.dev/blog/2026-10-static-site-builder/
