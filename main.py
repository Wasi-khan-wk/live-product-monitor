from Database import load_products, save_products
from Gsheet import write_changed_products
from Scraper import build_product_objects, scrape_board_rows


def find_changed_products(db_products, live_products):
    # Return live products whose values differ from the stored ones (matched by position).
    changed = []
    try:
        for i in range(len(db_products)):
            db_product = db_products[i]
            live_product = live_products[i]

            for column in vars(db_product):
                if getattr(db_product, column) != getattr(live_product, column):
                    changed.append(live_product)
                    break
    except Exception as e:
        print(f"An Exception Occurred in find_changed_products due to {e}")
    return changed


def main():
    db_products = load_products()
    rows_data = scrape_board_rows()
    live_products = build_product_objects(rows_data)

    if not db_products:
        save_products(live_products)
        return

    changed_products = find_changed_products(db_products, live_products)
    if changed_products:
        write_changed_products(changed_products)


if __name__ == "__main__":
    main()