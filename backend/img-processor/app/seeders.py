import logging
from faker import Faker

from app.utils import generate_random_file_name
from app.base_model import db
from app.modules.image.models import Image

fake = Faker()

logger = logging.getLogger("seeder")


def run_image_seeder():
    logger.info("Running image seeder...")
    # create 5 images
    images = []
    for i in range(5):
        image = Image(
            name=fake.name(),
            size=fake.random_int(min=1, max=100),
            width=fake.random_int(min=1, max=100),
            height=fake.random_int(min=1, max=100),
            source="upload",
            storage_name=generate_random_file_name(),
        )
        images.append(image)
        logger.info(f"{image.storage_name} created")
    db.session.add_all(images)
    db.session.commit()
    logger.info("Image seeder has completed")


def run_seeds():
    logger.info("Start seeding...")
    run_image_seeder()
