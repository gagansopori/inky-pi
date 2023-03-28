import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from sources.webservice.models.UserProfile import UserProfile

user_deets = {
    "username": "gagansopori",
    "password": "InfernuS12!!",
    "type": 2
}

bp = Blueprint('auth', __name__)


@bp.route("/", methods=('GET', 'POST'))
def landing_page():
    # TODO - If user is logged or logs in then redirect to home page with user info. else throw error.
    # if request.method == 'POST':
        # Sanitize input & send for authentication
        # username, password = request.form['username'], request.form['password']
        # user = authenticate_user(username, password)
        # if user.messages is not None:
        #     # flash(user.messages)
        #     return render_template('login.html')
        # else:
        #     return render_template('index.html')

    return render_template('index.html')


@bp.route("/signup", methods=('GET', 'POST'))
def register_user():
    if request.method == 'POST':
        print(f'{request.form["username"]}')
        return redirect(url_for('auth.landing_page'))

    return render_template('signup.html')


def authenticate_user(username, password):
    user = UserProfile()
    if username == user_deets["username"]:
        if password == user_deets["password"]:
            user.username = username
            user.user_type = user_deets["type"]
            user.messages = None
        else:
            user.messages = f'Wrong Password'
    else:
        user.messages = f'Wrong UserName'
    return user
