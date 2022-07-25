# Run a test server.
from fm_face import create_app

app = create_app()
app.run(host="0.0.0.0", port=5000, debug=True)
