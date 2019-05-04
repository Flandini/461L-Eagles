import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.model import Model

app = Flask(__name__)

class User(Model):
    tables = 'saved_books'

    def __init__(self, user_id):
        with app.app_context():
            self.id = user_id
            self.dict = {"id": user_id}

    @staticmethod
    def find(user_id):
        return User(user_id)
    
    def to_dict(self):
        return self.dict

    @staticmethod
    def get_save_book_query():
        query = "insert into saved_books "\
            "(book_id, user_id) "\
            "values (%s, %s) "
        return query

    def book_is_saved(self, book_id, cursor):
        cursor.execute("select * from saved_books where user_id = %s and book_id = %s", (self.id, book_id,))
        result = cursor.fetchall()
        if result is not None and len(result) >= 1:
            return True
        else:
            return False

    def remove_book(self, book_id):
        cursor = get_db().cursor()
        if not self.book_is_saved(book_id, cursor):
            return False
        else:
            cursor.execute("delete from saved_books where user_id = %s and book_id = %s", (self.id, book_id,))
            get_db().commit()
            return True

    def save_book(self, book_id):
        cursor = get_db().cursor()
        if not self.book_is_saved(book_id, cursor):
            cursor.execute(User.get_save_book_query(), (book_id, self.id,))
            get_db().commit()
            print("BOOK HAS BEEN SAVED")
            return True
        else:
            return False

    @staticmethod
    def get_recently_viewed_query():
        query = "select * from users "\
                "left outer join recently_viewed "\
                "on users.id = recently_viewed.user_id "\
                "right outer join books "\
                "on books.id = recently_viewed.book_id "\
                "where users.id = %s order by "\
                "recently_viewed.id desc limit 12"

        return query

    def get_recently_viewed_books(self, cursor):
        #if g.user and session['user_id']:
        cursor.execute(User.get_recently_viewed_query(), (self.id,))
        return cursor.fetchall();

    @staticmethod
    def get_saved_books_query():
        query = "select * from users "\
                "left outer join saved_books "\
                "on users.id = saved_books.user_id "\
                "right outer join books "\
                "on books.id = saved_books.book_id "\
                "where users.id = %s "\
                "order by saved_books.id desc"
        return query

    def get_saved_books(self, cursor):
        #if g.user and session['user_id']:
        cursor.execute(User.get_saved_books_query(), (self.id,))
        return cursor.fetchall();

    def get_my_books(self):
        cursor = get_db().cursor()
        cursor.execute(User.get_recently_viewed_query(), (self.id,))
        recently_viewed = self.get_recently_viewed_books(cursor)
        saved_books = self.get_saved_books(cursor)
        return render_template('user/profile.html', recently_viewed=recently_viewed, saved_books=saved_books)

