# Product Scraper

Scrapes the "A board that changes every minute" table on [magicscraper.app](https://magicscraper.app/) (Sandbox section), stores it in SQL Server, and on later runs writes any changed rows to a Google Sheet.

## How it works

1. Load the stored products from SQL Server.
2. Scrape the live board with Playwright.
3. If the database is empty, insert the scraped rows (first run).
4. Otherwise compare the scraped rows with the stored ones and write the changed rows to the **Product Changes** tab of the Google Sheet.

## Project structure

```
product_scraper/
├── main.py            # entry point and change detection
├── config.py          # all settings (URL, DB, Google Sheet)
├── scraper.py         # Playwright scraping and row parsing
├── database.py        # SQL Server connection, insert and load
├── gsheet.py          # writes changed products to Google Sheets
├── requirements.txt
└── README.md
```

The code also imports `Model_Live_Product` from `Models/model_product.py`, so keep that folder next to these files.

## Requirements

- Python 3.9+
- Google Chrome installed (the scraper launches it through Playwright with `channel="chrome"`)
- ODBC driver "SQL Server Native Client 10.0" (or change `DB_DRIVER` in `config.py`)
- A SQL Server database with this table:

```sql
dbo.tbl_live_product (SKU, PRODUCT, MAKER, PRICE, STOCK, UPDATED)
```

- A Google service account with access to the sheet

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

### Database settings

Defaults live in `config.py`. Override them with environment variables:

| Variable | Meaning |
|---|---|
| `DB_SERVER` | SQL Server host |
| `DB_NAME` | Database name |
| `DB_USER` | Login |
| `DB_PASSWORD` | Password |

### Google Sheets

1. Create a service account in Google Cloud and enable the **Google Sheets API** and **Google Drive API**.
2. Download its key as `credentials.json` and put it in the project folder.
3. Share the spreadsheet with the service account's `client_email` as **Editor**.
4. The sheet needs a tab named `Product Changes` with headers in row 1, a separator row in row 2, and data starting at row 3. The sheet ID and tab name are set in `config.py`.

## Run

```bash
python main.py
```

## Notes

- Each run **replaces** the data in `Product Changes` (row 3 onward). Rows 1 and 2 are never touched.
- Changes are detected by comparing rows by position. If the board's row order or count can change, match by SKU instead.
- Never commit `credentials.json` or real passwords. Add them to `.gitignore`:

```
credentials.json
.env
venv/
__pycache__/
```