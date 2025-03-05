from collections import defaultdict

from flask import json, jsonify
from database import get_db_connection


def get_all_product_progress():
    """
    Fetches all product progress from the database.

    This function connects to the database, executes a query to select all
    records from the 'image_main' table, and returns the results as a list
    of dictionaries.

    Returns:
        list: A list of dictionaries, each representing a product record.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM image_main""")
    products = cursor.fetchall()
    conn.close()

    column_names = [desc[0] for desc in cursor.description]

    groupedData = defaultdict(list)

    for product in products:
        product_dict = dict(zip(column_names, product))
        groupedData[product_dict["product_id"]].append(product_dict)

    nested_json = [{"id": key, "images": value} for key, value in groupedData.items()]

    return nested_json
