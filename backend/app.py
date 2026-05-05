from flask import Flask
from backend.config import Config
from backend.extensions import db, jwt, bcrypt
from flask_cors import CORS
from backend.routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Register routes
    app.register_blueprint(api)

    # Root route
    @app.route("/")
    def home():
        return "Team Task Manager API is running 🚀"

    # Create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)