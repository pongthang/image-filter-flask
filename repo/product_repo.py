# repo/database layer

from collections import defaultdict

from flask import json, jsonify
from database import get_db_connection


def findAll():
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

    return [dict(product) for product in products]


def findAllUnfilteredAngles():
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
    cursor.execute("""SELECT * FROM finalised_angles where image_name!='1.JPG' """)
    products = cursor.fetchall()
    conn.close()

    return [dict(product) for product in products]


def bulkInsertImageDataInFinaliseAngle(data):
    """
    Inserts multiple records into the 'finalised_angles' table.

    Args:
        data (list): A list of dictionaries, each representing a record to insert.

    Returns:
        int: The number of records inserted.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO finalised_angles (product_id, angle_id, image_name, image_path)
    VALUES (?, ?, ?, ?)
    """

    values = [
        (item["product_id"], item["angle_id"], item["image_name"], item["image_path"])
        for item in data
    ]

    cursor.executemany(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()

    return len(data)


def findAllUnfilteredAnglesByIndex(index):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """  SELECT product_id FROM finalised_angles 
    WHERE image_name != '1.JPG' 
    GROUP BY product_id 
    ORDER BY finalised_angles_id 
    LIMIT 1 OFFSET ?;""",
        (index,),
    )
    product_id = cursor.fetchone()

    if product_id is None:
        return []

    cursor.execute(
        """SELECT * FROM finalised_angles 
    WHERE product_id = ?
    AND image_name != '1.JPG'""",
        (product_id[0],),
    )

    products = cursor.fetchall()

    conn.close()

    return [dict(product) for product in products]


def findAllUnfilteredAnglesByProductId():
    return []


def insertProductAngles(product_id, data: list):
    connection = get_db_connection()
    cursor = connection.cursor()

    update_query = """
    UPDATE finalised_angles
    SET angle_id = ?
    WHERE product_id = ?
    AND image_name = ?
    """

    print(update_query)

    values = [(item["angle_id"], product_id, item["image_name"]) for item in data]

    print(values)

    cursor.executemany(update_query, values)
    connection.commit()
    cursor.close()
    connection.close()

    return len(data)
