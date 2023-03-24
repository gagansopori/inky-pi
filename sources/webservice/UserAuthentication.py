import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

bp = Blueprint('auth', __name__)


@bp.route("/", methods=('GET', 'POST'))
def landing_page():
    # TODO - If user is logged or logs in then redirect to home page with user info. else throw error.
    return render_template('login.html')


@bp.route("/signup", methods=('GET', 'POST'))
def register_user():
    if request.method == 'POST':
        print(f'{request.form["username"]}')
        return redirect(url_for('auth.landing_page'))

    return render_template('signup.html')
