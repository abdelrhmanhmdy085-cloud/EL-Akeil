el_akeil = "مرحبا بالعالم"
print(el_akeil)

import os
import logging
from pathlib import Path
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

# ===============================
# CONFIG
# ===============================
class Config:
    DEBUG = False
    TESTING = False
    HOST = "0.0.0.0"
    PORT = 5000
    LOG_LEVEL = logging.INFO

    # تحديد مسار frontend/dist بشكل صحيح
    BASE_DIR = Path(__file__).resolve().parent  # backend folder
    STATIC_FOLDER = str(BASE_DIR.parent / "frontend" / "dist")


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.INFO


# ===============================
# APP FACTORY
# ===============================
def create_app():
    env = os.environ.get("APP_ENV", "production").lower()
    cfg = DevelopmentConfig if env == "development" else ProductionConfig

    app = Flask(__name__, static_folder=cfg.STATIC_FOLDER, static_url_path="/")
    app.config.from_object(cfg)
    CORS(app)

    logging.basicConfig(
        level=app.config["LOG_LEVEL"],
        format="%(asctime)s %(levelname)s %(message)s"
    )

    # بيانات مؤقتة
    DISHES = [
        {"id": 1, "name": "كشري", "price": 45, "preparationTime": 20},
        {"id": 2, "name": "فتة", "price": 55, "preparationTime": 30},
    ]

    # ===============================
    # API ROUTES
    # ===============================
    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/api/dishes", methods=["GET"])
    def list_dishes():
        return jsonify(DISHES)

    @app.route("/api/dishes", methods=["POST"])
    def create_dish():
        data = request.get_json() or {}
        if not data.get("name") or not data.get("price"):
            return jsonify({"error": "name and price required"}), 400

        new_id = max([d["id"] for d in DISHES] or [0]) + 1
        dish = {
            "id": new_id,
            "name": data["name"],
            "price": data["price"],
            "preparationTime": data.get("preparationTime", 20)
        }
        DISHES.append(dish)
        return jsonify(dish), 201

    # ===============================
    # FRONTEND ROUTE
    # ===============================
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        static_dir = Path(app.static_folder)

        # لو ملف موجود جوه dist
        target = static_dir / path
        if static_dir.exists() and path and target.exists():
            return send_from_directory(app.static_folder, path)

        # رجّع index.html
        index_file = static_dir / "index.html"
        if index_file.exists():
            return send_from_directory(app.static_folder, "index.html")

        return jsonify({"message": "Backend only. No frontend found."})

    return app


# ===============================
# START APP
# ===============================
app = create_app()

logging.getLogger().setLevel(app.config.get("LOG_LEVEL", logging.INFO))
logging.info("APP ENV = %s", os.environ.get("APP_ENV", "production"))
logging.info("Static folder: %s", app.static_folder)

if __name__ == "__main__":
    logging.info("Starting server on %s:%s (DEBUG=%s)",
                 app.config["HOST"], app.config["PORT"], app.config["DEBUG"])
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
    x