# Publishing and privacy rules

This site repository is public and its entire Git history is public. Deleting a file in a later commit does not reliably remove it from history.

## Before committing to ANY public repository

- Do not upload passwords, authentication cookies, private keys, tokens, .env files or recovery codes.
- Remove private home/school addresses, personal phone numbers, student IDs, other people's personal details and non-public information.
- Check embedded document contents, comments, revisions, hidden text, tables, document properties and images.
- Remove GPS coordinates and camera/device metadata from photographs before publishing.
- Confirm you have permission to publish images, drawings, documents and information from others.
- Keep raw school reports, spreadsheets and private project material in private project repositories. Publish summaries, not raw reports.

## Safety gates in this repository

1. tools/check_publish.py checks recognizable credential patterns, email addresses, student identifiers, raw office/PDF files and a limited subset of GPS image metadata indicators.
2. tools/build.py checks publication data fields and asset paths, then copies ONLY the site/ directory to dist/.
3. GitHub Pages deploys only the vetted dist/ artifact.

The scanner is **not comprehensive**. It does not identify every private fact or hidden document property, image EXIF variant, face or licensing concern. It cannot protect files already committed to a public GitHub repository. For private project materials, perform a full analysis BEFORE copying or committing any generated public content.

## Handling findings

- Obvious unnecessary source material should be excluded from website output. Do not silently delete originals.
- A questionable decision must block publication and create a review task in the existing GPT Todoist project once that integration exists.
- Tasks must state a file path, issue category and safe suggested fix, but must not reproduce passwords or sensitive personal data.
- Avoid duplicate tasks for the same unresolved issue.
- If a key was ever published, revoke/rotate it. Removing it from the current file is not sufficient; assess public Git history exposure.

## Never commit these

.env, secrets, PATs, API keys, private school reports and the credentials required to access private project repositories. Configure credentials using GitHub Actions secrets when the future import workflow is implemented.
