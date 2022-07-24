import os
import uuid
from datetime import datetime

from config import config

UPLOAD_FOLDER = config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS
PROCESSED_FACES_FOLDER = config.PROCESSED_FACES_FOLDER


def is_allowed_image_name(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_processed_file_path(filename):
    return os.path.join(PROCESSED_FACES_FOLDER, filename)


def get_uploaded_file_path(filename):
    return os.path.join(UPLOAD_FOLDER, filename)


def generate_uuid():
    return str(uuid.uuid4())


def generate_random_filename(extension=""):
    return (
        str(datetime.now()).replace(" ", "_").replace(":", "-")
        + "_"
        + generate_uuid()
        + "."
        + extension
    )
