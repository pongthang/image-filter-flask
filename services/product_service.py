# service layer

from collections import defaultdict

from repo.product_repo import (
    bulkInsertImageDataInFinaliseAngle,
    findAll,
    findAllUnfilteredAngles,
    findAllUnfilteredAnglesByIndex,
    findAllUnfilteredAnglesByProductId,
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


def getProductsForAngleFiltering(prodcut_id, index):

    products = []
    if prodcut_id:
        products = findAllUnfilteredAnglesByProductId()
        return products

    if index:
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
