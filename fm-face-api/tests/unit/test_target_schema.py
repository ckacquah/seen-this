from api.modules.target.schemas import target_schema, targets_schema
from api.utils.testing.faker import generate_fake_targets


def test_target_schema():
    """
    GIVEN a Target object
    WHEN the object is dumped
    THEN check that the dictionary is valid
    """
    target = generate_fake_targets(1)[0]
    target_dict = target_schema.dump(target)

    assert target_dict["uuid"] == target.uuid
    assert target_dict["title"] == target.title
    assert target_dict["description"] == target.description
    assert target_dict["created_at"] == target.created_at
    assert target_dict["updated_at"] == target.updated_at
    assert target_dict["results_uuid"] == target.results_uuid

    for tag_dict, tag in zip(target_dict["tags"], target.tags):
        assert tag_dict["name"] == tag.name

    for face_dict, face in zip(target_dict["faces"], target.faces):
        assert face_dict["uuid"] == face.uuid
        assert face_dict["score"] == face.score
        assert face_dict["facial_area"]["x1"] == face.facial_area.x1
        assert face_dict["facial_area"]["x2"] == face.facial_area.x2
        assert face_dict["facial_area"]["y1"] == face.facial_area.y1
        assert face_dict["facial_area"]["y2"] == face.facial_area.y2


def test_target_schemas():
    """
    GIVEN a list of Target objects
    WHEN the list is dumped
    THEN check that the results is valid
    """
    targets = generate_fake_targets(3)
    targets_list = targets_schema.dump(targets)

    for target_dict, target in zip(targets_list, targets):

        assert target_dict["uuid"] == target.uuid
        assert target_dict["title"] == target.title
        assert target_dict["description"] == target.description
        assert target_dict["created_at"] == target.created_at
        assert target_dict["updated_at"] == target.updated_at
        assert target_dict["results_uuid"] == target.results_uuid

        for tag_dict, tag in zip(target_dict["tags"], target.tags):
            assert tag_dict["name"] == tag.name

        for face_dict, face in zip(target_dict["faces"], target.faces):
            assert face_dict["uuid"] == face.uuid
            assert face_dict["score"] == face.score
            assert face_dict["facial_area"]["x1"] == face.facial_area.x1
            assert face_dict["facial_area"]["x2"] == face.facial_area.x2
            assert face_dict["facial_area"]["y1"] == face.facial_area.y1
            assert face_dict["facial_area"]["y2"] == face.facial_area.y2
