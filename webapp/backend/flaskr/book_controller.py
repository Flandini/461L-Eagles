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

bp = Blueprint('book', __name__)

def book_is_saved(book_id):
    if g.user and session['user_id']:
        cursor = get_db().cursor()
        cursor.execute("select * from saved_books where user_id = %s and book_id = %s", (session['user_id'], book_id,))
        result = cursor.fetchall()
        if result is not None and len(result) >= 1:
            return True
        else:
            return False
    else:
        return False

def set_recently_viewed_books(isbn):
    if g.user and session['user_id']:
        user_id = session['user_id']
        cursor = get_db().cursor()
        insert_query = "insert into recently_viewed (user_id, book_id) values (%s, %s)"
        cursor.execute(
            "insert into recently_viewed (user_id, book_id) values (%s, %s)", (user_id, isbn,)
        )
        get_db().commit()

@bp.route('/book/<isbn>', methods=['GET'])
def show(isbn):
    book = get_book(isbn)
    set_recently_viewed_books(isbn)
    return book

def get_book(isbn):
    book = Book.find(isbn)

    return render_template('book/book.html', book=book, saved=book_is_saved(book.id))


