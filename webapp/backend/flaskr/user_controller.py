import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.user import User
from flaskr.db import get_db

bp = Blueprint('user', __name__)

@bp.route('/profile', methods=['POST'])
def update():
    if session['user_id'] and request.method == 'POST':
        current_user = User(session['user_id'])
        book_id = get_id_from_post_data(request.data)
        if book_id is not None:
            if command_is_remove(request.data):
                current_user.remove_book(book_id)
            else:
                current_user.save_book(book_id)
        return 'OK'
    else:
        flash("Please login first.")
        return redirect('/login')

@bp.route('/profile', methods=['GET'])
def show():
    if session['user_id']:
        current_user = User(session['user_id'])
        return current_user.get_my_books()
    else:
        flash("Please login first.")
        return redirect('/login')

def get_id_from_post_data(post_data):
    stringified_data = post_data.decode('utf-8')
    print(stringified_data)
    if stringified_data is not None:
        data = stringified_data.replace('&','=').split("=")
        if len(data) >= 2:
            return data[1]
        else:
            return None
    else:
        return None

def command_is_remove(post_data):
    stringified_data = post_data.decode('utf-8')
    print(stringified_data)
    if stringified_data is not None:
        data = stringified_data.replace('&','=').split("=")
        if len(data) > 2:
            return True
        else:
            return False
    else:
        return False


