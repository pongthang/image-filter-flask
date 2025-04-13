from flask import Flask
from flask_cors import CORS
from apis.product_apis import product_api
from routes.main import main_bp  # Importing blueprint

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

@app.route('/shoot/<folder>/<file>')
def shoot(folder, file):
    import os
    import io
    from PIL import Image, ImageOps
    from flask import send_file
    # Path to the image
    image_path = os.path.join('../shoot', folder, file)

    print(image_path)

    # Open the image
    with Image.open(image_path) as img:
        # Automatically correct orientation based on EXIF data
        img = ImageOps.exif_transpose(img)

        # # # Resize image (optional)
        max_width = 800
        max_height = 800
        img.thumbnail((max_width, max_height))

        # Compress the image based on its format
        img_io = io.BytesIO()

        file_extension = os.path.splitext(image_path)[1].lower()

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
            download_name=image_path.split(os.sep)[-1],
        )

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(product_api)

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    app.run(host='0.0.0.0', port=8501, debug=True)
