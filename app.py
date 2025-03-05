from flask import Flask

from apis.product_apis import product_api
from routes.main import main_bp  # Importing blueprint

app = Flask(__name__, static_folder="static", template_folder="templates")

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(product_api)

if __name__ == "__main__":
    app.run(debug=True)
