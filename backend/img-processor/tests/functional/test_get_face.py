import uuid

from conftest import client

from app.seeders import run_face_seeder
from app.modules.face.models import Face


def test_get_all_faces(client):
    run_face_seeder()
    faces = Face.query.all()
    response = client.get("face/")
    assert response.status_code == 200
    assert len(response.json) == len(faces)
    for i, face in enumerate(faces):
        assert response.json[i]["uuid"] == face.uuid
        assert response.json[i]["score"] == face.score
        assert response.json[i]["file_uuid"] == face.file_uuid
        assert response.json[i]["parent_uuid"] == face.parent_uuid


def test_get_all_faces_returns_nothing_if_db_is_empty(client):
    response = client.get("face/")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_face_by_id(client):
    run_face_seeder()
    face = Face.query.first()
    response = client.get(f"face/{face.uuid}")
    assert response.status_code == 200
    assert response.json["uuid"] == face.uuid
    assert response.json["score"] == face.score
    assert response.json["file_uuid"] == face.file_uuid
    assert response.json["parent_uuid"] == face.parent_uuid


def test_get_face_by_id_returns_404_if_face_does_not_exist(client):
    response = client.get(f"face/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Face not found"
