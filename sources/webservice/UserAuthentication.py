import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session

bp = Blueprint('auth', __name__)


@bp.route("/")
def landing_page():
    return render_template('login.html')


@bp.route("/signup")
def register_user():
    return render_template('signup.html')
