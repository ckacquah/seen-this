from api.base_model import BaseModel, db


class Job(BaseModel):
    __abstract__ = True

    status = db.Column(db.String(255), nullable=False)
    celery_task_id = db.Column(db.String(255), nullable=False)
    percentage_complete = db.Column(db.Integer, nullable=False)
    completion_time = db.Column(db.DateTime)


class FaceExtractionJob(Job):
    image_uuid = db.Column(db.String(255), nullable=False)
