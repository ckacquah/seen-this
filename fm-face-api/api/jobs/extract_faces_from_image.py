from functools import reduce

from api.jobs import celery
from api.utils import get_uploaded_file_path
from api.modules.image.models import Image
from api.modules.image.services import (
    detect_faces_from_image,
    store_detected_faces_to_db,
    store_detected_faces_image_info_to_db,
    store_detected_faces_images_to_processed_folder,
)


def execute_face_extraction_pipeline(image_storage_name):
    return reduce(
        lambda value, function: function(value),
        (
            get_uploaded_file_path,
            detect_faces_from_image,
            store_detected_faces_image_info_to_db,
            store_detected_faces_images_to_processed_folder,
        ),
        image_storage_name,
    )


@celery.task(name="job-face-extraction")
def extract_faces_from_image(image_id):
    image = Image.query.get(image_id)
    faces = execute_face_extraction_pipeline(image.storage_name)
    results = store_detected_faces_to_db(faces, parent=image)
    return results
