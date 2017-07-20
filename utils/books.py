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
def exists( mapID ):
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
        finder = cM.find_one(
            { "mapID" : int(mapID) }
            )
        return finder["outline"]
    return None
"""

def getPageData( bookNum, chNum, pgNum ):
    return None

def addImage( url, mapID ):
    if exists( mapID ):
        finder = cM.find_one(
            { "mapID" : int(mapID) }
        )  
        print finder["outline"]
        if finder["outline"] == []:
            cM.update_one(
                {"mapID" : int(mapID)},
                {"$set" :
                    {   
                        "outline" : [url],
                        "timeUpdated" :  datetime.date.today().ctime(),
                        "tUpdated" : time.time()
                        }
                }
                )
            return True
        else:
            cM.update_one(
                {"mapID" : int(mapID)},
                {"$set" :
                    {   
                        "outline" : finder["outline"] + [url],
                        "timeUpdated" :  datetime.date.today().ctime(),
                        "tUpdated" : time.time()
                        }
                }
                )
            return True
    return False

#helper functions

def counter_cM():
    return cM.count()
