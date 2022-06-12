
import logging
import click
# Import flask and template operators
from flask import Flask, render_template
from flask.cli import with_appcontext

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import Flask Migrate
from flask_migrate import Migrate

# Import app models & blueprints
from app.models import db
from app.seeders import run_seeds
from app.tasks import celery
from app.modules.image_handler.controllers import image_handler


# Select logging level for the running instance of the application
logging.basicConfig(level=logging.DEBUG)

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Handling database ORM
db.init_app(app)

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
