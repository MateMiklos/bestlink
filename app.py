from flask import Flask
from bestlink_app.routes import bp as main_bp
import os

app = Flask(__name__, template_folder=os.path.join("bestlink_app", "templates"))
app.secret_key = "dev"

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
