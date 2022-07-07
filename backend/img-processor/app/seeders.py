from faker import Faker

from app.base_model import db
from app.modules.image.models import File

fake = Faker()


def run_seeds():
    # create 5 files
    # files = []
    # for i in range(5):
    #     file = File(
    #         name=fake.name(),
    #         age=fake.random_int(min=1, max=100)
    #     )
    #     files.append(file)
    #     print(f"{file} created")
    # db.session.add_all(files)
    # db.session.commit()
    print("File Seeds written to database")
