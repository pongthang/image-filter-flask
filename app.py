from flask import Flask
from flask_cors import CORS
from apis.product_apis import product_api
from routes.main import main_bp  # Importing blueprint

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(product_api)

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    app.run(debug=True)
