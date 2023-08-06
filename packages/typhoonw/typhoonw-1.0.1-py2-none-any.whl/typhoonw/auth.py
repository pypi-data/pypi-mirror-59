#-*- coding:utf-8 -*-
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# from flaskr.db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

user = {'username':'admin', 'password':generate_password_hash('123456'), 'id':1}

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('data.parting_intro'))

        flash(error)

    return render_template('auth/login.html')

@auth_bp.before_app_request
def load_logged_in_user():
	# pass
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user
    #     g.user = get_db().execute(
    #         'SELECT * FROM user WHERE id = ?', (user_id,)
    #     ).fetchone()

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view