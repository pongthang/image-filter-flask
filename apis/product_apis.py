import base64
from collections import defaultdict
import os
import re
import shutil
from flask import Blueprint, jsonify, request

from repo.product_repo import (
    find_filtered_facefix,
    findFaceSwapImagesByIndexAndAngleId,
    findFaceSwapImagesByProductIdAndAngleId,
    insertImageSwapEntries,
    project_id_by_product_id,
    update_face_swap,
    update_image_main,
)
from services.product_service import (
    bulkInsertFinaliseAngleFromFolder,
    createAndInsertImageMain,
    getAllProductAnglesProgress,
    getProductsForAngleFiltering,
    getProductsProgress,
    updateProductAngles,
)


product_api = Blueprint("product_api", __name__, url_prefix="/api/products")


@product_api.route("/", methods=["GET"])
def list_products_with_files():
    """Returns all products with their associated files"""
    products = getProductsProgress()

    return jsonify(products)


@product_api.route("/finalise-angles", methods=["GET"])
def getFinaliseImages():
    """Returns all products with their associated files"""
    products = getProductsForAngleFiltering(None, None)

    return jsonify(products)


@product_api.route("/finalise-product", methods=["GET"])
def getAllProductImages():
    """Returns all products with their associated files"""
    product_id = request.args.get("product_id")
    index = request.args.get("index")
    products = getProductsForAngleFiltering(product_id, index)

    return jsonify(products)


@product_api.route("/bulk-insert/finalise-angle", methods=["GET"])
def bulkInsertFinaliseAngle():
    """Returns all products with their associated files"""
    status = bulkInsertFinaliseAngleFromFolder("../shoot")

    if status:
        return jsonify({"message": "Data inserted successfully"})
    else:
        return jsonify({"message": "Data insertion failed"})


@product_api.route("/finalise-product", methods=["POST"])
def postProductAngles():
    """Returns all products with their associated files"""
    product_id = request.args.get("product_id")
    data = request.get_json()

    products = updateProductAngles(product_id, data)

    return jsonify(products)


@product_api.route("/finalise-products-progress", methods=["GET"])
def productAnglesProgress():
    """Returns all products with their associated files"""
    products = getAllProductAnglesProgress()

    return jsonify(products)


@product_api.route("/bulk-insert/image-main", methods=["GET"])
def bulkInsertImageMain():
    """Returns all products with their associated files"""
    # copy valid files from ../shoot folder into the ../finalised-angles folder
    # the valid image is decided by he finalised-angle table where for each product we check which files have been assigned angle
    # check ../finalised-angle folder and add its images and data to the image-main table
    project_id = 5
    response = createAndInsertImageMain(project_id, False)

    return response


@product_api.route("/firstpass-filter/<angle>", methods=["GET"])
def get_images(angle):

    product_id = request.args.get("product_id")
    index = request.args.get("index")
    lora_id = request.args.get("lora_id") or None
    # This would be replaced with your actual data source
    # Example API response matching your required structure
    # folder_name = "../output/Intune Men Wears"
    # if not os.path.exists(folder_name):
    #     return jsonify({"error": "Folder not found"}), 404

    # if product_id is not None and product_id != "null":
    #     folder_name = os.path.join(folder_name, product_id)
    #     index = os.listdir(folder_name).index(product_id)

    # if (
    #     (product_id is None or product_id == "null")
    #     and index is not None
    #     and index != "null"
    # ):
    #     p = os.listdir(folder_name)[int(index)]
    #     folder_name = os.path.join(folder_name, p)

    product_arr = []
    if product_id is not None and product_id != "null":
        products = findFaceSwapImagesByProductIdAndAngleId(product_id, angle, lora_id)
        product_arr = products

    if index is not None and index != "null":
        products = findFaceSwapImagesByIndexAndAngleId(index, angle, lora_id)
        product_arr = products

    print("product_arr", product_arr)

    product_id = product_arr[0]["product_id"]

    return jsonify(
        {
            "new_images": product_arr,
            "product_id": product_id,
            "index": index,
            "original_image": product_arr[0]["original_image_path"],
        }
    )

    # images = []
    # print(folder_name)
    # for idx, file_name in enumerate(os.listdir(folder_name), start=1):

    #     if (
    #         file_name.lower().endswith((".png", ".jpg", ".jpeg"))
    #         and file_name.split("_")[2] == angle
    #     ):
    #         images.append(
    #             {
    #                 "name": file_name,
    #                 "path": os.path.join(folder_name, file_name),
    #                 "link": file_name.split("_")[0] + "/",
    #             }
    #         )

    # product_id = folder_name.split("/")[-1]

    # return jsonify(
    #     {
    #         "product_id": product_id,
    #         "original_image": "../finalised_angles/Intune Men Wears/"
    #         + product_id
    #         + "/"
    #         + product_id
    #         + "_"
    #         + angle
    #         + ".jpg",
    #         "new_images": images,
    #         "index": index,
    #     }
    # )


@product_api.route("/add-face-swap-entires", methods=["GET"])
def add_face_swap_entries():

    folder_name = "../output/project_4_out_skin/"

    images = []
    print(folder_name)
    # pId = os.listdir(folder_name)[0]
    # print("pId", pId)

    # project_id = project_id_by_product_id(pId)
    # print("project_id", project_id)

    for idx, product_folder in enumerate(os.listdir(folder_name), start=1):
        for idx, file_name in enumerate(
            os.listdir(os.path.join(folder_name, product_folder)), start=1
        ):

            images.append(
                {
                    "product_id": product_folder,
                    "angle_id": file_name.split("_")[-3],
                    "image_name": file_name,
                    "image_path": os.path.join(folder_name, product_folder, file_name),
                    "lora_id": 1,
                    # "project_id": project_id,
                }
            )

    print("images", images)

    count = insertImageSwapEntries(images)

    return jsonify(
        {
            "count": count,
            "new_images": images,
        }
    )


