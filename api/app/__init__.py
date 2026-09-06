from flask import Flask
from api.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)