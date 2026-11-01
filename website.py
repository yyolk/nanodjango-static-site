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

app.pages("/", path="pages", context={"site_title": "Nanodjango Static Site"})

if __name__ == "__main__":
    app.invoke(default="run")
