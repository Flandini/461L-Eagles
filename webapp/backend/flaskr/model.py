from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from textblob import TextBlob
from flaskr.db import get_db

class Model:
    def to_dict(self):
        raise NotImplementedError("Please implement to_dict for this subclass")
    def find(something):
        raise NotImplementedError("Please implement find for this class")
