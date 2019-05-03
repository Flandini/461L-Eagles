# -*- coding: utf-8 -*-
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, Flask, current_app
)

from werkzeug.exceptions import abort
from textblob import TextBlob
from flaskr.auth_controller import login_required
from flaskr.db import get_db
from flaskr.model import Model

class Twitter_review(Model):
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.id = dictionary["id"]
        self.book_id = dictionary["book_id"]
        self.title = dictionary["title"]
        self.isbn = dictionary["isbn"]
        self.author = dictionary["author"]
        self.review_source = dictionary["review_source"]
        self.review_content = dictionary["review_content"]
        
    @classmethod    
    def find_by_id(book_id):
        cursor = get_db().cursor()
        cursor.execute(
                'SELECT * FROM twitter WHERE twitter.book_id = %s;', (book_id,)
        )
        twitter_reviews_dictionary = cursor.fetchall()
        twitter_reviews = [];
        for twitter_review_dictionary in twitter_reviews_dictionary:
            twitter_review = Twitter_review(twitter_review_dictionary)
            twitter_reviews.append(twitter_review)
        return twitter_reviews
    
    @classmethod
    def find_by_isbn(isbn):
        cursor = get_db().cursor()
        cursor.execute(
                'SELECT * FROM twitter WHERE twitter.isbn = %s;', (isbn,)
        )
        twitter_reviews_dictionary = cursor.fetchall()
        twitter_reviews = [];
        for twitter_review_dictionary in twitter_reviews_dictionary:
            twitter_review = Twitter_review(twitter_review_dictionary)
            twitter_reviews.append(twitter_review)
        return twitter_reviews