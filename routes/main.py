import os
from flask import Blueprint, render_template, send_file, send_from_directory

from services.product_service import getAllProductAnglesProgress
from PIL import Image, ImageOps
import io

main_bp = Blueprint("main", __name__)
IMAGE_FOLDER = "../"


@main_bp.route("/")
def home():
    return render_template("product_progress.html")


@main_bp.route("/<parentfolder>/<category>/<foldername>/<filename>")
def get_image(parentfolder, category, foldername, filename):

    # Path to the image
    image_path = (
        IMAGE_FOLDER + parentfolder + "/" + category + "/" + foldername + "/" + filename
    )

    # Open the image
    with Image.open(image_path) as img:
        # Resize image (optional)
        image_path = (
            IMAGE_FOLDER
            + parentfolder
            + "/"
            + category
            + "/"
            + foldername
            + "/"
            + filename
        )

    # Open the image
    with Image.open(image_path) as img:
        # Automatically correct orientation based on EXIF data
        img = ImageOps.exif_transpose(img)

        # Resize image (optional)
        # max_width = 800
        # max_height = 800
        # img.thumbnail((max_width, max_height))

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


@main_bp.route("/filter-images")
def compare_images():
    return render_template("firstpass_filter.html")


@main_bp.route("/edit-image")
def edit_image_page():
    # You might want to pass the product_id or index from the request args
    # to the template if needed for initial setup, but the JS currently handles it.
    # product_id = request.args.get('product_id')
    # index = request.args.get('index')
    return render_template("image_correction.html")  # Pass variables if needed


@main_bp.route("/edit-image2")
def edit_image_page2():
    # You might want to pass the product_id or index from the request args
    # to the template if needed for initial setup, but the JS currently handles it.
    # product_id = request.args.get('product_id')
    # index = request.args.get('index')
    return render_template("image_edit.html")  # Pass variables if needed
