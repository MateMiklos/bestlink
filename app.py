from flask import Flask
from bestlink_app.database import init_db

app = Flask(__name__)

@app.route("/")
def index():
    return "Database test"

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
