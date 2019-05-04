# -*- coding: utf-8 -*-
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, Flask, current_app
)

from werkzeug.exceptions import abort
from textblob import TextBlob
from flaskr.auth_controller import login_required
from flaskr.db import get_db

# Models
app = Flask(__name__)
from flaskr.model import Model

class BnReview(Model):
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.id = dictionary["id"]
        self.book_id = dictionary["book_id"]
        self.title = dictionary["title"]
        self.isbn = dictionary["isbn"]
        self.author = dictionary["author"]
        self.review_source = dictionary["review_source"]
        self.average_rating = dictionary["average_rating"]
        self.review_author = dictionary["review_author"]
        self.review_content = dictionary["review_content"]

    @staticmethod
    def find_by_id(book_id):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute(
                'SELECT * FROM BN WHERE BN.book_id = %s;', (book_id,)
            )
            BN_reviews_dictionary = cursor.fetchall()
            BN_reviews = [];
            for BN_review_dictionary in BN_reviews_dictionary:
                BN_review = BnReview(BN_review_dictionary)
                BN_reviews.append(BN_review)
            return BN_reviews
    
    @staticmethod
    def find_by_isbn(isbn):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute(
                'SELECT * FROM BN WHERE BN.isbn = %s;', (isbn,)
            )
            BN_reviews_dictionary = cursor.fetchall()
            BN_reviews = [];
            for BN_review_dictionary in BN_reviews_dictionary:
                BN_review = BnReview(BN_review_dictionary)
                BN_reviews.append(BN_review)
            return BN_reviews
