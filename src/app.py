from flask import Flask, redirect, jsonify
import os
import logging
from pathlib import Path

def create_app(config=None):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    
    # Get absolute path to templates directory
    template_dir = Path(__file__).resolve().parents[1] / 'templates'
    
    app = Flask(__name__, 
                instance_relative_config=False,
                template_folder=str(template_dir))
    
    app.config.from_mapping(
        SECRET_KEY="change-me",
        DATABASE="feedback.db",
    )
    if config:
        app.config.update(config)

    # Import and register feedback blueprint; log if import fails
    try:
        from .api.feedback import bp as feedback_bp
        app.register_blueprint(feedback_bp, url_prefix="/api")
        app.logger.debug("Registered feedback blueprint at /api/feedback")
    except Exception:
        app.logger.exception("Failed to import/register feedback blueprint")

    # Optional: attempt to register other operator blueprints (don't crash app)
    optional_blueprints = ("operator_auth", "operator_feedback", "operator_actions")
    for name in optional_blueprints:
        try:
            mod = __import__(f"src.api.{name}", fromlist=["bp"])
            app.register_blueprint(mod.bp, url_prefix="/operator")
            app.logger.debug("Registered optional blueprint: %s", name)
        except ModuleNotFoundError:
            # missing optional module — debug note only, no stacktrace
            app.logger.debug("Optional blueprint %s not installed (skipping)", name)
        except Exception:
            # unexpected errors when importing/ registering should be visible
            app.logger.exception("Error registering optional blueprint %s", name)

    @app.route("/")
    def index():
        return redirect("/api/feedback")

    @app.route("/health")
    def health():
        return jsonify({
            "status": "ok",
            "database": app.config.get("DATABASE")
        }), 200

    return app