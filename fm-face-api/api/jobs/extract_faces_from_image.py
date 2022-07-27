import json

from api.jobs import celery
from api.utils import get_uploaded_file_path
from api.modules.image.models import Image
from api.modules.image.services import (
    detect_faces_from_image,
    store_detected_faces_to_db,
    store_detected_faces_image_info_to_db,
    store_detected_faces_images_to_processed_folder,
)


@celery.task(name="extract-faces-from-image")
def extract_faces_from_image(image_id):
    image = Image.query.get(image_id)
    image_path = get_uploaded_file_path(image.storage_name)
    faces = detect_faces_from_image(image_path)
    faces = store_detected_faces_images_to_processed_folder(faces)
    faces = store_detected_faces_image_info_to_db(faces)
    faces = store_detected_faces_to_db(
        faces,
        parent=image,
    )
    return json.dumps(faces)
