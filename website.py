# /// script
# dependencies = [
#   "nanodjango",
#   "django-style",
#   "django-nanopages",
#   "django-browser-reload",
#   "django-distill",
# ]
# ///

import os
from django.db import models
from django.views.generic import ListView, DetailView
from nanodjango import Django

# Base path for GitHub Pages project sites.
# Set BASE_PATH in the workflow only.
base_path = os.environ.get("BASE_PATH", "")

settings = {}
if base_path:
    settings["FORCE_SCRIPT_NAME"] = base_path

app = Django(EXTRA_APPS=["django_style"], **settings)

# Monkeypatch distill's internal request so it doesn't double-prefix.
# reverse() / {% url %} will still emit the prefixed absolute links,
# but the internal WSGI request path is stripped of the base path.
if base_path:
    from django_distill import request as distill_request
    _original_internal = distill_request.internal_wsgi_request

    def _patched_internal_wsgi_request(path, *args, **kwargs):
        if path.startswith(base_path):
            path = path[len(base_path):] or "/"
        return _original_internal(path, *args, **kwargs)

    distill_request.internal_wsgi_request = _patched_internal_wsgi_request

# ---------------------------------------------------------------------------
# Model-based dated blog posts (admin UI + distill_func)
# ---------------------------------------------------------------------------
# This is the approach from the original nanodjango static-site blog post.
# Posts are created via the Django admin (uv run website.py, then /admin/).
# The SQLite database holds the content; distill freezes the pages to HTML.
# (On main the blog is pure Markdown under pages/blog/ instead.)

@app.admin(list_display=["title", "created"], prepopulated_fields={"slug": ("title",)})
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ["-created"]

@app.path("blog/", name="post_list", distill=True)
class PostList(ListView):
    model = Post

@app.path(
    "blog/<slug:slug>/",
    name="post_detail",
    distill_func=lambda: list(Post.objects.values_list("slug", flat=True)),
)
class PostDetail(DetailView):
    model = Post

# Markdown pages (nanopages) — still available alongside the model blog
app.pages("/", path="pages", context={"site_title": "Nanodjango Static Site"})

if __name__ == "__main__":
    app.invoke(default="run")
