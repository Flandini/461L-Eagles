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

class RedditReview(Model):
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.id = dictionary["id"]
        self.book_id = dictionary["book_id"]
        self.title = dictionary["title"]
        self.isbn = dictionary["isbn"]
        self.author = dictionary["author"]
        self.review_source = dictionary["review_source"]
        self.review_author = dictionary["review_author"]
        self.review_content = dictionary["review_content"]

    @staticmethod
    def find_by_id(book_id):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute(
                'SELECT * FROM reddit WHERE reddit.book_id = %s;', (book_id,)
            )
            reddit_reviews_dictionary = cursor.fetchall()
            reddit_reviews = [];
            for reddit_review_dictionary in reddit_reviews_dictionary:
                reddit_review = RedditReview(reddit_review_dictionary)
                reddit_reviews.append(reddit_review)
            return reddit_reviews

    @staticmethod
    def find_by_isbn(isbn):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute(
                'SELECT * FROM reddit WHERE reddit.isbn = %s;', (isbn,)
            )
            reddit_reviews_dictionary = cursor.fetchall()
            reddit_reviews = [];
            for reddit_review_dictionary in reddit_reviews_dictionary:
                reddit_review = RedditReview(reddit_review_dictionary)
                reddit_reviews.append(reddit_review)
            return reddit_reviews
