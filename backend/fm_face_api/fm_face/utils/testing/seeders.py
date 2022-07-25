import logging
from faker import Faker
from werkzeug.datastructures import FileStorage

from fm_face.utils import generate_random_filename
from fm_face.base_model import db
from fm_face.modules.face.models import Face, FacialArea
from fm_face.modules.image.models import Image
from fm_face.modules.target.models import Target, TargetTag
from fm_face.utils.testing import get_sample_image_path
from fm_face.modules.image.services import save_uploaded_image

fake = Faker()

logger = logging.getLogger("seeder")


def generate_factory_images(count=1, source="upload"):
    return [
        Image(
            name=generate_random_filename(extension="jpg"),
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
                image=files[i],
                parent=parents[i],
                facial_area=facial_areas[i],
            )
        )
    db.session.add_all(files + parents + facial_areas + faces)
    db.session.commit()
    logger.info("Face seeder has completed")


def run_target_seeder():
    logger.info("Running target seeder...")
    run_face_seeder()
    faces = Face.query.all()
    tags = [TargetTag(name=fake.name()) for _ in range(5)]
    target = Target(title=fake.name(), description=fake.text())
    for index in range(5):
        target.tags.append(tags[index])
        target.faces.append(faces[index])
    db.session.add(target)
    db.session.add_all(tags)
    db.session.commit()
    logger.info("Target seeder has completed")


def run_seeds():
    logger.info("Start seeding...")
    run_image_seeder()
    run_face_seeder()
    run_target_seeder()
