from flask import Blueprint, jsonify

from app.base_model import db
from app.modules.face.models import Face
from app.modules.face.schemas import faces_schema

face_controller = Blueprint("face", __name__, url_prefix="/face")


@face_controller.route("/", methods=["GET"])
def get_all_faces():
    return jsonify(faces_schema.dump(Face.query.all())), 200
