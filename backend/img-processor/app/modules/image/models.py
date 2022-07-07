from app.base_model import BaseModel, db, ma


class File(BaseModel):
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)


class FileSchema(ma.Schema):
    class Meta:
        fields = ("uuid", "name", "size", "created_at", "updated_at")


file_schema = FileSchema()
files_schema = FileSchema(many=True)


class Face(BaseModel):
    score = db.Column(db.Integer, nullable=False)
    file_uuid = db.Column(db.String, db.ForeignKey("file.uuid"))
    parent_uuid = db.Column(db.String, db.ForeignKey("file.uuid"))
    file = db.relationship("File", foreign_keys=[file_uuid])
    parent = db.relationship("File", foreign_keys=[parent_uuid])


class FaceSchema(ma.Schema):
    class Meta:
        fields = ("uuid", "file", "parent", "score", "created_at", "updated_at")
        include_fk = True

    file = ma.Nested(FileSchema)
    parent = ma.Nested(FileSchema)


face_schema = FaceSchema()
faces_schema = FaceSchema(many=True)
