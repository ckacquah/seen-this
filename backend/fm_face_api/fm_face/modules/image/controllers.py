from flask import Blueprint, jsonify, request, send_from_directory

from config import config
from fm_face.base_model import db
from fm_face.modules.face.models import Face
from fm_face.modules.face.schemas import faces_schema
from fm_face.modules.image.models import Image
from fm_face.modules.image.schemas import images_schema, image_schema
from fm_face.modules.image.services import save_uploaded_image

image_blueprint = Blueprint("image", __name__, url_prefix="/image")


@image_blueprint.route("/", methods=["GET"])
def get_all_images():
    return jsonify(images_schema.dump(Image.query.all())), 200


@image_blueprint.route("/<image_id>", methods=["GET"])
def get_image_by_id(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return jsonify({"message": "Image not found"}), 404
    return jsonify(image_schema.dump(image)), 200


@image_blueprint.route("/<image_id>", methods=["DELETE"])
def delete_image_by_id(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return jsonify({"message": "Image not found"}), 404
    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image has been deleted successfully"}), 200


@image_blueprint.route("/<image_id>/faces", methods=["GET"])
def get_faces_extracted_by_image(image_id):
    if Image.query.get(image_id) is None:
        return jsonify({"message": "Image not found"}), 404
    return (
        jsonify(faces_schema.dump(Face.query.filter_by(parent_uuid=image_id))),
        200,
    )


@image_blueprint.route("/upload", methods=["POST"])
def upload_image():
    if "image" in request.files:
        image_file = request.files["image"]
        results = save_uploaded_image(image_file)
        if results is not None:
            return jsonify(results), 201
    return jsonify({"message": "Failed to upload image"}), 400


@image_blueprint.route("/download/<filename>", methods=["GET"])
def download_image(filename):
    image = Image.query.filter_by(storage_name=filename).first()
    if image is None:
        return jsonify({"message": "Image not found"}), 404
    if image.source == "upload":
        return send_from_directory(config.UPLOAD_FOLDER, filename)
    elif image.source == "processed":
        return send_from_directory(config.PROCESSED_FACES_FOLDER, filename)
