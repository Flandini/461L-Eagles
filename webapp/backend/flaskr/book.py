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

            self.populate_similar_books()
            self.populate_twitter_reviews()
            self.populate_amazon_reviews()
            self.populate_bn_reviews()
            self.populate_reddit_reviews()

    def populate_similar_books(self):
        if self.isbn is None:
            return

        with app.app_context():
            self.cursor.execute(
                'select * from similar where similar.id = %s', (self.id,)
            )

            similar_books_dict = self.cursor.fetchone()
            self.similar_books = []

            if similar_books_dict is None:
                return

            for idx in range(1, 6):
                self.similar_books.append(SimilarBook(similar_books_dict['similar_' + str(idx)]))

    def populate_twitter_reviews(self):
        self.twitter_reviewws = []

    def populate_amazon_reviews(self):
        self.amazon_reviews = AmazonReview.find_by_id(self.id)

    def populate_bn_reviews(self):
        self.bn_reviews = BnReview.find_by_id(self.id)

    def populate_reddit_reviews(self):
        self.reddit_reviews = RedditReview.find_by_id(self.id)

    @staticmethod
    def find(isbn):
        return Book(isbn);

    def to_dict(self):
        return self.dict

class SimilarBook(Book):
    def __init__(self, isbn):
        super(SimilarBook, self).__init__(isbn)

    # Necessary to avoid building a tree of all
    # books by finding similar books of similar books
    # of similar books... etc.
    def populate_similar_books(self):
        self.similar_books = []

    def populate_twitter_reviews(self):
        self.twitter_reviewws = []

    def populate_amazon_reviews(self):
        self.amazon_reviews = []

    def populate_bn_reviews(self):
        self.bn_reviews = []

    def populate_reddit_reviews(self):
        self.reddit_reviews = []
