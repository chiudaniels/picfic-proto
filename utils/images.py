import datetime
import time

import pymongo
from pymongo import MongoClient

import userDb

server = MongoClient( "127.0.0.1" )

db = server.picfic

cI = db.images


#Helper
def exists( imageID ):
    finder = cB.find_one(
        { "imageID" : int(imageID) }
        )
    return finder is not None


#Possibly replace with get image data (for page loading)

#given: image id
#returns: image url
def getImageURL( imageID ):
    if exists(imageID):
        finder = cI.find_one({"imageID":int(imageID)}, {"url" : 1})
        return finder
    return False

#for the reading page (non detailed)
def getImageDisplay( imageID ):
    if exists(imageid):
        finder = cI.find_one({"imageID":int(imageID)}, {"url" : 1, "userID" : 1, "markerID" : 1})
        finder["authortag"] = userDb.getTag( finder["userID"])
        return finder
    return False
        

#given: image url (from flask request), markerID, uploader
#returns: imageID
#creates image document
def saveImage( url, markerID, userID ):
    imageID = counter_cI()
    #update user db
    db.users.update_one(
        {"userID": int(userID)},
        {"$addToSet":
         {"imageIDs": [imageID]}
        }
    )
    #update marker db
    db.markers.update_one(
        {"markerID": int(markerID)},
        {"$addToSet":
         {"imageIDs": [imageID]}
        }
    )
    #update images db
    cI.insert_one(
        {
            "imageID" : imageID,
            "timestamp" : datetime.date.today().ctime(),
            "userID" : userID,
            "markerID" : markerID,
            "likes" : [], #to hold userIDs,
            "comments" : [], #to hold comment data tructure
            #{ user: <userName>, message: <text>, timestamp: <timestamp> }
            "url" : url
        }
    )
    return True


def like_image( userID, imageID ):
    cI.update_one(
        {"imageID": int(imageID)},
        {"$addToSet":
         {"likes": [userID]}
        }
    )
    return True

#pass this info to frontend
def isImageLiked( userID, imageID ):
    if userID == None:
        return False
    else:
        finder = cI.find_one(
            {"imageID": int(imageID)},
            {"likes" : 1}
        )
        return userID in finder["likes"]
        
    
def userFind( userID ):
    return None


def counter_cI():
    return cI.count()
