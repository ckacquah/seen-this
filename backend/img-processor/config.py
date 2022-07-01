import os
from app.config import get_config


config = get_config(os.environ.get("FLASK_ENV", "development"))
