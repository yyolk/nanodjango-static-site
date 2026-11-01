# /// script
# dependencies = [
#   "nanodjango",
#   "django-style",
#   "django-nanopages",
#   "django-browser-reload",
#   "django-distill",
# ]
# ///
#
# Run locally:
#    uv run website.py
#
# Build static site:
#    uv run website.py manage distill generate --output-directory=output/ --collectstatic --force
#
from nanodjango import Django

app = Django(
    EXTRA_APPS=["django_style"],
)

# Register django-nanopages to serve markdown/HTML from pages/
app.pages("/", path="pages", context={"site_title": "Nanodjango Static Site"})

if __name__ == "__main__":
    app.invoke(default="run")
