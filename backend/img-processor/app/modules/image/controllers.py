import os
import uuid
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename


from config import config
from app.utils import allowed_file
from app.modules.image.models import Image
from app.modules.image.schemas import images_schema
from app.tasks.extract_faces_from_image import extract_faces_from_image, celery

UPLOAD_FOLDER = config.UPLOAD_FOLDER
CELERY_CONFIG = config.CELERY_CONFIG

image_controller = Blueprint("image", __name__, url_prefix="/image")


@image_controller.route("/", methods=["GET"])
def get_all_images():
    return jsonify(images_schema.dump(Image.query.all())), 200
