
from app.models import BaseModel, db


class File(BaseModel):
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer(), nullable=False)

    def __str__(self):
        return "Name=%s, Age=%d" % (self.name, self.age)
