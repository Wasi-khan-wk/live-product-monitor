import pyodbc

import config
from Models.model_product import Model_Live_Product


def get_connection():
    conn_str = (
        f"DRIVER={config.DB_DRIVER};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_NAME};"
        f"UID={config.DB_USER};"
        f"PWD={config.DB_PASSWORD};")
    try:
        conn = pyodbc.connect(conn_str)
        print("Connected successfully.")
        return conn
    except pyodbc.Error as e:
        print(f"Connection failed: {e}")
        return None


def insert_products(conn, products):
    if conn is None:
        print("No connection available.")
        return False

    if not products:
        print("No products to insert.")
        return True

    insert_query = f""" INSERT INTO {config.DB_TABLE} (SKU, PRODUCT, MAKER, PRICE, STOCK, UPDATED) VALUES (?, ?, ?, ?, ?, ?) """

    cursor = None
    try:
        cursor = conn.cursor()
        rows = [
            (
                p.SKU,
                p.PRODUCT,
                p.MAKER,
                p.PRICE.replace("$", ""),
                p.STOCK,
                p.UPDATED,
            )
            for p in products
        ]
        cursor.executemany(insert_query, rows)
        conn.commit()
        print(f"Inserted {len(rows)} products successfully.")
        return True

    except (pyodbc.Error, TypeError, AttributeError) as e:
        conn.rollback()
        print(f"Insert failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()


def save_products(products):
    try:
        conn = get_connection()
        if conn:
            insert_products(conn, products)
            conn.close()
    except Exception as e:
        print(f"An Exception Occurred in save_products due to {e}")


def load_products():
    conn = None
    cursor = None
    products = []

    try:
        conn = get_connection()
        if conn is None:
            return products

        cursor = conn.cursor()
        cursor.execute(f""" SELECT SKU, PRODUCT, MAKER, PRICE, STOCK, UPDATED FROM {config.DB_TABLE} """)

        for row in cursor.fetchall():
            product = Model_Live_Product()
            product.SKU = row[0]
            product.PRODUCT = row[1]
            product.MAKER = row[2]
            product.PRICE = f"${row[3]:.2f}" if row[3] is not None else None
            product.STOCK = row[4]
            product.UPDATED = row[5].strftime("%H:%M") if row[5] is not None else None
            products.append(product)

        return products

    except pyodbc.Error as e:
        print(f"Error loading products: {e}")
        return []

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()