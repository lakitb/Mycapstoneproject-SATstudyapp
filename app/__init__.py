from flask import Flask, render_template

from .routes import bp as quiz_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key-change-me"
    app.register_blueprint(quiz_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template(
            "error.html",
            title="Page not found",
            message="The page you requested does not exist. Return home to start a quiz.",
        ), 404

    return app
