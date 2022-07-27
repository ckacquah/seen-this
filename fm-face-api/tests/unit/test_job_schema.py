from api.utils.testing.faker import generate_fake_extraction_job
from api.modules.jobs.schemas import (
    face_extraction_job_schema,
    face_extraction_jobs_schema,
)


def test_face_extraction_job_schema():
    """
    GIVEN a FaceExtractionJob object
    WHEN the object is dumped to a dictionary
    THEN check that the dictionary is valid
    """
    job = generate_fake_extraction_job(1)[0]
    job_dict = face_extraction_job_schema.dump(job)
    assert job_dict["uuid"] == job.uuid
    assert job_dict["status"] == job.status
    assert job_dict["image_uuid"] == job.image_uuid
    assert job_dict["completion_time"] == job.completion_time
    assert job_dict["percentage_complete"] == job.percentage_complete


def test_multiple_face_extraction_jobs_schema():
    """
    GIVEN a list of FaceExtractionJob objects
    WHEN the list is dumped
    THEN check that the results is valid
    """
    jobs = generate_fake_extraction_job(3)
    jobs_list = face_extraction_jobs_schema.dump(jobs)
    for job_dict, job in zip(jobs_list, jobs):
        assert job_dict["uuid"] == job.uuid
        assert job_dict["status"] == job.status
        assert job_dict["image_uuid"] == job.image_uuid
        assert job_dict["completion_time"] == job.completion_time
        assert job_dict["percentage_complete"] == job.percentage_complete
