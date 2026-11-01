import config


def write_changed_products(changed_products):
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        credentials = Credentials.from_service_account_file(
            config.GSHEET_CREDENTIALS_FILE, scopes=config.GSHEET_SCOPES
        )
        client = gspread.authorize(credentials)
        worksheet = client.open_by_key(config.GSHEET_ID).worksheet(config.GSHEET_TAB_NAME)

        first_row = config.GSHEET_FIRST_DATA_ROW

        # Clear old data only (header rows stay untouched), without deleting rows
        worksheet.batch_clear([f"A{first_row}:F{worksheet.row_count}"])
        print(f"Cleared old data in {config.GSHEET_TAB_NAME}")

        if not changed_products:
            print("No changed products to write.")
            return

        values = [
            [p.SKU, p.PRODUCT, p.MAKER, p.PRICE, p.STOCK, p.UPDATED]
            for p in changed_products
        ]
        last_row = first_row + len(values) - 1

        worksheet.update(range_name=f"A{first_row}:F{last_row}", values=values)
        print(f"{len(values)} changed products inserted successfully!")
    except Exception as e:
        print(f"An Exception Occurred in write_changed_products due to {e}")