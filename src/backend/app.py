import os
import sys
from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Ensure we can import from src
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent))

# Load Env
load_dotenv()

FRONTEND_DIR = BASE_DIR.parent / "Frontend"
DB_PATH = BASE_DIR / "data.db"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    # Support both SQLite and other databases for Railway
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXP_MINUTES = 1440

def create_app():
    app = Flask(__name__, static_folder=str(FRONTEND_DIR))
    app.config.from_object(Config)
    CORS(app)

    try:
        from backend.models import db, User
        db.init_app(app)
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

    try:
        from backend.routes import auth, chef, customer, driver, admin, browse
        app.register_blueprint(auth.bp, url_prefix="/api")
        app.register_blueprint(chef.bp, url_prefix="/api/chef")
        app.register_blueprint(customer.bp, url_prefix="/api/customer")
        app.register_blueprint(driver.bp, url_prefix="/api/driver")
        app.register_blueprint(admin.bp, url_prefix="/api/admin")
        app.register_blueprint(browse.bp, url_prefix="/api/browse")
    except Exception as e:
        print(f"Error registering blueprints: {e}")
        raise

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")
            raise

    @app.route("/")
    def index(): 
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        try:
            if (Path(app.static_folder) / path).exists():
                return send_from_directory(app.static_folder, path)
        except Exception as e:
            print(f"Error serving static file {path}: {e}")
        return send_from_directory(app.static_folder, "index.html")

    return app

if __name__ == "__main__":
    try:
        from backend.socket_instance import socketio
        from backend import sockets
        
        app = create_app()
        socketio.init_app(app, cors_allowed_origins="*")
        
        # Get port from environment or default to 5000
        port = int(os.getenv("PORT", 5000))
        host = os.getenv("HOST", "0.0.0.0")
        debug = os.getenv("FLASK_DEBUG", "0") == "1"
        
        print(f"[OK] Server starting on http://{host}:{port}")
        socketio.run(app, debug=debug, port=port, host=host)
    except Exception as e:
        print(f"[ERROR] Server Error: {e}")
        import traceback
        traceback.print_exc()