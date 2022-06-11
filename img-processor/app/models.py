from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    '''
    Define a base model for other database tables to inherit
    '''
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
