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
  mapID - unique id given to each map
Returns:
  <data> form of the data held in a given map
"""    
def getBookMetadata( bookID ):
    if exists(bookID):
        finder = cB.find_one(
            { "bookID" : int(bookID) },
            { "_id" : 0 }
            )
        return finder
    return None
"""
def getImages( mapID ):
    if exists( mapID ):
        finder = cB.find_one(
            { "mapID" : int(mapID) }
            )
        return finder["outline"]
    return None
"""

def getPageData( bookID, chNum, pgNum ):
    return None

def getTopImages( bookID ):
    return None

#helper functions

def counter_cB():
    return cB.count()
