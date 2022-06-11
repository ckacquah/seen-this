from flask import Flask
from app.utils.celery import make_celery

# Define the WSGI application object
flask_app = Flask(__name__)

# Configurations
flask_app.config.from_object('config')

celery = make_celery(flask_app)
