from app.seeders import run_face_seeder
from app.modules.face.models import Face
from app.modules.target.models import Target, TargetTag
from app.modules.target.services import save_target_from_dict


def test_save_target(client):
    """
    GIVEN a some target dict
    WHEN the target dict is saved
    THEN check that the target data is stored correctly
    """
    run_face_seeder()
    target_data = {
        "title": "Search target",
        "description": "John",
        "tags": ["tag1", "tag2", "tag3"],
        "faces": [face.uuid for face in Face.query.all()],
    }
    save_target_from_dict(target_data)
    target = Target.query.first()
    assert target.title == target_data["title"]
    assert target.description == target_data["description"]
    assert len(TargetTag.query.all()) == 3
    for tag_name in target_data["tags"]:
        assert TargetTag.query.filter_by(name=tag_name).first() is not None
    for face_uuid in target_data["faces"]:
        assert Face.query.get(face_uuid) is not None
