# service layer
import shutil
from collections import defaultdict

from repo.product_repo import (
    bulkInsertImageDataInFinaliseAngle,
    findAll,
    findAllUnfilteredAngles,
    findAllUnfilteredAnglesByIndex,
    findAllUnfilteredAnglesByProductId,
    insertImageMain,
    insertProductAngles,
)

import os


def getProductsProgress():

    # fetching from database layer
    products = findAll()

    grouped_data = defaultdict(list)
    for item in products:
        grouped_data[item["product_id"]].append(item)

    # Convert defaultdict to a regular dictionary
    result = [{"id": pid, "images": images} for pid, images in grouped_data.items()]

    return result


def getProductsForAngleFiltering(product_id, index):

    products = []
    if product_id is not None and product_id != "null":
        products = findAllUnfilteredAnglesByProductId(product_id)
        return products

    if index is not None and index != "null":
        products = findAllUnfilteredAnglesByIndex(index)
        return products

    products = findAllUnfilteredAngles()

    grouped_data = defaultdict(list)
    for item in products:
        grouped_data[item["product_id"]].append(item)

    # Convert defaultdict to a regular dictionary
    result = [{"id": pid, "images": images} for pid, images in grouped_data.items()]

    return result


def bulkInsertFinaliseAngleFromFolder(directory_path):

    try:

        data_to_insert = []

        for folder_name in os.listdir(directory_path):
            folder_path = os.path.join(directory_path, folder_name)
            if os.path.isdir(folder_path):
                for image_name in os.listdir(folder_path):
                    image_path = os.path.join(folder_path, image_name)
                    if os.path.isfile(image_path):
                        # Collect data to insert
                        data_to_insert.append(
                            {
                                "product_id": folder_name,
                                "angle_id": None,  # Set appropriate angle_id if needed
                                "image_name": image_name,
                                "image_path": image_path,
                            }
                        )

        # Perform bulk insert
        if data_to_insert:
            bulkInsertImageDataInFinaliseAngle(data_to_insert)

        return True

    except Exception as e:
        print(e)
        return False


def updateProductAngles(product_id, data):

    result = insertProductAngles(product_id, data)

    return result


def getAllProductAnglesProgress():

    products = findAllUnfilteredAngles()

    grouped_data = defaultdict(lambda: {"count": 0, "status": "pending"})
    for item in products:

        if item["angle_id"] != None and item["angle_id"] != "":
            grouped_data[item["product_id"]]["count"] += 1

        if grouped_data[item["product_id"]]["count"] == 4:
            grouped_data[item["product_id"]]["status"] = "completed"

    # Convert defaultdict to a regular dictionary

    return grouped_data


def createAndInsertImageMain():
    # copy valid files from ../shoot folder into the ../finalised-angles folder
    # the valid image is decided by the finalised-angle table where for each product
    # we check which files have been assigned angle
    # check ../finalised-angle folder and add its images and data to the image-main table

    folderPath = "../finalised_angles"

    if not os.path.isdir(folderPath):
        return "no directory found to copy the files in : contact admin"

    try:
        allFiles = (
            findAllUnfilteredAngles()
        )  # This function needs to be defined elsewhere
    except Exception as e:
        return f"Error retrieving angle data: {str(e)}"

    imageMainEntries = []
    processed_count = 0

    for i in allFiles:
        # Skip if angle_id is None or empty
        if i["angle_id"] is None or i["angle_id"] == "":
            continue

        subcategory_path = os.path.join(folderPath, i["sub_category"])
        product_path = os.path.join(subcategory_path, i["product_sku_number"])

        # Create directories if they don't exist
        os.makedirs(product_path, exist_ok=True)

        # Define source and destination file paths
        source_file = os.path.join("../shoot", i["product_sku_number"], i["image_name"])

        dest_file = os.path.join(
            product_path, f"{i['product_sku_number']}_{i['angle_id']}.jpg"
        )

        # Skip if destination file already exists
        if os.path.isfile(dest_file):
            continue

        # Check if source file exists
        if not os.path.isfile(source_file):
            print(f"Warning: Source file not found: {source_file}")
            continue

        try:
            # Use shutil.copy2 instead of os.system for better error handling and preservation of metadata

            shutil.copy2(source_file, dest_file)

            # Prepare data for image_main table
            imageMainEntries.append(
                {
                    "sub_category": i["sub_category"],
                    "product_sku_number": i["product_sku_number"],
                    "angle_id": i["angle_id"],
                    "file_path": dest_file,
                }
            )

            processed_count += 1

        except Exception as e:
            print(f"Error copying {source_file} to {dest_file}: {str(e)}")

    # TODO: Add code to insert imageMainEntries into the database
    # For example:
    # insert_into_image_main_table(imageMainEntries)

    if processed_count == 0:
        return "No new files were processed"

    return f"Processed {processed_count} files. Database entries prepared but not inserted."
