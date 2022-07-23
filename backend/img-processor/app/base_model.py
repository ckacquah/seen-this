from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.utils import generate_uuid

db = SQLAlchemy()
ma = Marshmallow()


class BaseModel(db.Model):
    """
    Define a base model for other database tables to inherit
    """

    __abstract__ = True

    uuid = db.Column(db.String, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
