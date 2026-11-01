import os

SITE_URL = "https://magicscraper.app/"
SANDBOX_LINK_XPATH = "//a[contains(text(),'Sandbox')]"
BOARD_LINK_XPATH = "//a[contains(text(),'A board that changes every minute')]"
TABLE_ROWS_XPATH = "//tbody/tr"
EXPECTED_COLUMNS = 6

# DB
DB_SERVER = os.getenv("DB_SERVER", "wasi")
DB_NAME = os.getenv("DB_NAME", "UniversityDB")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD") # Put DB Password here
DB_DRIVER = "{SQL Server Native Client 10.0}"
DB_TABLE = "dbo.tbl_live_product"

# G Sheet
GSHEET_ID = "1o3aoVe4jGKJ2obTGBF9J1OvbVYHuQWdaLGaB1r1g48o"
GSHEET_TAB_NAME = "Product Changes"
GSHEET_CREDENTIALS_FILE = "credentials.json"
GSHEET_SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive",]
GSHEET_FIRST_DATA_ROW = 3