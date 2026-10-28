#!/usr/bin/env python3
"""Build the vetted public portfolio. No private project repositories are read here."""
import json
import shutil
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DIST = ROOT / "dist"
MANIFEST = SITE / "data" / "projects.json"
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".svg"}

def safe_relative(value, prefix):
    if not isinstance(value, str) or not value.startswith(prefix + "/"):
        return False
    path = Path(value)
    return bool(path.parts) and all(p not in ("..", ".", "") for p in path.parts) and "\\" not in value and ":" not in value

def validate():
    projects = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(projects, list):
        raise ValueError("Project data must be a JSON array.")
    seen = set()
    for idx, project in enumerate(projects):
        if not isinstance(project, dict):
            raise ValueError(f"Project {idx}: expected object.")
        for key in ("slug", "title", "summary", "published"):
            if key not in project:
                raise ValueError(f"Project {idx}: missing {key}.")
        slug = project["slug"]
        if not isinstance(slug, str) or not slug or not all(c.isalnum() or c in "-_" for c in slug):
            raise ValueError(f"Project {idx}: invalid slug.")
        if slug in seen:
            raise ValueError(f"Duplicate project slug: {slug}")
        seen.add(slug)
        if project["published"] is not True:
            raise ValueError(f"Project {idx}: unpublished draft records must never be included in public JSON.")
        for key in ("title", "summary"):
            if not isinstance(project[key], str) or not project[key].strip():
                raise ValueError(f"Project {idx}: {key} cannot be blank.")
        if "tags" in project and (not isinstance(project["tags"], list) or any(not isinstance(t, str) for t in project["tags"])):
            raise ValueError(f"Project {idx}: tags must be strings.")
        if project.get("cover"):
            path = project["cover"]
            if not safe_relative(path, "assets") or Path(path).suffix.lower() not in IMAGE_EXT or not (SITE / path).is_file():
                raise ValueError(f"Project {idx}: cover must be an existing asset under site/assets/.")
        if project.get("page"):
            path = project["page"]
            if not safe_relative(path, "projects") or Path(path).suffix.lower() != ".html" or not (SITE / path).is_file():
                raise ValueError(f"Project {idx}: page must be an existing HTML file under site/projects/.")
        if project.get("repository_url"):
            uri = urlsplit(project["repository_url"])
            if uri.scheme != "https" or uri.hostname != "github.com":
                raise ValueError(f"Project {idx}: repository_url must be a public GitHub HTTPS link.")
        if project["published"] and project.get("repository_private", False) and project.get("repository_url"):
            raise ValueError(f"Project {idx}: do not link a private repository.")
    return projects

def main():
    projects = validate()
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for src in SITE.rglob("*"):
        if src.is_symlink():
            raise ValueError("Publishing symlinks is forbidden: " + str(src.relative_to(ROOT)))
        if src.is_file():
            relative = src.relative_to(SITE)
            destination = DIST / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, destination)
    print(f"Built dist/ with {len(projects)} project records.")

if __name__ == "__main__":
    main()
