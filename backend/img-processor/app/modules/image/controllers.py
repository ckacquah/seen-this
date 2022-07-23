import os

from flask import Blueprint, jsonify, request, send_file

from app.base_model import db
from app.utils import get_uploaded_file_path
from app.modules.face.models import Face
from app.modules.face.schemas import faces_schema
from app.modules.image.models import Image
from app.modules.image.schemas import images_schema, image_schema
from app.modules.image.services import save_uploaded_image

image_controller = Blueprint("image", __name__, url_prefix="/image")


@image_controller.route("/", methods=["GET"])
def get_all_images():
    return jsonify(images_schema.dump(Image.query.all())), 200


@image_controller.route("/<image_id>", methods=["GET"])
def get_image_by_id(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return jsonify({"message": "Image not found"}), 404
    return jsonify(image_schema.dump(image)), 200


@image_controller.route("/<image_id>", methods=["DELETE"])
def delete_image_by_id(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return jsonify({"message": "Image not found"}), 404
    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image has been deleted successfully"}), 200


@image_controller.route("/<image_id>/faces", methods=["GET"])
def get_faces_extracted_by_image(image_id):
    if Image.query.get(image_id) is None:
        return jsonify({"message": "Image not found"}), 404
    return (
        jsonify(faces_schema.dump(Face.query.filter_by(parent_uuid=image_id))),
        200,
    )


@image_controller.route("/upload", methods=["POST"])
def upload_image():
    if "image" in request.files:
        image_file = request.files["image"]
        results = save_uploaded_image(
            image_file.filename, image_file.stream.read()
        )
        if results is not None:
            return jsonify(results), 201
    return jsonify({"message": "Failed to upload image"}), 400


@image_controller.route("/download/<filename>", methods=["GET"])
def download_image(filename):
    uploaded_image_path = get_uploaded_file_path(filename)
    if os.path.exists(uploaded_image_path):
        return send_file(uploaded_image_path)
    return jsonify({"message": "Image not found"}), 404
