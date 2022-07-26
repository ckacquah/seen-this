from fm_face.base_model import BaseModel, db


class Job(BaseModel):
    tag = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    celery_task_id = db.Column(db.String(255), nullable=False)
    percentage_complete = db.Column(db.Integer, nullable=False)
    completion_time = db.Column(db.DateTime)
