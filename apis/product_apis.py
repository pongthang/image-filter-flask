from flask import Blueprint, jsonify
from repo.product_repo import get_all_product_progress

product_api = Blueprint("product_api", __name__, url_prefix="/api/products")


@product_api.route("/", methods=["GET"])
def list_products_with_files():
    """Returns all products with their associated files"""
    products = get_all_product_progress()

    return jsonify(products)
