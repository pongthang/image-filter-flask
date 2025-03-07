from flask import Blueprint, render_template, send_from_directory

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
