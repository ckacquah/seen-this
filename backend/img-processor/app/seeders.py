import logging
from faker import Faker
from werkzeug.datastructures import FileStorage

from app.utils import generate_random_filename
from app.base_model import db
from app.modules.face.models import Face, FacialArea
from app.modules.image.models import Image
from app.utils.testing import get_sample_image_path
from app.modules.image.services import save_uploaded_image

fake = Faker()

logger = logging.getLogger("seeder")


def generate_factory_images(count=1, source="upload"):
    return [
        Image(
            name=fake.name(),
            size=fake.random_int(min=1, max=100),
            width=fake.random_int(min=1, max=100),
            height=fake.random_int(min=1, max=100),
            source=source,
            storage_name=generate_random_filename(),
        )
        for _ in range(count)
    ]


def generate_factory_facial_areas(count=1):
    return [
        FacialArea(
            x1=fake.random_int(min=100, max=1000),
            x2=fake.random_int(min=100, max=1000),
            y1=fake.random_int(min=100, max=1000),
            y2=fake.random_int(min=100, max=1000),
        )
        for _ in range(count)
    ]


def run_image_seeder():
    logger.info("Running image seeder...")
    file_path = get_sample_image_path("sample.jpg")
    for _ in range(5):
        with open(file_path, mode="rb") as f:
            file_storage_object = FileStorage(
                f, filename=generate_random_filename(extension="jpg")
            )
            save_uploaded_image(file_storage_object)
    logger.info("Image seeder has completed")


def run_face_seeder():
    logger.info("Running face seeder...")
    faces = []
    files = generate_factory_images(5, "processed")
    parents = generate_factory_images(5)
    facial_areas = generate_factory_facial_areas(5)
    for i in range(5):
        faces.append(
            Face(
                score=fake.random_int(min=1, max=100),
                file=files[i],
                parent=parents[i],
                facial_area=facial_areas[i],
            )
        )
    db.session.add_all(files + parents + facial_areas + faces)
    db.session.commit()
    logger.info("Face seeder has completed")


def run_seeds():
    logger.info("Start seeding...")
    run_image_seeder()
    run_face_seeder()
