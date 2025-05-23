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
    cursor.execute("""SELECT * FROM image_main ORDER BY id""")
    products = cursor.fetchall()
    conn.close()

    return [dict(product) for product in products]


def findAllUnfilteredAngles(project_id):
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
    cursor.execute(
        """select * from finalised_angles fa 
    left join products p on fa.product_id = p.product_sku_number
    where image_name!='1.JPG0' AND fa.project_id ==?""", str(project_id)
    )
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
    INSERT OR IGNORE INTO finalised_angles (product_id, angle_id, image_name, image_path, project_id)
    VALUES (?, ?, ?, ?, ?)
    """

    values = [
        (item["product_id"], item["angle_id"], item["image_name"], item["image_path"], item["project_id"])
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

    return {
        "data": [dict(product) for product in products],
        "metadata": {"index": index},
    }


def findAllUnfilteredAnglesByProductId(product_id):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM finalised_angles 
    WHERE product_id = ?
    AND image_name != '1.JPG'""",
        (product_id,),
    )

    products = cursor.fetchall()
    conn.close()

    metadata = unfilteredProductAnglesMetadata(product_id)

    return {"data": [dict(product) for product in products], "metadata": metadata}


def unfilteredProductAnglesMetadata(product_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT product_id FROM finalised_angles 
    WHERE image_name != '1.JPG' 
    GROUP BY product_id 
    ORDER BY finalised_angles_id """
    )

    product_ids = cursor.fetchall()
    product_ids = [item[0] for item in product_ids]

    index = product_ids.index(product_id)

    # cursor.execute(
    #     """
    #     SELECT COUNT(*)
    #     FROM (
    #         SELECT product_id
    #         FROM finalised_angles
    #         WHERE image_name != '1.JPG'
    #         GROUP BY product_id
    #         ORDER BY finalised_angles_id
    #     ) subquery
    #     WHERE product_id != ?;
    #     """,
    #     (product_id,),
    # )
    conn.close()

    return {"index": index}


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


def insertImageMain(data):

    conn = get_db_connection()
    curr = conn.cursor()

    # convert list of objects to list of lists
    data = [list(item.values()) for item in data]

    # execute the query
    curr.executemany(
        """INSERT OR IGNORE INTO image_main (product_id, angle_id, image_path) VALUES (?, ?, ?)""",
        data,
    )

    # get the count of rows inserted
    count = curr.rowcount
    conn.commit()
    conn.close()

    return count


def insertImageSwapEntries(images):
    conn = get_db_connection()
    curr = conn.cursor()

    # convert list of objects to list of lists
    data = [list(item.values()) for item in images]
    print(data)

    # dublicate check on image_name
    curr.executemany(
        """Insert INTO face_swap (product_id,angle_id, image_name, image_path, lora_id) VALUES (?, ?, ?, ?, ?)""",
        data,
    )

    count = curr.rowcount
    conn.commit()
    conn.close()

    return int(count)


def update_face_swap(data):

    conn = get_db_connection()
    curr = conn.cursor()

    # convert list of objects to list of lists
    data = [list(item.values()) for item in data]
    print(data)

    # dublicate check on image_name
    curr.executemany(
        """UPDATE face_swap SET face_swap_score=?, need_edit= ? WHERE image_name = ?""",
        data,
    )

    count = curr.rowcount
    conn.commit()
    conn.close()

    return int(count)


def findFaceSwapImagesByProductIdAndAngleId(product_id, angle_id, lora_id):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT fs.product_id, fs.angle_id, fs.image_name, fs.image_path, fs.need_edit, fs.face_swap_score, fa.image_path as original_image_path 
FROM face_swap fs
LEFT JOIN finalised_angles fa ON fs.product_id = fa.product_id AND fs.angle_id = fa.angle_id
WHERE fs.product_id = ? AND fs.angle_id = ? AND fs.lora_id=?""",
        (product_id, angle_id, lora_id),
    )

    products = cursor.fetchall()
    conn.close()

    return [dict(product) for product in products]


def findFaceSwapImagesByIndexAndAngleId(index, angle_id, lora_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT product_id FROM face_swap fs
    GROUP BY product_id
    ORDER BY face_swap_id
    LIMIT 1 OFFSET ?;""",
        (index,),
    )
    product_id = cursor.fetchone()



    if product_id is None:
        return []

    cursor.execute(
        """SELECT fs.product_id, fs.angle_id, fs.image_name, fs.image_path, fs.face_swap_score, fs.need_edit,  fa.image_path as original_image_path 
FROM face_swap fs
LEFT JOIN finalised_angles fa ON fs.product_id = fa.product_id AND fs.angle_id = fa.angle_id
WHERE fs.product_id = ? AND fs.angle_id = ? AND fs.lora_id=?;""",
        (product_id[0], angle_id, lora_id),
    )

    products = cursor.fetchall()
    conn.close()

    return [dict(product) for product in products]


def update_image_main(step, product_id, angle_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    if step == "facefix":

        cursor.execute(
            """UPDATE image_main SET face_swap_status="DONE" WHERE product_id=? AND angle_id = ?""",
            (product_id, angle_id),
        )

    count = cursor.rowcount
    conn.commit()
    conn.close()

    return count


def find_filtered_facefix(project_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""Select * from face_swap fs left join finalised_angles fa on fs.product_id=fa.product_id and fs.angle_id=fa.angle_id where face_swap_score=1 and project_id=?""", (str(project_id),))

    images = cursor.fetchall()
    conn.commit()
    conn.close()

    return [dict(product) for product in images]


def project_id_by_product_id(product_id):
    """
    Fetches the project ID associated with a given product ID.

    Args:
        product_id (str): The product ID to search for.

    Returns:
        str: The project ID associated with the product ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT project_id FROM finalised_angles WHERE product_id = ?""",
        (product_id,),
    )
    project_id = cursor.fetchone()
    conn.close()

    return project_id[0] if project_id else None