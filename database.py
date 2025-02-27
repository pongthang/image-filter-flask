## create database oof the clothes
#sqlite3
#struncture as below
## image_id(name of the image) | path | cloth name | view | original cloth path | vote | comments


import sqlite3

# Define database file
DB_FILE = "images.db"

def create_tables():
    """Creates the images and exported_images tables if they do not exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            key TEXT PRIMARY KEY,
            path TEXT,
            name TEXT,
            view TEXT,
            ori_name TEXT,
            ori_path TEXT,
            vote INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exported_images (
            key TEXT PRIMARY KEY,
            ori_name TEXT,
            view TEXT,
            selected_image TEXT,
            FOREIGN KEY (selected_image) REFERENCES images(key)
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_data(images):
    """Inserts image data into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    for key, data in images.items():
        cursor.execute('''
            INSERT INTO images (key, path, name, view, ori_name, ori_path, vote)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (key, data['path'], data['name'], data['view'], data['ori_name'], data['ori_path'], data['vote']))
    
    conn.commit()
    conn.close()

def fetch_all():
    """Fetches and prints all rows from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM images")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    conn.close()

def fetch_by_ori_name_and_view(ori_name, view):
    """Fetches all image info for a given ori_name and view as a dictionary."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM images WHERE ori_name = ? AND view = ?", (ori_name, view))
    rows = cursor.fetchall()
    
    column_names = [desc[0] for desc in cursor.description]
    
    data = {}
    for row in rows:
        row_dict = dict(zip(column_names, row))
        data[row_dict["key"]] = row_dict
    
    conn.close()
    return data

def update_image_info(image_key, column, value):
    """Updates a specific column value for a given image key."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    query = f"""UPDATE images SET {column} = ? WHERE key = ?"""
    cursor.execute(query, (value, image_key))
    
    conn.commit()
    conn.close()


def update_image_info_new_column(image_key, column, value):
    """Updates a specific column value for a given image key. If column does not exist, it is added with default None values."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(images)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if column not in columns:
        # Add new column with default NULL values
        cursor.execute(f"ALTER TABLE images ADD COLUMN {column} TEXT DEFAULT NULL")
        conn.commit()
    
    # Update the column value for the specific image key
    query = f"UPDATE images SET {column} = ? WHERE key = ?"
    cursor.execute(query, (value, image_key))
    
    conn.commit()
    conn.close()


def insert_exported_images(exported_images):
    """Inserts multiple records into the exported_images table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    for key, data in exported_images.items():
        cursor.execute('''
            INSERT INTO exported_images (key, ori_name, view, selected_image)
            VALUES (?, ?, ?, ?)
        ''', (key, data['ori_name'], data['view'], data['selected_image']))
    
    conn.commit()
    conn.close()

def fetch_exported_images(ori_name, view):
    """Fetches image info from images table for a given ori_name and view from exported_images table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT images.* FROM images 
        JOIN exported_images ON images.key = exported_images.selected_image
        WHERE exported_images.ori_name = ? AND exported_images.view = ?
    ''', (ori_name, view))
    
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    
    data = {}
    for row in rows:
        row_dict = dict(zip(column_names, row))
        data[row_dict["key"]] = row_dict
    
    conn.close()
    return data

def update_exported_image(ori_name, view, new_selected_image):
    """Updates the selected_image value for a given ori_name and view."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE exported_images
        SET selected_image = ?
        WHERE ori_name = ? AND view = ?
    ''', (new_selected_image, ori_name, view))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Given Data
    data = {
        "image_3": {
            "view": "front",
            "name": "5715512990538_1_first_pass_0001.png",
            "path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass/5715512990538/5715512990538_1_first_pass_0001.png",
            "ori_name": "5715512990538",
            "ori_path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/original_image_folder/5715512990538/5715512990538_1.jpg",
            "vote": 0,
            "key": "image_0"
        },
        "image_4": {
            "view": "front",
            "name": "5715512990538_1_first_pass_0002.png",
            "path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass/5715512990538/5715512990538_1_first_pass_0002.png",
            "ori_name": "5715512990538",
            "ori_path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/original_image_folder/5715512990538/5715512990538_1.jpg",
            "vote": 0,
            "key": "image_1"
        },
        "image_5": {
            "view": "front",
            "name": "5715512990538_1_first_pass_0003.png",
            "path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass/5715512990538/5715512990538_1_first_pass_0003.png",
            "ori_name": "5715512990538",
            "ori_path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/original_image_folder/5715512990538/5715512990538_1.jpg",
            "vote": 0,
            "key": "image_2"
        }
    }

    exported_images  = {"exported_1":{"ori_name": "5715512990538","view": "front","selected_image":"image_1"}}
    # Execute functions
    create_tables()
    # insert_data(data)
    # fetch_all()

    # print(fetch_by_ori_name_and_view("5715512990538","front"))

    # insert_exported_images(exported_images)
    print(fetch_exported_images("5715512990538","front"))
    update_exported_image("5715512990538","front","image_3")
    print(fetch_exported_images("5715512990538","front"))
