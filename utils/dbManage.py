import pymongo
from pymongo import MongoClient
server = MongoClient("127.0.0.1")
db = server.picfic

def clear():
    db.books.remove_many({})
    db.images.remove_many({})
    db.users.remove_many({})
    db.markers.remove_many({})
