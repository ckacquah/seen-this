from retinaface import RetinaFace

from app.tasks import celery
from app.utils import get_uploaded_file_path
from app.modules.image_handler.models import File


@celery.task(name="extract-faces-from-image-task")
def extract_faces_from_image(image_param):
    uuid = image_param["image"]
    backend = image_param["backend"]
    image_file = File.query.filter_by(uuid=uuid).first()
    image_path = get_uploaded_file_path(image_file.name)
    resp = RetinaFace.detect_faces(image_path)
    print(resp)
    return {"faces": resp.values()}
