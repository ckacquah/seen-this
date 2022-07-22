import uuid

from conftest import client

from app.seeders import run_face_seeder
from app.modules.face.models import Face


def test_delete_face_by_id(client):
    run_face_seeder()
    for i, face in enumerate(Face.query.all()):
        response = client.delete(f"face/{str(face.uuid)}")
        assert response.status_code == 200
        assert response.json["message"] == "Face has been deleted successfully"
        assert Face.query.get(face.uuid) is None
        assert len(Face.query.all()) == 4 - i


def test_delete_face_by_id_returns_404_if_face_does_not_exist(client):
    response = client.delete(f"face/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Face not found"
