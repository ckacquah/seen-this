from app.base_model import BaseModel, db


tagert_tag_association = db.Table(
    "tagert_tag_association",
    db.Column(
        "target_uuid",
        db.String,
        db.ForeignKey("target.uuid"),
        primary_key=True,
    ),
    db.Column(
        "target_tag_uuid",
        db.String,
        db.ForeignKey("target_tag.uuid"),
        primary_key=True,
    ),
)

face_target_association = db.Table(
    "face_target_association",
    db.Column(
        "target_uuid",
        db.String,
        db.ForeignKey("target.uuid"),
        primary_key=True,
    ),
    db.Column(
        "face_uuid",
        db.String,
        db.ForeignKey("face.uuid"),
        primary_key=True,
    ),
)


class Target(BaseModel):
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    results_uuid = db.Column(db.String(255))
    faces = db.relationship(
        "Face",
        secondary=face_target_association,
        lazy="subquery",
        backref=db.backref("targets", lazy=True),
    )
    tags = db.relationship(
        "TargetTag", secondary=tagert_tag_association, back_populates="targets"
    )


class TargetTag(BaseModel):
    name = db.Column(db.String(255), nullable=False)
    targets = db.relationship(
        "Target", secondary=tagert_tag_association, back_populates="tags"
    )
