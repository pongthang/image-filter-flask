import os
from flask import Blueprint, render_template, send_file, send_from_directory

from services.product_service import getAllProductAnglesProgress
from PIL import Image, ImageOps
import io

main_bp = Blueprint("main", __name__)
IMAGE_FOLDER = "../shoot/"


@main_bp.route("/")
def home():
    return render_template("product_progress.html")


@main_bp.route("/shoot/<foldername>/<filename>")
def get_image(foldername, filename):

    # Path to the image
    image_path = IMAGE_FOLDER + foldername + "/" + filename

    # Open the image
    with Image.open(image_path) as img:
        # Resize image (optional)
        image_path = IMAGE_FOLDER + foldername + "/" + filename

    # Open the image
    with Image.open(image_path) as img:
        # Automatically correct orientation based on EXIF data
        img = ImageOps.exif_transpose(img)

        # Resize image (optional)
        max_width = 800
        max_height = 800
        img.thumbnail((max_width, max_height))

        # Compress the image based on its format
        img_io = io.BytesIO()

        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension == ".png":
            # For PNG, use lossless compression
            img.save(img_io, "PNG", optimize=True)
        else:
            # For JPEG, use lossy compression
            img.save(img_io, "JPEG", quality=80)

        img_io.seek(0)

        # Send the image as a response
        return send_file(
            img_io,
            mimetype="image/jpeg" if file_extension != ".png" else "image/png",
            as_attachment=False,
            download_name=filename,
        )


@main_bp.route("/finalise-angles")
def finaliseAngles():
    return render_template("finalise_angles.html")


@main_bp.route("/angles-progress")
def angles_progress():
    # This would typically come from your API call
    products = getAllProductAnglesProgress()

    return render_template("angles_progress.html", products=products)
