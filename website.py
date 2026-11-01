# /// script
# dependencies = [
#   "nanodjango",
#   "django-style",
#   "django-nanopages",
#   "django-browser-reload",
#   "django-distill",
# ]
# ///

from nanodjango import Django

app = Django(EXTRA_APPS=["django_style"])

app.pages("/", path="pages", context={"site_title": "Nanodjango Static Site"})

if __name__ == "__main__":
    app.invoke(default="run")
