from flask import Flask, render_template, request, redirect
from sources.webservice import UserAuthentication


def create_app(config=None):
    app = Flask(__name__)
    app.register_blueprint(UserAuthentication.bp)

    @app.route("/")
    def landing_page():
        # TODO: If user is logged in, redirect to home page, else redirect to login page
        return render_template('login.html')

    # @app.route("/login/")
    # def login():
    #     return render_template('login.html')



    return app
