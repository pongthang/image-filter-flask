from flask import Blueprint, jsonify, request

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
    response = createAndInsertImageMain()

    return response
