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

# Monkeypatch distill so FORCE_SCRIPT_NAME works for absolute links
# without double-prefixing the internal requests or the output file paths.
# reverse() / {% url %} still emit the prefixed absolute links in the HTML.
if base_path:
    from django_distill import request as distill_request

    _original_internal = distill_request.internal_wsgi_request
    _original_generate_filename = distill_request.generate_filename

    def _patched_internal_wsgi_request(path, *args, **kwargs):
        if path.startswith(base_path):
            path = path[len(base_path):] or "/"
        return _original_internal(path, *args, **kwargs)

    def _patched_generate_filename(distill_file, uri, param_set):
        filename = _original_generate_filename(distill_file, uri, param_set)
        # Strip the base path from the output file path so files land in
        # output/blog/ not output/nanodjango-static-site/blog/
        if filename.startswith(base_path.lstrip("/")):
            filename = filename[len(base_path.lstrip("/")):].lstrip("/")
        elif filename.startswith(base_path):
            filename = filename[len(base_path):].lstrip("/")
        return filename or "index.html"

    distill_request.internal_wsgi_request = _patched_internal_wsgi_request
    distill_request.generate_filename = _patched_generate_filename

app.pages("/", path="pages", context={"site_title": "Nanodjango Static Site"})

if __name__ == "__main__":
    app.invoke(default="run")
