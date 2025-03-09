import sqlite3

conn = sqlite3.connect("images.db")
cursor = conn.cursor()


def createImageMainTable():
    # check if image_main table exists
    cursor.execute(
        """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='image_main'"""
    )
    if cursor.fetchone()[0] == 1:
        print("Table exists.")
        return

    # Creating image_main table
    cursor.execute(
        """CREATE TABLE image_main (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    angle_id INTEGER NOT NULL,
    image_path TEXT UNIQUE NOT NULL,
    first_pass_status TEXT CHECK(first_pass_status IN ('PENDING', 'DONE', 'RERUN')) DEFAULT 'PENDING',
    face_swap_status TEXT CHECK(face_swap_status IN ('PENDING', 'DONE', 'RERUN')) DEFAULT 'PENDING',
    hand_fix_status TEXT CHECK(hand_fix_status IN ('PENDING', 'DONE', 'RERUN')) DEFAULT 'PENDING',
    upscale_status TEXT CHECK(upscale_status IN ('PENDING', 'DONE', 'RERUN')) DEFAULT 'PENDING')"""
    )

    print("image_main table created.")


def createFirstPassTable():
    # check if first_pass table exists
    cursor.execute(
        """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='first_pass'"""
    )
    if cursor.fetchone()[0] == 1:
        print("Table exists.")
        return

    # Creating first_pass table
    cursor.execute(
        """CREATE TABLE first_pass (
    first_pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    angle_id TEXT NOT NULL,
    image_name TEXT NOT NULL,
    image_path TEXT NOT NULL,
    cloth_score INTEGER DEFAULT 0,
    skin_score INTEGER DEFAULT 0,
    hair_score INTEGER DEFAULT 0,
    hand_score INTEGER DEFAULT 0)"""
    )

    print("first_pass table created.")


def createFaceSwapTable():
    # check if face_swap table exists
    cursor.execute(
        """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='face_swap'"""
    )
    if cursor.fetchone()[0] == 1:
        print("Table exists.")
        return

    # Creating face_swap table
    cursor.execute(
        """CREATE TABLE face_swap (
        first_pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    angle_id TEXT NOT NULL,
    image_name TEXT NOT NULL,
    image_path TEXT NOT NULL,
    face_swap_score INTEGER DEFAULT 0)"""
    )


def createHandFixTable():
    # check if hand_fix table exists
    cursor.execute(
        """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='hand_fix'"""
    )
    if cursor.fetchone()[0] == 1:
        print("Table exists.")
        return

    # Creating face_swap table
    cursor.execute(
        """CREATE TABLE hand_fix (
        first_pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    angle_id TEXT NOT NULL,
    image_name TEXT NOT NULL,
    image_path TEXT NOT NULL,
    hand_fix_score INTEGER DEFAULT 0)"""
    )


def createFinalisedAngles():
    # check if hand_fix table exists
    cursor.execute(
        """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='finalised_angles'"""
    )
    if cursor.fetchone()[0] == 1:
        print("Table exists.")
        return

    # Creating face_swap table
    cursor.execute(
        """CREATE TABLE finalised_angles (
        finalised_angles_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    angle_id TEXT DEFAULT NULL,
    image_name TEXT NOT NULL,
    image_path TEXT NOT NULL)"""
    )


def createProductsTable():

    cursor.execute(
        """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='products'"""
    )
    if cursor.fetchone()[0] == 1:
        print("Table exists.")
        return

    cursor.execute(
        """ CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_sku_number TEXT UNIQUE NOT NULL,
    brand TEXT NOT NULL,
    type TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    product_type TEXT NOT NULL
    );"""
    )


def createTables():
    createImageMainTable()
    createFirstPassTable()
    createFaceSwapTable()
    createHandFixTable()
    createFinalisedAngles()
    createProductsTable()


print("Creating tables...")
createTables()
print("Tables created.")
