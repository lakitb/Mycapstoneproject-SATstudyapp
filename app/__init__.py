from flask import Flask

from .routes import bp as quiz_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key-change-me"
    app.register_blueprint(quiz_bp)
    return app
