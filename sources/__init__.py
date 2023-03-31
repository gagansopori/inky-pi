from flask import Flask
from sources.webservice.controllers import UserAuthentication


def create_app(config=None):
    app = Flask(__name__)
    app.register_blueprint(UserAuthentication.bp)

    return app
