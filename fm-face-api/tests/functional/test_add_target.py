from flask import json

from api.utils.testing.seeders import run_face_seeder
from api.modules.face.models import Face
from api.modules.target.models import Target, TargetTag


TARGET_REQUEST_DATA = {
    "title": "Search target",
    "description": "John",
    "tags": ["tag1", "tag2", "tag3"],
    "faces": [],
}


def test_add_target(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target' is posted to (POST) with a valid target info
    THEN check that the response is valid and that target is created
         successfully
    """
    run_face_seeder()
    request_data = TARGET_REQUEST_DATA.copy()
    request_data.update(
        {
            "faces": [face.uuid for face in Face.query.all()],
        }
    )
    response = client.post(
        "/target",
        data=json.dumps(request_data),
        content_type="application/json",
    )
    target = Target.query.first()
    assert response.status_code == 201
    assert target.title == request_data["title"]
    assert target.description == request_data["description"]
    assert len(TargetTag.query.all()) == 3
    for tag_name in request_data["tags"]:
        assert TargetTag.query.filter_by(name=tag_name).first() is not None
    for face_uuid in request_data["faces"]:
        assert Face.query.get(face_uuid) is not None


def test_add_target_with_invalid_face_uuids(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target' is posted to (POST) without valid face uuids
    THEN check that a '400' status code is returned and no targets are created
    """
    request_data = TARGET_REQUEST_DATA.copy()
    request_data.update(
        {
            "faces": ["936dcdcd-9c65-4381-b36c-55ef4e139119"],
        }
    )
    response = client.post(
        "/target",
        data=json.dumps(request_data),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert (
        response.json["faces"]["0"][0]
        == "There is no face resource with a uuid of "
        "936dcdcd-9c65-4381-b36c-55ef4e139119"
    )
    assert len(Target.query.all()) == 0


def test_add_target_without_faces(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target' is posted to (POST) without faces
    THEN check that a '400' status code is returned and no targets are created
    """
    request_data = TARGET_REQUEST_DATA.copy()
    request_data.update(
        {
            "faces": None,
        }
    )
    response = client.post(
        "/target",
        data=json.dumps(request_data),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "faces" in response.json
    assert len(Target.query.all()) == 0


def test_add_target_without_title_and_description(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/target' is posted to (POST) without title and description
    THEN check that a '400' status code is returned and no targets are created
    """
    run_face_seeder()
    request_data = TARGET_REQUEST_DATA.copy()
    request_data.update(
        {
            "title": None,
            "description": None,
            "faces": [face.uuid for face in Face.query.all()],
        }
    )
    response = client.post(
        "/target",
        data=json.dumps(request_data),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "title" in response.json
    assert "description" in response.json
    assert len(Target.query.all()) == 0
