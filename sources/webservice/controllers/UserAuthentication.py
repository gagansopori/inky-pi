import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from sources.webservice.controllers import user_deets
from sources.webservice.models.UserProfile import UserProfile

bp = Blueprint('auth', __name__)


@bp.route("/", methods=('GET', 'POST'))
@bp.route("/login", methods=('GET', 'POST'))
def landing_page():
    # TODO - If user is logged or logs in then redirect to home page with user info. else throw error.
    if request.method == 'POST':
        # Sanitize input & send for authentication
        username, password = request.form['username'], request.form['password']
        user = authenticate_user(username, password)
        if user.messages is not None:
            # flash(user.messages)
            return render_template('authentication/login.html')
        else:
            return render_template('index.html')

    return render_template('authentication/login.html')


@bp.route("/signup", methods=('GET', 'POST'))
def register_user():
    if request.method == 'POST':
        username, password, email = request.form['username'], request.form['password'], request.form['emailaddr']
        print(f'{username, password, email}')
        create_new_user(username, password, email)

        return redirect(url_for('auth.landing_page'))

    return render_template('authentication/signup.html')


def authenticate_user(username, password):
    """
    Method takes in username & password & validates the user's identity
    :param username:
    :param password:
    :return:
    """
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


def create_new_user(uname, pwd, email):
    pass
