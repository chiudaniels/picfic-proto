#import modules needed

import datetime
import time
import userDb, markers, images

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
def getPageData( bookIDA, chNumA, userID ):
    bookID = int(bookIDA)
    chNum = int(chNumA) - 1
    bookmark = userDb.getBookmark(userID, bookID )
    if bookmark == None or bookmark[0] != chNum :
        pgNum = 0 #turn into something loaded from userID
    else:
        pgNum = bookmark[1]
    ret = {}
    if exists( bookID ):
        ret["bookID"] = bookID
        #ret["bookData"] =  cB.find_one({"bookID": bookID}) #just pass everything
        ret["chData"] = cB.find_one({"bookID": bookID })["chapters"][chNum]
        ret["pgData"] = ret["chData"]["pages"][pgNum] 
        ret["markerData"] = db.markers.find_one(
            {"markerID": ret["pgData"]["marker"]}
        )
        #probably needs to pull more data for sorting
        ret["imageData"] = []
        print markers.getImages(ret["markerData"]["markerID"])
        for imgID in markers.getImages(ret["markerData"]["markerID"])["imageIDs"]:
            ret["imageData"].append(images.getImageDisplay(imgID))#all images associated - do ajax for associated
            #attributes: authortag, url, userID, markerID
        ret["pgNum"] = pgNum + 1 #for offset
        ret["chNum"] = int(chNumA)
        ret["bookID"] = int(bookIDA)
        ret["chLength"] = len(ret["chData"]["pages"])
        ret["bookLength"] = len(cB.find_one({"bookID": int(bookID)})["chapters"])
        ret["status"] = 1
        return ret
        """
        try:
            ret["chData"] = cB.find_one({"bookID": bookID })["chapters"][chNum]
            ret["pgData"] = ret["chData"]["pages"][pgNum] 
            ret["markerData"] = db.markers.find_one(
                {"markerID": ret["pgData"]["marker"]}
            )
            #probably needs to pull more data for sorting
            ret["imageData"] = []
            print markers.getImages(ret["markerData"]["markerID"])
            for imgID in markers.getImages(ret["markerData"]["markerID"]):
                
                ret["imageData"].append(images.getImageDisplay(imgID))#all images associated - do ajax for associated
                #attributes: authortag, url, userID, markerID
            ret["pgNum"] = int(pgNumA)
            ret["chNum"] = int(chNumA)
            ret["bookID"] = int(bookIDA)
            ret["chLength"] = len(ret["chData"]["pages"])
            ret["bookLength"] = len(cB.find_one({"bookID": int(bookID)})["chapters"])
            ret["status"] = 1
            return ret
        except:
            ret["status"] = 0
            ret["errMsg"] = "This book doesn't have this page."
            
            return ret
    ret["status"] = -1
    ret["errMsg"] = "Book doesn't exist."
    return ret
"""

def getPageAJAX( bookIDA, chNumA, pgNumA ):
    print "ajaxing"
    print bookIDA
    print chNumA
    print pgNumA
    bookID = int(bookIDA)
    chNum = int(chNumA) - 1
    pgNum = int(pgNumA) - 1 #offset for list  indices
    ret = {}
    if exists( bookID ):
        ret["bookID"] = bookID
        chData = cB.find_one({"bookID": bookID }, {"_id": 0})["chapters"][chNum]
        ret["pgData"] = chData["pages"][pgNum] 
        ret["markerData"] = db.markers.find_one(
            {"markerID": ret["pgData"]["marker"]}, {"_id": 0}
        )
        #probably needs to pull more data for sorting
        ret["imageData"] = []
        #print markers.getImages(ret["markerData"]["markerID"])
        for imgID in markers.getImages(ret["markerData"]["markerID"])["imageIDs"]:
            ret["imageData"].append(images.getImageDisplay(imgID))#all images associated - do ajax for associated
            #attributes: authortag, url, userID, markerID
        ret["pgNum"] = int(pgNumA)
        ret["chNum"] = int(chNumA)
        ret["bookID"] = int(bookIDA)
        ret["chLength"] = len(chData["pages"])
        ret["bookLength"] = len(cB.find_one({"bookID": int(bookID)}, {"_id": 0})["chapters"])
        ret["status"] = 1
        
        return ret
        """
        try:
            ret["chData"] = cB.find_one({"bookID": bookID })["chapters"][chNum]
            ret["pgData"] = ret["chData"]["pages"][pgNum] 
            ret["markerData"] = db.markers.find_one(
                {"markerID": ret["pgData"]["marker"]}
            )
            #probably needs to pull more data for sorting
            ret["imageData"] = []
            print markers.getImages(ret["markerData"]["markerID"])
            for imgID in markers.getImages(ret["markerData"]["markerID"]):
                
                ret["imageData"].append(images.getImageDisplay(imgID))#all images associated - do ajax for associated
                #attributes: authortag, url, userID, markerID
            ret["pgNum"] = int(pgNumA)
            ret["chNum"] = int(chNumA)
            ret["bookID"] = int(bookIDA)
            ret["chLength"] = len(ret["chData"]["pages"])
            ret["bookLength"] = len(cB.find_one({"bookID": int(bookID)})["chapters"])
            ret["status"] = 1
            return ret
        except:
            ret["status"] = 0
            ret["errMsg"] = "This book doesn't have this page."
            
            return ret
    ret["status"] = -1
    ret["errMsg"] = "Book doesn't exist."
    return ret
"""




#helper functions

def counter_cB():
    return cB.count()
