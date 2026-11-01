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

# Base path for GitHub Pages project sites (e.g. /nanodjango-static-site).
# Set BASE_PATH in the workflow; leave unset for local runs (no base tag).
base_path = os.environ.get("BASE_PATH", "")

app = Django(EXTRA_APPS=["django_style"])

# Override base template to inject a <base> tag so absolute links
# (starting with /) resolve under the project path in the browser.
# Distill's internal requests are unaffected.
if base_path:
    app.templates["base.html"] = f"""
{{% extends "django_style/base.html" %}}
{{% block extra_head %}}
  <base href="{base_path}/">
  {{{{ block.super }}}}
{{% endblock %}}
"""

app.pages("/", path="pages", context={{"site_title": "Nanodjango Static Site"}})

if __name__ == "__main__":
    app.invoke(default="run")
