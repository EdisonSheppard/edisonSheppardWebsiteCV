# Project ingestion format

## Private project repository convention

Create a *private* repository per project when raw supporting material is not intended for the public.

    Project-Name/
    └── Portfolio/
        ├── README.md
        ├── project.yml
        ├── images/
        │   └── cover.jpg
        └── supporting/
            ├── School-Engineering-Report.docx
            ├── test-results.xlsx
            └── drawings.pdf

- The README provides background, explanations and constraints.
- The YAML file provides hints; it is NOT treated as permission to publish every source.
- Images can be extracted from DOCX or supporting files during a later AI-assisted import.
- Files in supporting/ must never be directly copied into the website by default.

Suggested minimal project.yml:

    title: "RC Car"
    summary: "Mechanical design and construction of a custom RC car"
    status: "Completed"
    category: "Mechanical Engineering"
    tags: ["CAD", "3D Printing", "Electronics"]
    visibility: "review-required"

## Public website format

The website reads ONLY reviewed records from site/data/projects.json. Example:

    [
      {
        "slug": "rc-car",
        "title": "RC Car",
        "summary": "An approved, factual project summary.",
        "category": "Mechanical Engineering",
        "status": "Completed",
        "tags": ["CAD", "3D Printing"],
        "published": true,
        "cover": "assets/rc-car/cover.webp",
        "cover_alt": "RC car chassis on a workbench",
        "page": "projects/rc-car.html"
      }
    ]

Fields cover and page are optional. Referenced files must exist under site/assets/ or site/projects/, respectively. repository_url can be supplied ONLY when the destination repository is intended to be publicly accessible.

Until an AI review/import pipeline is connected, add records and derived content via a reviewed pull request. Never put confidential source documents in site/ or commit them to this public website repo.

## Planned import automation (not yet enabled)

1. Authenticate with a fine-grained, read-only credential or GitHub App installation that can read only the explicitly approved private project repositories.
2. Inspect README, YAML, images and supported source documents, including embedded DOCX images and relevant tables.
3. Detect sensitive content BEFORE drafting public output. Do not copy originals, comments, revision history, image EXIF, usernames, student numbers or hidden metadata.
4. Prepare source-grounded, concise engineering explanations and selected images. Capture confidence, citations/source paths and provenance privately, not on the public page.
5. Open a website pull request showing exact proposed public changes. Require review where facts, redactions or legal rights are uncertain.
6. Merge approved changes; the Pages workflow validates and deploys the vetted site.
7. Send unresolved manual issues to the existing GPT Todoist project, with paths/categories but no secret values; deduplicate.

Do not activate unattended AI publishing or advertise it as running until the importer, credentials, privacy handling and notification integration are actually configured and tested.
