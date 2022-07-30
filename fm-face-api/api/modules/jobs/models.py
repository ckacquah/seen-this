from api.base_model import BaseModel, db
from api.modules.image.models import Image


face_extraction_job_association = db.Table(
    "face_extraction_job_association",
    db.Column(
        "face_extraction_job_uuid",
        db.String,
        db.ForeignKey("face_extraction_job.uuid"),
        primary_key=True,
    ),
    db.Column(
        "face_uuid",
        db.String,
        db.ForeignKey("face.uuid"),
        primary_key=True,
    ),
)


class Job(BaseModel):
    __abstract__ = True

    status = db.Column(db.String(255), nullable=False)
    celery_task_id = db.Column(db.String(255))
    percentage_complete = db.Column(db.Integer, nullable=False)
    completion_time = db.Column(db.DateTime)


class FaceExtractionJob(Job):
    image_uuid = db.Column(
        db.String(255), db.ForeignKey(Image.uuid), nullable=False
    )
    image = db.relationship(Image, foreign_keys=[image_uuid])
    results = db.relationship(
        "Face",
        secondary=face_extraction_job_association,
        lazy="subquery",
        backref=db.backref("jobs", lazy=True),
    )
