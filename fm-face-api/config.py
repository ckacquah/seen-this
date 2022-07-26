import os
from api.config import get_config


config = get_config(os.environ.get("FLASK_ENV", "development"))
