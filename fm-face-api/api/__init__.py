import logging

# Import flask
from flask import Flask

# Import Flask Migrate
from flask_migrate import Migrate

# App Configuration
from config import config

# Import app models & blueprints
from api.base_model import db, ma
from api.modules.jobs.controllers import extraction_jobs_blueprint
from api.modules.face.controllers import face_blueprint
from api.modules.image.controllers import image_blueprint
from api.modules.target.controllers import target_blueprint


# Select logging level for the running instance of the application
logging.basicConfig(level=logging.DEBUG)


def create_app(config=config):
    # Define the WSGI application object
    api = Flask(__name__)

    # Configurations
    api.config.from_object(config)

    # Handling database ORM
    db.init_app(api)

    # Handling Marshmallow
    ma.init_app(api)

    # Handling database migrations
    Migrate(api, db)

    @api.errorhandler(404)
    def not_found(error):
        return {"message": "Not found"}, 404

    # Register blueprint(s)
    api.register_blueprint(face_blueprint)
    api.register_blueprint(image_blueprint)
    api.register_blueprint(target_blueprint)
    api.register_blueprint(extraction_jobs_blueprint)

    return api


if __name__ == "__main__":
    app = create_app()
