import logging
from faker import Faker

from app.utils import generate_random_file_name
from app.base_model import db
from app.modules.face.models import Face, FacialArea
from app.modules.image.models import Image

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
            storage_name=generate_random_file_name(),
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
    db.session.add_all(generate_factory_images(5))
    db.session.commit()
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
    logger.info("Writing to db...")
    db.session.add_all(files + parents + facial_areas + faces)
    db.session.commit()
    logger.info("Face seeder has completed")


def run_seeds():
    logger.info("Start seeding...")
    run_image_seeder()
    run_face_seeder()
