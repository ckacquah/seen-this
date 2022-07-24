from app.base_model import ma
from app.modules.face.schemas import FaceSchema


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
