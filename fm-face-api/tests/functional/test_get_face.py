import uuid
from unittest.mock import Mock

from api.utils.testing.seeders import run_face_seeder
from api.modules.face.models import Face


def test_get_all_faces(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/face' is requested (GET)
    THEN check that the response is valid
    """
    run_face_seeder()

    mock_faces_schema_dump = Mock(return_value=[])

    monkeypatch.setattr(
        "api.modules.face.controllers.faces_schema.dump",
        mock_faces_schema_dump,
    )

    faces = Face.query.all()
    response = client.get("face/")

    mock_faces_schema_dump.assert_called_once_with(faces)

    assert response.status_code == 200
    assert response.json == []


def test_get_all_faces_returns_nothing_if_db_is_empty(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/face' is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("face/")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_face_by_id(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/face/<face_id>' is requested (GET) with face_id that exist
    THEN check that the response is valid
    """
    run_face_seeder()

    mock_face_schema_dump = Mock(return_value={})

    monkeypatch.setattr(
        "api.modules.face.controllers.face_schema.dump",
        mock_face_schema_dump,
    )

    face = Face.query.first()
    response = client.get(f"face/{face.uuid}")

    mock_face_schema_dump.assert_called_once_with(face)

    assert response.status_code == 200
    assert response.json == {}


def test_get_face_by_id_returns_404_if_face_does_not_exist(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/face/<face_id>' is requested (GET) with face_id that does
         not exist
    THEN check that a '404' status code is returned
    """
    response = client.get(f"face/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Face not found"
