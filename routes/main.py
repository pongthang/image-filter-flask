from flask import Blueprint, render_template, send_from_directory

from services.product_service import getAllProductAnglesProgress

main_bp = Blueprint("main", __name__)
IMAGE_FOLDER = "../shoot/"


@main_bp.route("/")
def home():
    return render_template("product_progress.html")


@main_bp.route("/shoot/<foldername>/<filename>")
def get_image(foldername, filename):

    return send_from_directory(IMAGE_FOLDER + foldername, filename)


@main_bp.route("/finalise-angles")
def finaliseAngles():
    return render_template("finalise_angles.html")


@main_bp.route("/angles-progress")
def angles_progress():
    # This would typically come from your API call
    products = getAllProductAnglesProgress()

    return render_template("angles_progress.html", products=products)
