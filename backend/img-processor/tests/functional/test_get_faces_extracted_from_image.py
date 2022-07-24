import uuid

from app.seeders import run_face_seeder
from app.modules.face.models import Face


def test_get_faces_extracted_by_image(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>/faces' is requested (GET) with image_id
        that exist
    THEN check that the response is valid
    """
    run_face_seeder()
    face = Face.query.first()
    image = face.parent
    response = client.get(f"image/{image.uuid}/faces")
    assert response.status_code == 200
    assert response.json[0]["uuid"] == face.uuid
    assert response.json[0]["score"] == face.score
    assert response.json[0]["image_uuid"] == face.image_uuid
    assert response.json[0]["parent_uuid"] == face.parent_uuid


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
