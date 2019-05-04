import functools
import re

from flask import (
    Flask, current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

#Import Models
app = Flask(__name__)
from flaskr.model import Model

class Auth(Model):
    table = "users"
    
    def __init__(self, username):
        with app.app_context():
            self.cursor = get_db().cursor()
            self.cursor.execute('SELECT * FROM users WHERE username = %s',(username,))
            self.dict = self.cursor.fetchone()

            self.id = None
            self.username = None
            self.password = None

            if self.dict is None:
                return None
            
            self.id = self.dict['id']
            self.username = self.dict['username']
            self.password = self.dict['password']
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_user_by_id(user_id):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            return cursor.fetchone()

    @staticmethod
    def add_user(username, password):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            print(password)
            thing = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, generate_password_hash(password)))
            print(thing)
            db.commit()

    @staticmethod
    def find(username):
	return Auth(username)

    def to_dict(self):
	return self.dict
