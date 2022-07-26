from flask import Blueprint, jsonify

from api.base_model import db
from api.modules.face.models import Face
from api.modules.face.schemas import faces_schema, face_schema

face_blueprint = Blueprint("face", __name__, url_prefix="/face")


@face_blueprint.route("/", methods=["GET"])
def get_all_faces():
    return jsonify(faces_schema.dump(Face.query.all())), 200


@face_blueprint.route("/<face_id>", methods=["GET"])
def get_face_by_id(face_id):
    face = Face.query.get(face_id)
    if face is None:
        return jsonify({"message": "Face not found"}), 404
    return jsonify(face_schema.dump(face)), 200


@face_blueprint.route("/<face_id>", methods=["DELETE"])
def delete_face_by_id(face_id):
    face = Face.query.get(face_id)
    if face is None:
        return jsonify({"message": "Face not found"}), 404
    db.session.delete(face)
    db.session.commit()
    return jsonify({"message": "Face has been deleted successfully"}), 200
