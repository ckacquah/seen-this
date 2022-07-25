from fm_face.base_model import ma


class ImageSchema(ma.Schema):
    class Meta:
        fields = (
            "uuid",
            "name",
            "size",
            "width",
            "height",
            "source",
            "storage_name",
            "created_at",
            "updated_at",
        )


image_schema = ImageSchema()
images_schema = ImageSchema(many=True)
