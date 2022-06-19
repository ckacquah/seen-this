import os
import random
import string
from datetime import datetime

from config import ALLOWED_EXTENSIONS, PROCESSED_FACES_FOLDER, UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_processed_face_path(filename):
    return os.path.join(PROCESSED_FACES_FOLDER, filename)


def get_uploaded_file_path(filename):
    return os.path.join(UPLOAD_FOLDER, filename)


def generate_random_file_name(size):
    return (
        str(datetime.now()).replace(" ", "_").replace(":", "-")
        + "_"
        + "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(size)
        )
    )
