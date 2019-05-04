import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, Flask, current_app
)

from werkzeug.exceptions import abort
from textblob import TextBlob
from flaskr.auth_controller import login_required
from flaskr.db import get_db

# Import Models
app = Flask(__name__)
from flaskr.model import Model
from flaskr.Amazon_review import AmazonReview
from flaskr.Reddit_review import RedditReview
from flaskr.BarnesAndNoble_review import BnReview

class Book(Model):
    table = 'books'

    def __init__(self, isbn):
        with app.app_context():
            self.cursor = get_db().cursor()

            self.cursor.execute(
                'SELECT * from books where books.id = %s;', (isbn,)
            )
            self.dict = self.cursor.fetchone()

            if self.dict is None:
                return None

            for k,v in self.dict.items():
                if isinstance(self.dict[k], str):
                    self.dict[k] = re.sub("[^A-Za-z0-9\.\,\?\!\(\)\;\:\'\"\\n\ \/\=\+\-\_\*\#\%_]+", '', v)

            self.id = self.dict['id']
            self.isbn = self.dict['isbn']
            self.isbn13 = self.dict['isbn13']
            self.date_published = self.dict['date_published']
            self.title = self.dict['title']
            self.average_review = self.dict['average_review']
            self.ratings_count = self.dict['ratings_count']
            self.work_ratings_count = self.dict['work_ratings_count']
            self.work_text_reviews_count = self.dict['work_text_reviews_count']
            self.ratings_1 = self.dict['ratings_1']
            self.ratings_2 = self.dict['ratings_2']
            self.ratings_3 = self.dict['ratings_3']
            self.ratings_4 = self.dict['ratings_4']
            self.ratings_5 = self.dict['ratings_5']
            self.cover = self.dict['cover']
            self.author = self.dict['author']
            self.details = self.dict['details']
            self.description = self.dict['description']
            self.purchase_link = self.dict['purchase_link']

            # TODO
            self.similar_books = None
            self.twitter_reviews = None
            self.amazon_reviews = AmazonReview.find_by_id(self.id)
            self.bn_reviews = BnReview.find_by_id(self.id)
            self.reddit_reviews = RedditReview.find_by_id(self.id)

    def find(isbn):
        return Book(isbn);

    def to_dict(self):
        return self.dict
