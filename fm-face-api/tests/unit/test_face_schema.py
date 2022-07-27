from api.modules.face.schemas import (
    face_schema,
    faces_schema,
    facial_area_schema,
)
from api.utils.testing.faker import (
    generate_fake_faces,
    generate_fake_facial_areas,
)


def test_face_schema():
    """
    GIVEN a Face object
    WHEN the object is dumped
    THEN check that the dictionary is valid
    """

    face = generate_fake_faces(1)[0]
    face_dict = face_schema.dump(face)

    assert face_dict["uuid"] == face.uuid
    assert face_dict["score"] == face.score
    assert face_dict["facial_area"]["x1"] == face.facial_area.x1
    assert face_dict["facial_area"]["x2"] == face.facial_area.x2
    assert face_dict["facial_area"]["y1"] == face.facial_area.y1
    assert face_dict["facial_area"]["y2"] == face.facial_area.y2


def test_face_schemas():
    """
    GIVEN a list of Face objects
    WHEN the list is dumped
    THEN check that the results is valid
    """

    faces = generate_fake_faces(3)
    faces_list = faces_schema.dump(faces)

    for face_dict, face in zip(faces_list, faces):
        assert face_dict["uuid"] == face.uuid
        assert face_dict["score"] == face.score
        assert face_dict["facial_area"]["x1"] == face.facial_area.x1
        assert face_dict["facial_area"]["x2"] == face.facial_area.x2
        assert face_dict["facial_area"]["y1"] == face.facial_area.y1
        assert face_dict["facial_area"]["y2"] == face.facial_area.y2


def test_facial_area_schema():
    """
    GIVEN a FacialArea object
    WHEN the object is dumped
    THEN check that the dictionary is valid
    """

    facial_area = generate_fake_facial_areas(1)[0]
    facial_area_dict = facial_area_schema.dump(facial_area)

    assert facial_area_dict["x1"] == facial_area.x1
    assert facial_area_dict["x2"] == facial_area.x2
    assert facial_area_dict["y1"] == facial_area.y1
    assert facial_area_dict["y2"] == facial_area.y2
