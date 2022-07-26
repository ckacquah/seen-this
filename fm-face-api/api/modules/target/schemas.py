from marshmallow import fields, validate, ValidationError

from api.base_model import ma
from api.modules.face.models import Face
from api.modules.face.schemas import FaceSchema


class TagSchema(ma.Schema):
    class Meta:
        fields = ("name",)


class TargetSchema(ma.Schema):
    class Meta:
        fields = (
            "uuid",
            "title",
            "description",
            "results_uuid",
            "tags",
            "faces",
            "created_at",
            "updated_at",
        )

    tags = ma.Nested(TagSchema, many=True)
    faces = ma.Nested(FaceSchema, many=True)


target_schema = TargetSchema()
targets_schema = TargetSchema(many=True)


def validate_face(face_uuid):
    if Face.query.get(str(face_uuid)) is None:
        raise ValidationError(
            f"There is no face resource with a uuid of {face_uuid}"
        )


class AddTargetRequestSchema(ma.Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    tags = fields.List(
        fields.Str(required=True),
        validate=validate.Length(min=0),
        required=False,
    )

    faces = fields.List(
        fields.UUID(required=True, validate=validate_face),
        validate=validate.Length(min=1),
        required=True,
    )


add_target_reqeust_schema = AddTargetRequestSchema()
