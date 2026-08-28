# Steady Payday

**Pa...[truncated]

## Current public scope

- Real straight-on workbook previews
- A free one-page Payday Bill Map PDF
- A free biweekly paycheck bill-calendar guide
- A live $3 Payday Reset Pack checkout on Gumroad
- Truthful product boundaries with no email form, advertising, or personal-data collection on the companion site

The paid workbook is not included in this repository.

## Local preview

```bash
python -m http.server 4173 --directory public
```

Open `http://127.0.0.1:4173/`.

## Rebuild the free PDF

The PDF generator uses ReportLab and Noto fonts available on the build machine:

```bash
python scripts/create_payday_map.py
```

## Responsive QA

`browser_qa.py` expects Chrome with a DevTools endpoint at `127.0.0.1:9222` and the local preview at port 4173. It validates desktop, 390px, and 320px layouts, broken images, empty links, the download route, and horizontal overflow.

## Commercial and legal status

The $3 Payday Reset Pack is live on a verified Gumroad checkout. The Shift Pay & Bill Planner workbook remains a preview and is not sold from this repository. Product planning estimates are not payroll, tax, legal, or financial advice.
