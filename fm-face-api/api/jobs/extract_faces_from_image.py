from functools import reduce
from datetime import datetime

from api.base_model import db
from api.jobs import celery
from api.utils import get_uploaded_file_path
from api.modules.jobs.models import FaceExtractionJob
from api.modules.image.services import (
    detect_faces_from_image,
    store_detected_faces_to_db,
    store_detected_face_images_to_disk,
    store_detected_faces_image_info_to_db,
)


def execute_face_extraction_pipeline(image_storage_name):
    return reduce(
        lambda value, function: function(value),
        (
            get_uploaded_file_path,
            detect_faces_from_image,
            store_detected_face_images_to_disk,
            store_detected_faces_image_info_to_db,
        ),
        image_storage_name,
    )


@celery.task(name="job-face-extraction")
def extract_faces_from_image(job_id):
    job = FaceExtractionJob.query.get(job_id)
    image = job.image
    faces = execute_face_extraction_pipeline(image.storage_name)
    results = store_detected_faces_to_db(faces, parent=image)
    job.status = "completed"
    job.completion_time = datetime.now()
    job.percentage_complete = 100
    db.session.commit()
    return results
