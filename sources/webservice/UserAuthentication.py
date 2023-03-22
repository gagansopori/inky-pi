import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session

bp = Blueprint('auth', __name__)


@bp.route('/register/')
def register():
    pass
