from flask import Flask

from zsources.webservice.controllers import UserController


def create_app(config=None):
    app = Flask(__name__)
    app.register_blueprint(UserController.bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()