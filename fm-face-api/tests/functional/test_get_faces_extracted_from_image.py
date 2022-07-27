import uuid
from unittest.mock import Mock


from api.utils.testing.seeders import run_face_seeder
from api.modules.face.models import Face


def test_get_faces_extracted_by_image(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>/faces' is requested (GET) with image_id
        that exist
    THEN check that the response is valid
    """
    run_face_seeder()

    mock_faces_schema_dump = Mock(return_value=[])

    monkeypatch.setattr(
        "api.modules.image.controllers.faces_schema.dump",
        mock_faces_schema_dump,
    )

    face = Face.query.first()
    image = face.parent
    response = client.get(f"image/{image.uuid}/faces")

    mock_faces_schema_dump.assert_called_once()

    assert response.status_code == 200
    assert response.json == []


def test_get_faces_extracted_by_image_with_unknown_image_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>/faces' is requested (GET) with image_id
        that does
        not exist
    THEN check that a '404' status code is returned
    """
    response = client.get(f"image/{str(uuid.uuid4())}/faces")
    assert response.status_code == 404
    assert response.json["message"] == "Image not found"
