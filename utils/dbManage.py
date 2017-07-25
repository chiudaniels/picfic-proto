import pymongo
from pymongo import MongoClient
server = MongoClient("127.0.0.1")
db = server.picfic

def clear():
    db.books.removeMany({})
    db.images.removeMany({})
    db.users.removeMany({})
    db.markers.removeMany({})
