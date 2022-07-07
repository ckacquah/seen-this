import logging

# Import flask
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import Flask Migrate
from flask_migrate import Migrate

# App Configuration
from config import config

# Import app models & blueprints
from app.tasks import celery
from app.seeders import run_seeds
from app.base_model import db, ma
from app.modules.image.controllers import image_handler


# Select logging level for the running instance of the application
logging.basicConfig(level=logging.DEBUG)


def create_app(config=config):
    # Define the WSGI application object
    app = Flask(__name__)

    # Configurations
    app.config.from_object(config)

    # Handling database ORM
    db.init_app(app)

    # Handling Marshmallow
    ma.init_app(app)

    # Handling database migrations
    migrate = Migrate(app, db)

    @app.cli.command("seed")
    def seed():
        run_seeds()

    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Not found"}, 404

    # Register blueprint(s)
    app.register_blueprint(image_handler)

    return app


if __name__ == "__main__":
    app = create_app()
