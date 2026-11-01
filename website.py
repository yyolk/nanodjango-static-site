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
from nanodjango import Django

# Temporary measure: inject base path for GitHub Pages project sites during static builds.
# Set BASE_PATH=/nanodjango-static-site in the workflow; leave unset for local runs.
base_path = os.environ.get("BASE_PATH")
settings = {}
if base_path:
    settings["FORCE_SCRIPT_NAME"] = base_path

app = Django(EXTRA_APPS=["django_style"], **settings)

app.pages("/", path="pages", context={"site_title": "Nanodjango Static Site"})

if __name__ == "__main__":
    app.invoke(default="run")
