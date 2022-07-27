import logging

from api.base_model import db
from api.utils.testing.faker import (
    generate_fake_extraction_job,
    generate_fake_images,
    generate_fake_faces,
    generate_fake_targets,
)

logger = logging.getLogger("seeder")


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
    db.session.add_all(generate_fake_targets(5, use_files=True))
    db.session.commit()
    logger.info("Target seeder has completed")


def run_job_seeder():
    logger.info("Running job seeder...")
    db.session.add_all(generate_fake_extraction_job())
    db.session.commit()
    logger.info("Job seeder has completed")


def run_seeds():
    logger.info("Start seeding...")
    run_image_seeder()
    run_face_seeder()
    run_target_seeder()
    run_job_seeder()
