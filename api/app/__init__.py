from flask import Flask, jsonify

from config import Config
from connection import db
from .routes import posts_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(posts_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return jsonify({"message": "Post CRUD API is running"})

    return app
