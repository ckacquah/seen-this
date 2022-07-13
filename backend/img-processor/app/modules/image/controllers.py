from flask import Blueprint, jsonify

from app.base_model import db
from app.modules.image.models import Image
from app.modules.image.schemas import images_schema, image_schema

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
