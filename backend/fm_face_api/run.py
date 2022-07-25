# Run a test server.
from app import create_app

app = create_app()
fm_face.run(host="0.0.0.0", port=5000, debug=True)
