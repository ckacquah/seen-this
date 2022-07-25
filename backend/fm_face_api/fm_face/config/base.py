import os


class Config(object):
    # Define the database - we are working with
    # SQLite for this example
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}

    # Define the application directory
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"

    # Secret key for signing cookies
    SECRET_KEY = "secret"

    # Files upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

    # Project Folder directories
    @property
    def STORAGE_FOLDER(self):
        return os.path.join(self.BASE_DIR, "storage")

    @property
    def UPLOAD_FOLDER(self):
        return os.path.join(self.STORAGE_FOLDER, "uploads")

    @property
    def SAMPLES_FOLDER(self):
        return os.path.join(self.STORAGE_FOLDER, "samples")

    @property
    def PROCESSED_FOLDER(self):
        return os.path.join(self.STORAGE_FOLDER, "processed")

    @property
    def PROCESSED_FACES_FOLDER(self):
        return os.path.join(self.PROCESSED_FOLDER, "faces")

    @property
    def DATABASE_FOLDER(self):
        return os.path.join(self.STORAGE_FOLDER, "database")

    # configuration for Celery
    CELERY_CONFIG = {
        "broker_url": "amqp://root:root@127.0.0.1:5672//",
        "result_backend": "redis://127.0.0.1",
    }
