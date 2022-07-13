import os
import uuid
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename


from config import config
from app.utils import allowed_file
from app.tasks.extract_faces_from_image import extract_faces_from_image, celery
from app.modules.image.models import File, db, files_schema

UPLOAD_FOLDER = config.UPLOAD_FOLDER
CELERY_CONFIG = config.CELERY_CONFIG

image_controller = Blueprint("images", __name__, url_prefix="/images")


@image_controller.route("/")
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


@image_controller.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"message": "No image file part"}), 400

    file = request.files["image"]

    if file is None or file.filename == "":
        return jsonify({"message": "Image cannot be empty"}), 400

    if not allowed_file(filename=file.filename):
        return (
            jsonify(
                {
                    "message": "Only images can be uploaded",
                    "error": "Invalid file type",
                }
            ),
            400,
        )

    destination_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(destination_path)
    new_file = File(name=file.filename, size=file.content_length)
    db.session.add(new_file)
    db.session.commit()

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


@image_controller.route("/extract-faces", methods=["POST"])
def extract_faces():
    task = extract_faces_from_image.apply_async(
        args=({"image": request.json["image"], "backend": "retinaface"},)
    )
    return (
        jsonify({"task_id": task.id, "message": "Face extraction started successful"}),
        200,
    )


@image_controller.route("/task/<task_id>")
def task(task_id, methods=["GET"]):
    task_result = extract_faces_from_image.AsyncResult(task_id)
    return (
        jsonify(
            {
                "task_id": task_id,
                "task_state": task_result.state,
                "task_status": task_result.status,
                "task_result": task_result.result,
            }
        ),
        200,
    )
