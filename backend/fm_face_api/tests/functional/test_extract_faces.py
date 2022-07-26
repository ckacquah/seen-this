import uuid
from unittest.mock import Mock

from fm_face.modules.jobs.models import FaceExtractionJob
from fm_face.modules.image.models import Image
from fm_face.utils.testing.seeders import run_image_seeder


def test_start_face_extraction_job(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/<image_id>/extract-faces' is posted to (POST) with valid
         image_id
    THEN check that response is valid
    """
    run_image_seeder()
    image = Image.query.first()

    class FakeTaskResult:
        id = "fake-task-id"

    mock_extract_faces_from_image_apply_async = Mock(
        return_value=FakeTaskResult()
    )

    monkeypatch.setattr(
        "fm_face.modules.image.controllers."
        "extract_faces_from_image.apply_async",
        mock_extract_faces_from_image_apply_async,
    )

    response = client.post(f"/image/{image.uuid}/extract-faces")
    job = FaceExtractionJob.query.first()

    mock_extract_faces_from_image_apply_async.assert_called_once_with(
        args=(image.uuid,),
    )

    assert response.status_code == 201
    assert response.json["status"] == "started"
    assert response.json["image_uuid"] == image.uuid
    assert response.json["completion_time"] is None
    assert response.json["percentage_complete"] == 0
    assert job.uuid == response.json["uuid"]
    assert job.status == "started"
    assert job.image_uuid == image.uuid
    assert job.celery_task_id == "fake-task-id"
    assert job.completion_time is None
    assert job.percentage_complete == 0


def test_start_face_extraction_job_with_invalid_image_id(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/<image_id>/extract-faces' is posted to (POST) with invalid
         image_id
    THEN check that a '404' status code is returned and no job is created
    """

    class FakeTaskResult:
        id = "fake-task-id"

    mock_extract_faces_from_image_apply_async = Mock(
        return_value=FakeTaskResult()
    )

    monkeypatch.setattr(
        "fm_face.modules.image.controllers."
        "extract_faces_from_image.apply_async",
        mock_extract_faces_from_image_apply_async,
    )

    response = client.post(f"/image/{str(uuid.uuid4())}/extract-faces")
    job = FaceExtractionJob.query.filter_by(
        celery_task_id="fake-task-id"
    ).first()

    mock_extract_faces_from_image_apply_async.assert_not_called()

    assert response.status_code == 404
    assert response.json["message"] == "Image not found"
    assert job is None
