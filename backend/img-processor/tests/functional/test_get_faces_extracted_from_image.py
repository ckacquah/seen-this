import uuid

from conftest import client

from app.seeders import run_face_seeder
from app.modules.face.models import Face
from app.modules.image.models import Image


def test_get_faces_extracted_by_image(client):
    run_face_seeder()
    face = Face.query.first()
    image = face.parent
    response = client.get(f"image/{image.uuid}/faces")
    assert response.status_code == 200
    assert response.json[0]["uuid"] == face.uuid
    assert response.json[0]["score"] == face.score
    assert response.json[0]["file_uuid"] == face.file_uuid
    assert response.json[0]["parent_uuid"] == face.parent_uuid


def test_get_faces_extracted_by_image_returns_404_if_image_does_not_exist(client):
    response = client.get(f"image/{str(uuid.uuid4())}/faces")
    assert response.status_code == 404
    assert response.json["message"] == "Image not found"
