from app.models import BaseModel, db, ma


class File(BaseModel):
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return "Name=%s, Age=%d" % (self.name, self.age)


class FileSchema(ma.Schema):
    class Meta:
        fields = ("uuid", "name", "size", "created_at", "updated_at")


file_schema = FileSchema()
files_schema = FileSchema(many=True)
