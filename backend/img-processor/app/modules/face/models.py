from app.base_model import BaseModel, db
from app.modules.image.models import Image


class FacialArea(BaseModel):
    x1 = db.Column(db.Integer, nullable=False)
    x2 = db.Column(db.Integer, nullable=False)
    y1 = db.Column(db.Integer, nullable=False)
    y2 = db.Column(db.Integer, nullable=False)


class Face(BaseModel):
    score = db.Column(db.Integer, nullable=False)
    file_uuid = db.Column(db.String(255), db.ForeignKey(Image.uuid))
    parent_uuid = db.Column(db.String(255), db.ForeignKey(Image.uuid))
    facial_area_uuid = db.Column(
        db.String(255), db.ForeignKey(FacialArea.uuid)
    )
    file = db.relationship(Image, foreign_keys=[file_uuid])
    parent = db.relationship(Image, foreign_keys=[parent_uuid])
    facial_area = db.relationship(FacialArea, foreign_keys=[facial_area_uuid])
