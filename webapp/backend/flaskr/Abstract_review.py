import abc
#from abc import ABC, abstractmethod, abstractproperty

class ReviewObject():
    def __init__(self, dictionary):
        self.id = dictionary["id"]
        self.book_id = dictionary["book_id"]
        self.title = dictionary["title"]
        self.isbn = dictionary["isbn"]
        self.author = dictionary["author"]
        self.review_source = dictionary["review_source"]
        self.review_content = dictionary["review_content"]

    #@abstractmethod
    def find_by_id(book_id):
        pass
