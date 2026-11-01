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
if base_path:
    from django_distill import request as distill_request
    _original_internal = distill_request.internal_wsgi_request

    def _patched_internal_wsgi_request(path, *args, **kwargs):
        if path.startswith(base_path):
            path = path[len(base_path):] or "/"
        return _original_internal(path, *args, **kwargs)

    distill_request.internal_wsgi_request = _patched_internal_wsgi_request

# Model-based blog posts (admin UI + distill_func)
@app.admin(list_display=["title", "created"], prepopulated_fields={"slug": ("title",)})
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return self.title

@app.path("blog/", name="post_list", distill=True)
class PostList(ListView):
    model = Post
    template_name = "blog/post_list.html"

@app.path(
    "blog/<slug:slug>/",
    name="post_detail",
    distill_func=lambda: [(p.slug,) for p in Post.objects.all()],
)
class PostDetail(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

# Inline templates for the model-based blog
app.templates["blog/post_list.html"] = """
{% extends "base.html" %}
{% block content %}
  <h1>Blog</h1>
  <ul>
  {% for post in object_list %}
    <li><a href="{% url 'post_detail' post.slug %}">{{ post.title }}</a> ({{ post.created|date:"j M Y" }})</li>
  {% empty %}
    <li>No posts yet. Create some in the admin.</li>
  {% endfor %}
  </ul>
{% endblock %}
"""

app.templates["blog/post_detail.html"] = """
{% extends "base.html" %}
{% block content %}
  <h1>{{ object.title }}</h1>
  <p><em>{{ object.created|date:"j M Y" }}</em></p>
  {{ object.body|linebreaks }}
  <p><a href="{% url 'post_list' %}">All posts</a></p>
{% endblock %}
"""

# Keep nanopages for the rest of the site
app.pages("/", path="pages", context={"site_title": "Nanodjango Static Site"})

if __name__ == "__main__":
    app.invoke(default="run")
