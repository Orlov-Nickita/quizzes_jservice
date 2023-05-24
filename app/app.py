from flask import Flask
from loader import DEBUG
from models import db
from routes import questions


def create_app(config: str):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)
    flask_app.register_blueprint(questions)
    db.init_app(flask_app)
    return flask_app


if __name__ == '__main__':
    app = create_app('config.MainConfig')
    with app.app_context():
        db.create_all()
    app.run(debug=DEBUG, host='0.0.0.0')
