from api.jobs import celery
from api.utils import get_uploaded_file_path
from api.modules.image.models import Image
from api.modules.image.services import (
    detect_faces_from_image,
    store_detected_faces_to_db,
    store_detected_faces_images_to_processed_folder,
)


@celery.task(name="extract-faces-from-image")
def extract_faces_from_image(image_id):
    image = Image.query.get(image_id)
    image_path = get_uploaded_file_path(image.storage_name)
    detected_faces = detect_faces_from_image(image_path)
    stored_detected_faces = store_detected_faces_images_to_processed_folder(
        detected_faces
    )
    stored_detected_faces = store_detected_faces_to_db(
        stored_detected_faces,
        parent=image,
    )
    return stored_detected_faces