@product_api.route("/update-face-swap-entry", methods=["POST"])
def update_face_swap_entries():

    images = request.get_json()
    # lora_id = request.args.get("lora_id") or None

    # if(lora_id is None):
    #     return jsonify({"message": "lora_id is required"})

    data = []
    to_update_image_main = False

    for i in images["evaluations"]:
        d = {
            "face_swap_score": 1 if i["evaluations"]["faceGood"] else 0,
            "need_edit": (
                1
                if i["evaluations"]["needEdit"] and i["evaluations"]["faceGood"]
                else 0
            ),
            "image_name": i["image_name"],
        }

        if d["face_swap_score"] == 1:
            to_update_image_main = True

        data.append(d)

    update_face_swap(data)
    if to_update_image_main:
        product_id = images["productId"]
        angle = images["angle"]

        update_image_main("facefix", product_id, angle)

    return jsonify({"data": data})


@product_api.route("/move-facefix-images", methods=["GET"])
def move_face_fix():

    project_id = 4

    chosen_files = find_filtered_facefix(4)

    # copy the files to the facefix folder using the image_path
    for f in chosen_files:
        print(f["image_path"])
        # create a folder in ../facefix with name = product_id
        print(f["product_id"])

        project_path = os.path.join("../facefix", "project_" + str(project_id))
        if os.path.exists(project_path) == False:
            os.mkdir(project_path)

        path = os.path.join(project_path, f["product_id"])
        if os.path.exists(path) == False:
            os.mkdir(path)

        if os.path.exists(f["image_path"]):
            shutil.copy(f["image_path"], os.path.join(path, f["image_name"]))
        else:
            print("File not found for path", f["image_path"])

    return jsonify({"data": chosen_files})


@product_api.route("/edit-image/<angle>", methods=["GET"])
def edit_image(angle):

    product_id = request.args.get("product_id")
    index = request.args.get("index")
    lora_id = request.args.get("lora_id") or None

    originalImages = getProductsForAngleFiltering(product_id, index)
    face_swap_images = findFaceSwapImagesByIndexAndAngleId(index, angle, lora_id)

    project_id = originalImages["data"][0]["project_id"]
    product_id = originalImages["data"][0]["product_id"]

    print(product_id, project_id, angle, index)

    last_edited_image = os.path.exists(
        os.path.join(
            "../edited_images",
            "project_" + str(project_id),
            product_id,
            product_id + "_" + angle + ".jpg",
        )
    )

    if last_edited_image is None or last_edited_image == False:
        last_edited_image = ""

    original_image = {
        "image_path": "",
        "image_name": "",
        "image_angle": 0,
    }

    face_swap_image = {
        "image_path": "",
        "image_name": "",
        "image_angle": 0,
    }
    for i in originalImages["data"]:
        print(i)
        if i["angle_id"] == angle:
            original_image["image_path"] = i["image_path"]
            original_image["image_name"] = i["image_name"]
            original_image["image_angle"] = i["angle_id"]
            break

    for i in face_swap_images:
        if i["angle_id"] == angle:
            face_swap_image["image_path"] = i["image_path"]
            face_swap_image["image_name"] = i["image_name"]
            face_swap_image["image_angle"] = i["angle_id"]
            break

    return jsonify(
        {
            "original_image": original_image,
            "face_swap_image": face_swap_image,
            "last_edited_image": last_edited_image,
            "project_id": project_id,
        }
    )


@product_api.route("/save_edited_image", methods=["POST"])
def save_edited_image():
    """Receives base64 encoded image data and saves it to a file."""
    data = request.get_json()

    if not data or "image_data" not in data or "filename" not in data:
        return jsonify({"error": "Missing image data or filename"}), 400

    image_data_url = data["image_data"]
    filename = data["filename"]
    # Optional: Get product_id, angle etc. if you need to organize saves
    # product_id = data.get('product_id')
    # angle = data.get('angle')

    # Basic validation for filename
    filename = re.sub(r"[^\w\.\-]", "_", filename)  # Sanitize filename

    try:
        # Decode the base64 string
        # Remove the header part (e.g., "data:image/png;base64,")
        header, encoded = image_data_url.split(",", 1)
        image_data_bytes = base64.b64decode(encoded)

        # Define save path (customize as needed)
        save_directory = "../edited_images"  # Create this directory if it doesn't exist
        os.makedirs(save_directory, exist_ok=True)  # Ensure directory exists
        save_path = os.path.join(save_directory, filename)

        # Write the image data to a file
        with open(save_path, "wb") as f:
            f.write(image_data_bytes)

        print(f"Image saved successfully to: {save_path}")
        return (
            jsonify(
                {
                    "message": "Image saved successfully",
                    "filename": filename,
                    "path": save_path,
                }
            ),
            200,
        )

    except base64.binascii.Error as e:
        print(f"Error decoding base64 data: {e}")
        return jsonify({"error": "Invalid image data format"}), 400
    except Exception as e:
        print(f"Error saving image: {e}")
        return (
            jsonify({"error": f"An error occurred while saving the image: {str(e)}"}),
            500,
        )
