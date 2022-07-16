import uuid
import pytest

from conftest import client

from app.seeders import run_face_seeder
from app.modules.face.models import Face
from app.modules.face.schemas import faces_schema, face_schema


def test_get_all_faces_returns_faces_stored_in_db(client):
    run_face_seeder()
    response = client.get("face/")
    assert response.status_code == 200
    assert len(response.json) == 5
    assert len(Face.query.all()) == 5
    assert faces_schema.dump(Face.query.all()) == response.json


def test_get_all_faces_returns_nothing_if_db_is_empty(client):
    response = client.get("face/")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_face_by_id(client):
    run_face_seeder()
    for face in Face.query.all():
        response = client.get(f"face/{face.uuid}")
        assert response.status_code == 200
        assert face_schema.dump(face) == response.json


def test_get_face_by_id_returns_404_if_face_does_not_exist(client):
    response = client.get(f"face/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Face not found"


def test_delete_face_by_id(client):
    run_face_seeder()
    for index, face in enumerate(Face.query.all()):
        response = client.delete(f"face/{str(face.uuid)}")
        assert response.status_code == 200
        assert len(Face.query.all()) == 5 - index - 1
        assert Face.query.get(face.uuid) is None
        assert response.json["message"] == "Face has been deleted successfully"


def test_delete_face_by_id_returns_404_if_face_does_not_exist(client):
    response = client.delete(f"face/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json["message"] == "Face not found"
