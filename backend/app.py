from flask import Flask, render_template
from flask_cors import CORS

from backend.config import Config
from backend.extensions import db, jwt, bcrypt
from backend.routes import api
from backend.models import User


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config.from_object(Config)

# Initialize extensions

db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
CORS(app)

# Register routes

app.register_blueprint(api)


# ---------------- DATABASE SETUP ---------------- #

with app.app_context():

    db.create_all()

    # ---------------- AUTO CREATE DEMO USERS ---------------- #

    admin_exists = User.query.filter_by(
        email="admin@test.com"
    ).first()

    if not admin_exists:

        hashed_password = bcrypt.generate_password_hash(
            "123456"
        ).decode("utf-8")

        admin_user = User(
            username="admin",
            email="admin@test.com",
            password=hashed_password,
            role="admin"
        )

        db.session.add(admin_user)

    member_exists = User.query.filter_by(
        email="member@test.com"
    ).first()

    if not member_exists:

        hashed_password = bcrypt.generate_password_hash(
            "123456"
        ).decode("utf-8")

        member_user = User(
            username="member",
            email="member@test.com",
            password=hashed_password,
            role="member"
        )

        db.session.add(member_user)

    db.session.commit()


# ---------------- FRONTEND ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard-page")
def dashboard_page():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)