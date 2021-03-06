import uuid
from unittest.mock import Mock

from api.modules.jobs.models import FaceExtractionJob
from api.modules.image.models import Image
from api.utils.testing.seeders import run_image_seeder, run_job_seeder


class FakeTaskResult:
    id = "fake-task-id"


def test_start_face_extraction_job(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>/extract-faces' is posted to (POST) with valid
         image_id
    THEN check that response is valid
    """
    run_image_seeder()
    image = Image.query.first()

    mock_face_extraction_job_schema_dump = Mock(return_value={})
    mock_extract_faces_from_image_apply_async = Mock(
        return_value=FakeTaskResult()
    )

    monkeypatch.setattr(
        "api.modules.image.controllers.face_extraction_job_schema.dump",
        mock_face_extraction_job_schema_dump,
    )
    monkeypatch.setattr(
        "api.modules.image.controllers."
        "extract_faces_from_image.apply_async",
        mock_extract_faces_from_image_apply_async,
    )

    response = client.post(f"/image/{image.uuid}/extract-faces")
    job = FaceExtractionJob.query.first()

    mock_face_extraction_job_schema_dump.assert_called_once_with(job)
    mock_extract_faces_from_image_apply_async.assert_called_once_with(
        args=(job.uuid,),
    )

    assert response.status_code == 201
    assert response.json == {}


def test_start_face_extraction_job_with_invalid_image_id(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/image/<image_id>/extract-faces' is posted to (POST) with invalid
         image_id
    THEN check that a '404' status code is returned and no job is created
    """

    mock_extract_faces_from_image_apply_async = Mock(
        return_value=FakeTaskResult()
    )

    monkeypatch.setattr(
        "api.modules.image.controllers."
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


def test_get_face_extraction_job_status(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/extraction-jobs/<job_id>' is requested (GET) with valid
         job_id
    THEN check that response is valid
    """
    run_job_seeder()

    mock_face_extraction_job_schema_dump = Mock(return_value={})

    monkeypatch.setattr(
        "api.modules.jobs.controllers.face_extraction_job_schema.dump",
        mock_face_extraction_job_schema_dump,
    )

    job = FaceExtractionJob.query.first()

    response = client.get(f"/extraction-jobs/{job.uuid}")

    mock_face_extraction_job_schema_dump.assert_called_once_with(job)

    assert response.status_code == 200
    assert response.json == {}


def test_get_face_extraction_job_status_with_invalid_job_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/extraction-jobs/<job_id>' is requested (GET) with invalid
         job_id
    THEN check that a status code of '404' is returned
    """
    response = client.get(f"/extraction-jobs/{str(uuid.uuid4())}")

    assert response.status_code == 404
    assert response.json["message"] == "Extraction job not found"


def test_get_face_extraction_job_results(client, monkeypatch):
    """
    GIVEN a flask application configured for testing
    WHEN the '/extraction-jobs/<job_id>/results' is requested (GET) with
         invalid job_id
    THEN check that reponse is valid
    """
    run_job_seeder()

    mock_faces_schema_dump = Mock(return_value={})

    monkeypatch.setattr(
        "api.modules.jobs.controllers.faces_schema.dump",
        mock_faces_schema_dump,
    )

    job = FaceExtractionJob.query.first()

    response = client.get(f"/extraction-jobs/{str(job.uuid)}/results")

    mock_faces_schema_dump.assert_called_once_with(job.results)
    assert response.status_code == 200
    assert response.json == {}


def test_get_face_extraction_job_results_with_invalid_job_id(client):
    """
    GIVEN a flask application configured for testing
    WHEN the '/extraction-jobs/<job_id>/results' is requested (GET) with
         invalid job_id
    THEN check that a status code of '404' is returned
    """
    response = client.get(f"/extraction-jobs/{str(uuid.uuid4())}/results")

    assert response.status_code == 404
    assert response.json["message"] == "Extraction job not found"
