import pymongo 
from pymongo import MongoClient

server = MongoClient( "127.0.0.1" )
#server = MongoClient( "149.89.150.100" )

db = server.picfic

cM = db.markers

#markers have: ids, locations (somehow), imgIDs, (bookID, chapterID?)

#Helper
def exists( markerID ):
    finder = cM.find_one(
        { "markerID" : int(markerID) }
        )
    return finder is not None

def getImages( markerID ):
    if exists(markerID):
        finder = cM.find_one({"markerID": int(markerID)}, {"imageIDs": 1})
        return finder
    return false

