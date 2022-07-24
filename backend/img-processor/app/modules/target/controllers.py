from flask import Blueprint, jsonify

from app.modules.target.models import Target
from app.modules.target.schemas import targets_schema, target_schema

target_controller = Blueprint("target", __name__, url_prefix="/target")


@target_controller.route("/", methods=["GET"])
def get_all_targets():
    return jsonify(targets_schema.dump(Target.query.all())), 200


@target_controller.route("/<target_id>", methods=["GET"])
def get_target_by_id(target_id):
    target = Target.query.get(target_id)
    if target is None:
        return jsonify({"message": "Target resource not found"}), 404
    return jsonify(target_schema.dump(target)), 200
