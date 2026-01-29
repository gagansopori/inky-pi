from flask import Flask

from sources.webservice.controllers import UserController


def create_app(config=None):
    app = Flask(__name__)
    app.register_blueprint(UserController.bp)

    return app
