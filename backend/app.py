from flask import Flask, render_template
from flask_cors import CORS

from backend.config import Config
from backend.extensions import db, jwt, bcrypt
from backend.routes import api


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
CORS(app)

app.register_blueprint(api)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard-page")
def dashboard_page():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)