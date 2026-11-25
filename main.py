from Database import load_products, save_products
from Gsheet import write_changed_products
from Scraper import build_product_objects, scrape_board_rows


def find_changed_products(db_products, live_products):
    # Return live products whose values differ from the stored ones (matched by position).
    changed = []
    try:
        db_data_dict = {db_obj.SKU:vars(db_obj) for db_obj in db_products}
        instance_data_dict = {instance_obj.SKU:vars(instance_obj) for instance_obj in live_products}

        for sku, instance_row in instance_data_dict.items():
            if sku not in db_data_dict:
                changed.append(instance_row)
                continue

            db_row = db_data_dict.get(sku, {})
            for column_name, column_value in instance_row.items():
                if db_row.get(column_name, "") != column_value:
                    changed.append(instance_row)
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