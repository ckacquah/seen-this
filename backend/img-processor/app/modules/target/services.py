from app.base_model import db
from app.modules.face.models import Face
from app.modules.target.models import Target, TargetTag


def save_target_from_dict(target_data):
    tags = [TargetTag(name=tag_name) for tag_name in target_data["tags"]]
    faces = [
        Face.query.get(str(face_uuid)) for face_uuid in target_data["faces"]
    ]
    target = Target(
        tags=tags,
        faces=faces,
        title=target_data["title"],
        description=target_data["description"],
    )
    db.session.add(target)
    db.session.add_all(tags)
    db.session.commit()
