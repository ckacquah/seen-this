import os
import uuid
import pytest

from conftest import client

from app.seeders import run_face_seeder
from app.modules.face.models import Face
from app.modules.face.schemas import face_schema


def test_get_all_faces_returns_faces_stored_in_db(client):
    run_face_seeder()
    response = client.get("face/")
    assert response.status_code == 200
    assert len(response.json) == 5
    assert len(Face.query.all()) == 5
    for face_in_db, face_in_reponse in zip(Face.query.all(), response.json):
        assert face_in_db is not None
        assert face_in_reponse is not None
        assert face_schema.dump(face_in_db) == face_in_reponse
