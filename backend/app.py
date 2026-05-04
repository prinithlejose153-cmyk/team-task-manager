from flask import Flask
from backend.config import Config
from backend.extensions import db, jwt, bcrypt
from flask_cors import CORS
from backend.routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)