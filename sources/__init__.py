from flask import Flask, render_template, request


def create_app(config=None):
    app = Flask(__name__)

    @app.route("/")
    def landing_page():
        return render_template('index.html')

    return app
