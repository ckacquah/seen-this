# Statement for enabling the development environment
import os

DEBUG = True
TESTING = True

# Define the server name
# SERVER_NAME = "spencer.auth"

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

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

# configuration for Celery
CELERY_CONFIG = {
    'broker_url': 'pyamqp://root:root@127.0.0.1//',
    'result_backend': 'redis://127.0.0.1',
}

# Files upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
