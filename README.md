# Steady Payday

Public trust and discovery site for the Shift Pay & Bill Planner.

## Current public scope

- Real straight-on workbook previews
- A free one-page Payday Bill Map PDF
- Truthful product boundaries and prelaunch status
- No account, checkout, email form, advertising, or personal-data collection

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

The site is informational until a legitimate zero-upfront-cost checkout, payout path, and support/refund policy are verified. Product planning estimates are not payroll, tax, legal, or financial advice.
