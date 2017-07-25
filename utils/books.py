#import modules needed

import datetime
import time
import userDb

#initialize mongo database
import pymongo 
from pymongo import MongoClient

server = MongoClient( "127.0.0.1" )
#server = MongoClient( "149.89.150.100" )

db = server.picfic

cB = db.books

#Book database functions

"""
exists( bookID )
Given:
  bookID - unique id given to each map
Returns:
  boolean of whether a bookID exists
"""
def exists( bookID ):
    finder = cB.find_one(
        { "bookID" : int(bookID) }
        )
    return finder is not None

"""
getBookMetadata( bookID )
Given:
  bookID - unique id given to each map
Returns:
  data for book landing page
"""    
def getBookMetadata( bookID ):
    if exists(bookID):
        finder = cB.find_one(
            { "bookID" : int(bookID) },
            { "meta": 1, "bookID": 1 }
            )
        #NOT DONE NEEDS IMAGES
        
        return finder
    return None

def getTopImages( bookID ):
    return None

#For the gallery
def getGalleryPage( pgNum, query, userID ):

    #for every book
    #finder = cB.find_one({}, {"galMeta":1, "bookID":1})
    return None

#Reading
def getPageData( bookIDA, chNumA, pgNumA ):
    bookID = int(bookIDA)
    chNum = int(chNumA) - 1
    pgNum = int(pgNumA) - 1 #offset for list  indices
    if exists( bookID ):
        ret = {"bookID": bookID}
        #ret["bookData"] =  cB.find_one({"bookID": bookID}) #just pass everything
        print chNum
        ret["chData"] = cB.find_one({"bookID": int(bookID) })["chapters"][chNum]
        ret["pgData"] = ret["chData"]["pages"][pgNum] 
        ret["markerData"] = db.markers.find_one(
            {"markerID": ret["pgData"]["marker"]}
        )
        ret["imageData"] = db.images.find_one(
            {"markerID": ret["markerData"]["markerID"]}
        )
        return ret
    return None




#helper functions

def counter_cB():
    return cB.count()
