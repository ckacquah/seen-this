import logging
from faker import Faker
from shutil import copyfile
from api.base_model import db

from api.modules.jobs.models import FaceExtractionJob
from api.modules.face.models import Face, FacialArea
from api.modules.image.models import Image
from api.modules.target.models import Target, TargetTag
from api.utils.testing import get_sample_image_path
from api.utils import (
    get_uploaded_file_path,
    get_processed_file_path,
    generate_random_filename,
)

fake = Faker()

logger = logging.getLogger("seeder")


def generate_fake_images(count=1, source="upload", use_files=False):
    filenames = [
        generate_random_filename(extension="jpg") for _ in range(count)
    ]
    sample_image_path = get_sample_image_path("sample.jpg")
    if use_files:
        for filename in filenames:
            if source == "upload":
                destination = get_uploaded_file_path(filename)
                copyfile(sample_image_path, destination)
            else:
                destination = get_processed_file_path(filename)
                copyfile(sample_image_path, destination)
    return [
        Image(
            name=filenames[i],
            size=fake.random_int(min=1, max=100),
            width=fake.random_int(min=1, max=100),
            height=fake.random_int(min=1, max=100),
            source=source,
            storage_name=filenames[i],
        )
        for i in range(count)
    ]


def generate_fake_facial_areas(count=1):
    return [
        FacialArea(
            x1=fake.random_int(min=100, max=1000),
            x2=fake.random_int(min=100, max=1000),
            y1=fake.random_int(min=100, max=1000),
            y2=fake.random_int(min=100, max=1000),
        )
        for _ in range(count)
    ]


def generate_fake_faces(count=1, use_files=False):
    facial_areas = generate_fake_facial_areas(5)
    parents = generate_fake_images(5, use_files=use_files)
    images = generate_fake_images(5, "processed", use_files=use_files)
    return [
        Face(
            score=fake.random_int(min=1, max=100),
            image=images[index],
            parent=parents[index],
            facial_area=facial_areas[index],
        )
        for index in range(count)
    ]


def run_image_seeder():
    logger.info("Running image seeder...")
    db.session.add_all(generate_fake_images(5, use_files=True))
    db.session.commit()
    logger.info("Image seeder has completed")


def run_face_seeder():
    logger.info("Running face seeder...")
    db.session.add_all(generate_fake_faces(5, use_files=True))
    db.session.commit()
    logger.info("Face seeder has completed")


def run_target_seeder():
    logger.info("Running target seeder...")
    target = Target(
        title=fake.name(),
        description=fake.text(),
        faces=generate_fake_faces(5, use_files=True),
        tags=[TargetTag(name=fake.name()) for _ in range(5)],
    )
    db.session.add(target)
    db.session.commit()
    logger.info("Target seeder has completed")


def run_job_seeder():
    logger.info("Running job seeder...")
    db.session.add(
        FaceExtractionJob(
            image_uuid="123",
            status="started",
            percentage_complete=0,
            celery_task_id="celery_task_id",
        )
    )
    db.session.commit()
    logger.info("Job seeder has completed")


def run_seeds():
    logger.info("Start seeding...")
    run_image_seeder()
    run_face_seeder()
    run_target_seeder()
    run_job_seeder()