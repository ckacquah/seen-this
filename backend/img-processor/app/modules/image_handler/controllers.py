import os
import uuid
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER
from app.tasks import celery
from app.tasks.demo import demo
from app.utils import allowed_file
from app.modules.image_handler.models import File, db, files_schema

image_handler = Blueprint("images", __name__, url_prefix="/images")


@image_handler.route("/")
def index():
    images = File.query.all()
    return (
        jsonify(
            {
                "message": "Images retrieved successfully",
                "images": files_schema.dump(images),
            }
        ),
        200,
    )


@image_handler.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return jsonify({"message": "No image file part"}), 400

    file = request.files["image"]

    if file.filename == "" or file is None:
        return jsonify({"message": "Image cannot be empty"}), 400

    if allowed_file(filename=file.filename):
        destination_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(destination_path)
        new_file = File(name=file.filename, size=file.content_length)
        db.session.add(new_file)
        db.session.commit()
    else:
        return (
            jsonify(
                {
                    "message": "Only images can be uploaded",
                    "error": "Invalid file type",
                }
            ),
            400,
        )

    return (
        jsonify(
            {
                "message": "Image uploaded successfully",
                "image_name": file.filename,
                "uuid": new_file.uuid,
            }
        ),
        200,
    )


@image_handler.route("/task/<task_id>")
def task(task_id, methods=["GET"]):
    print(task_id)
    task_result = celery.AsyncResult(task_id)
    return (
        jsonify(
            {
                "task_id": task_id,
                "task_status": task_result.status,
                "task_result": task_result.result,
            }
        ),
        200,
    )
