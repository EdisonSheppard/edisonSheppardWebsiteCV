#!/usr/bin/env python3
"""Conservative pre-publication checks. Not a replacement for manual review.

No secret values are printed to CI logs. Scans the PUBLIC website repository.
A future private-repository pipeline must scan private sources before publishing.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "dist", ".venv", "venv", "__pycache__", ".pytest_cache"}
TEXT_TYPES = {".txt", ".md", ".html", ".htm", ".css", ".js", ".json", ".yml", ".yaml", ".py", ".toml", ".svg", ".xml", ".csv", ".sh"}
PRIVATE_DOCUMENTS = {".docx", ".doc", ".pdf", ".xlsx", ".xls", ".pptx", ".ppt", ".pages"}
MEDIA_TYPES = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"}
MAX_FILE_BYTES = 15 * 1024 * 1024

# Keep recognizable token marker fragments separated to avoid flagging the scan source itself.
TOKEN_PATTERNS = [
    re.compile("gh" + r"[pousr]_[A-Za-z0-9]{25,}"),
    re.compile("github" + r"_pat_[A-Za-z0-9_]{25,}"),
    re.compile("AK" + r"IA[0-9A-Z]{16}"),
    re.compile("sk" + r"-[A-Za-z0-9]{24,}"),
    re.compile(r"(?i)-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
]
ASSIGNMENT = re.compile(r"""(?im)^\s*(?:export\s+)?(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password|passwd)\s*[:=]\s*['"]?([A-Za-z0-9+/_=-]{16,})['"]?\s*(?:#.*)?$""")
EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
SCHOOL_IDENT = re.compile(r"(?i)\b(?:student|candidate)\s*(?:id|number)\s*[:#]\s*[A-Z0-9-]{4,}")
# Not comprehensive: automated document extraction and image metadata stripping come next.

def inspect_text(path, text):
    categories = []
    if any(pattern.search(text) for pattern in TOKEN_PATTERNS) or ASSIGNMENT.search(text):
        categories.append("possible credential or private key")
    if EMAIL.search(text) and path.suffix.lower() not in {".py"}:
        categories.append("email address: review before making public")
    if SCHOOL_IDENT.search(text):
        categories.append("student/candidate identifier")
    return categories

def scan():
    findings = []
    for path in sorted(ROOT.rglob("*")):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if not path.is_file():
            continue
        rel = str(path.relative_to(ROOT))
        if path.is_symlink():
            findings.append((rel, "symlink: not permitted"))
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            findings.append((rel, "large file: requires review"))
            continue
        suffix = path.suffix.lower()
        if suffix in PRIVATE_DOCUMENTS:
            findings.append((rel, "original office/PDF document in public repository: review and remove"))
            continue
        if suffix in TEXT_TYPES or path.name.startswith(".env"):
            text = path.read_text(encoding="utf-8", errors="replace")
            for category in inspect_text(path, text):
                findings.append((rel, category))
        elif suffix in MEDIA_TYPES:
            # Quick metadata signal, not full EXIF parsing. Sanitize before release.
            raw = path.read_bytes()
            if any(marker in raw for marker in (b"GPSLatitude", b"GPSLongitude", b"GPSInfo")):
                findings.append((rel, "possible GPS information in image metadata"))
        elif path.relative_to(ROOT).parts[0] == "site":
            if path.name != ".nojekyll":
                findings.append((rel, "unknown published file type: manual review required"))
    return findings

if __name__ == "__main__":
    findings = scan()
    if findings:
        print("Publication blocked; review these file paths and categories (secret values hidden):")
        for rel, category in findings:
            print(f"  {rel}: {category}")
        sys.exit(1)
    print("Basic public-repository checks passed (not a complete privacy/security audit).")
