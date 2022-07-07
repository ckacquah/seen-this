from marshmallow import Schema, fields, validate


class ExtractFacesFromImagesRequestSchema(Schema):
    backend = fields.Str(
        validate=validate.OneOf(
            ["opencv", "ssd", "dlib", "mtcnn", "retinaface", "mediapipe"]
        ),
        required=True,
    )
    targets = fields.List(fields.Str, required=True)
