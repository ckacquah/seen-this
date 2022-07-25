import logging

# Import flask
from flask import Flask

# Import Flask Migrate
from flask_migrate import Migrate

# App Configuration
from config import config

# Import app models & blueprints
from app.seeders import run_seeds
from app.base_model import db, ma
from app.modules.face.controllers import face_blueprint
from app.modules.image.controllers import image_blueprint
from app.modules.target.controllers import target_blueprint


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
    Migrate(app, db)

    @app.cli.command("seed")
    def seed():
        run_seeds()

    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Not found"}, 404

    # Register blueprint(s)
    app.register_blueprint(face_blueprint)
    app.register_blueprint(image_blueprint)
    app.register_blueprint(target_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
