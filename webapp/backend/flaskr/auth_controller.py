import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from flaskr.auth import Auth

bp = Blueprint('auth', __name__)


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Auth.get_user_by_id(user_id)
        
        '''
        cur=get_db().cursor()
        cur.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user=cur.fetchone()
        '''

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur=db.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = Auth(username)
            '''
            cur.execute(
                'SELECT id FROM users WHERE username = %s', (username,)
            )
            '''
            '''
            if cur.fetchone() is not None:
            '''
            if user.id is not None:
                error = 'User, {0}, is already registered.'.format(username)
                flash(error)

        if error is None:
            Auth.add_user(username, password)
            '''
            cur.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()
            '''
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        '''
        cur = get_db().cursor()
        cur.execute(
            'SELECT * FROM users WHERE username = %s', (username,)
        )
        user=cur.fetchone()
        '''
        
        
        user_object = Auth(username)
        user = user_object.to_dict()
        

        if user is None:
            error = 'Incorrect username.'
        #elif not check_password_hash(user['password'], password):
        elif not user_object.check_password(password):
            error = 'Incorrect password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('index'))
