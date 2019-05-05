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
from flaskr.Abstract_review import Review

class TwitterReview(Review):
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.id = dictionary["id"]
        self.book_id = dictionary["book_id"]
        self.title = dictionary["title"]
        self.isbn = dictionary["isbn"]
        self.author = dictionary["author"]
        self.review_source = dictionary["review_source"]
        self.review_content = dictionary["review_content"]
        self.set_sentiment()

    @staticmethod
    def find_by_id(book_id):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute(
                    'SELECT * FROM twitter WHERE twitter.book_id = %s;', (book_id,)
            )

            twitter_reviews_dictionary = cursor.fetchall()
            twitter_reviews = [];

            for twitter_review_dictionary in twitter_reviews_dictionary:
                twitter_review = TwitterReview(twitter_review_dictionary)
                twitter_reviews.append(twitter_review)

            return twitter_reviews

    @staticmethod
    def find_by_isbn(isbn):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute(
                    'SELECT * FROM twitter WHERE twitter.isbn = %s;', (isbn,)
            )

            twitter_reviews_dictionary = cursor.fetchall()
            twitter_reviews = [];

            for twitter_review_dictionary in twitter_reviews_dictionary:
                twitter_review = TwitterReview(twitter_review_dictionary)
                twitter_reviews.append(twitter_review)

            return twitter_reviews
