import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from textblob import TextBlob
from flaskr.auth_controller import login_required
from flaskr.db import get_db

# Import models
from flaskr.book import Book
from flaskr.user import User

bp = Blueprint('book', __name__)

@bp.route('/book/<isbn>', methods=['GET'])
def show(isbn):
    book = Book.find(isbn)

    if g.user and session['user_id'] and book is not None:
        current_user = User(session['user_id'])
        current_user.add_to_recently_viewed(isbn)

    if current_user is not None:
        saved = current_user.book_is_saved(book.id, get_db().cursor())
    else:
        saved = False

    return render_template('book/book.html', book=book, saved=saved)
