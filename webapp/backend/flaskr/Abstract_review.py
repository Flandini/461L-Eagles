from textblob import TextBlob

class Review():
    def __init__(self, dictionary):
        self.id = dictionary["id"]
        self.book_id = dictionary["book_id"]
        self.title = dictionary["title"]
        self.isbn = dictionary["isbn"]
        self.author = dictionary["author"]
        self.review_source = dictionary["review_source"]
        self.review_content = dictionary["review_content"]

    def find_by_id(book_id):
        pass

    def set_sentiment(self):
        if self.review_content is not None:
            self.sentiment = TextBlob(str(self.review_content)).sentiment
            self.polarity = self.sentiment.polarity
            self.subjectivity = self.sentiment.subjectivity
        else:
            self.polarity = ""
            self.subjectivity = ""
