from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.base_model import db
from app.modules.target.services import save_target_from_dict
from app.modules.target.models import Target
from app.modules.target.schemas import (
    targets_schema,
    target_schema,
    add_target_reqeust_schema,
)

target_controller = Blueprint("target", __name__, url_prefix="/target")


@target_controller.route("", methods=["GET"])
def get_all_targets():
    return jsonify(targets_schema.dump(Target.query.all())), 200


@target_controller.route("", methods=["POST"])
def add_target():
    try:
        target_data = add_target_reqeust_schema.load(request.json)
        save_target_from_dict(target_data)
        return "", 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@target_controller.route("/<target_id>", methods=["GET"])
def get_target_by_id(target_id):
    target = Target.query.get(target_id)
    if target is None:
        return jsonify({"message": "Target resource not found"}), 404
    return jsonify(target_schema.dump(target)), 200


@target_controller.route("/<target_id>", methods=["DELETE"])
def delete_target_by_id(target_id):
    target = Target.query.get(target_id)
    if target is None:
        return jsonify({"message": "target not found"}), 404
    db.session.delete(target)
    db.session.commit()
    return jsonify({"message": "target has been deleted successfully"}), 200
