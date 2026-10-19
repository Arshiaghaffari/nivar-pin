# Automatic public text mirror

Source: https://abrnivar.ir/ and same-domain public pages in its sitemap.
Checks run every 15 minutes (GitHub scheduling may be delayed).
Manual run: Actions > Sync public website text > Run workflow.
Edit the main website; README.md and pages/*.md are generated.
No private repository, SMTP credential or form submission is read.
On download or validation failure, existing published content is preserved.
Failures appear in the Actions tab and GitHub's normal notification settings.
This mirror does not guarantee ChatGPT Search indexing or ranking.
Monthly health commit avoids a long-inactive public repository schedule.

Last successful check month (UTC): 2026-10
