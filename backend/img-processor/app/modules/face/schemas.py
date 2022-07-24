from app.base_model import ma


class FacialAreaSchema(ma.Schema):
    class Meta:
        fields = ("x1", "x2", "y1", "y2")


facial_area_schema = FacialAreaSchema()
facial_areas_schema = FacialAreaSchema(many=True)


class FaceSchema(ma.Schema):
    class Meta:
        fields = (
            "uuid",
            "score",
            "image_uuid",
            "parent_uuid",
            "facial_area",
            "created_at",
            "updated_at",
        )
        include_fk = True

    facial_area = ma.Nested(FacialAreaSchema)


face_schema = FaceSchema()
faces_schema = FaceSchema(many=True)
