from app.base_model import BaseModel, db


class Image(BaseModel):
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(255), nullable=False)
    storage_name = db.Column(db.String(255), nullable=False)
