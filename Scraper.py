import config
from Models.model_product import Model_Live_Product


def scrape_board_rows():
    rows_data = []
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, channel="chrome")
            page = browser.new_page()

            page.goto(config.SITE_URL)
            page.wait_for_timeout(2)
            page.click(config.SANDBOX_LINK_XPATH)
            page.wait_for_timeout(2)
            page.click(config.BOARD_LINK_XPATH)
            page.wait_for_timeout(5)

            rows = page.locator(config.TABLE_ROWS_XPATH)

            for row_index in range(rows.count()):
                print(f"Row Index : {row_index + 1}")
                cells = rows.nth(row_index).locator("td")
                rows_data.append(cells.all_inner_texts())

            print("Data Loaded Successfully !")
    except Exception as e:
        print(f"An Exception Occurred in scrape_board_rows due to {e}")
    return rows_data


def build_product_objects(rows_data):
    products = []
    try:
        for row_number, row in enumerate(rows_data, start=1):
            if len(row) != config.EXPECTED_COLUMNS:
                print(f"skipping {row_number} Row due to incomplete data")
                continue

            product = Model_Live_Product()
            product.SKU = row[0]
            product.PRODUCT = row[1]
            product.MAKER = row[2]
            product.PRICE = row[3]
            product.STOCK = row[4]
            product.UPDATED = row[5]
            products.append(product)
    except Exception as e:
        print(f"An Exception Occurred in build_product_objects due to {e}")
    return products