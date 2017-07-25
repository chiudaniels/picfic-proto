#initialize mongo database

from pymongo import MongoClient

server = MongoClient( "127.0.0.1" )
#server = MongoClient( "149.89.150.100" )

db = server.picfic

cU = db.users #collection of users

#To do: replace counting id system with rng and validate

#User data functions

def exists( userID ):
    finder = cU.find_one(
        { "userID" : int(userID) }
        )
    return finder is not None

"""
isValidAccountInfo( uN, hP )
Given:
    uN - username
    hP - hashed pass 
Returns:
    boolean of validity of account info (for login)
"""
def isValidAccountInfo( uN, hP ):
    if not doesUserExist( uN ):
        return False
    finder = cU.find_one(
        { "username" : uN }
        )
    return finder["password"] == hP

"""
getUserID( uN )
Given:
    uN - username 
Returns:
    int of userID for given username
"""
def getUserID( uN ):
    finder = cU.find_one(
        { "username" : uN }
        )
    return finder["userID"]

"""
getUsername( uID )
Given:
    uID - userID 
Returns:
    str of username for given userID
"""
def getUsername( uID ):
    finder = cU.find_one(
        { "userID" : uID }
        )
    return finder["username"]

"""
registerAccountInfo( uN )
Given:
    uN - username
    hP - hashed pass
Returns:
    boolean of whether account was successfully created
"""
def registerAccountInfo( uN, hP ):
    try:
        doc = {}
        doc["username"] = uN
        doc["userID"] = counter_cU()
        doc["password"] = hP
        doc["starredIDs"] = []
        doc["ownedIDs"] = [] #images
        doc["authortag"] = uN #allow configuration
        doc["likedImages"] = []
        cU.insert_one( doc )
        return True
    except:
        return False


def registerAdditionalInfo( uID, newInfo ):
    if exists(uID):
        finder = cU.update_one({"userID": uID }, {"userInfo": newInfo })
    return None
    
    
"""
doesUserExist( uN )
Given:
    uN - username 
Returns:
    boolean of whether a username is already taken
"""
def doesUserExist( uN ):
    finder = cU.find_one(
        { "username" : uN }
        )
    return finder is not None
        
"""
getPass( uID )
Given:
    uID - userID 
Returns:
    str of password for a given userID
"""
def getPass( uID ):
    finder = cU.find_one(
        { "userID" : uID }
        )
    return finder["password"]

"""
changePass( uID, newPass )
Given:
    uID - userID
    newPass - new pass
Returns:
    boolean of whether a password was successfully changed
"""
def changePass( uID, newPass ):
    try:
        cU.update(
            { "userID" : uID },
            { "$set":
                { "password": newPass }
            }
        )
        return True
    except:
        return False


def changeTag( uID, newTag ):
    try:
        cU.update(
            { "userID" : uID },
            { "$set":
                { "authortag": newTag }
            }
        )
        return True
    except:
        return False



def getTag( userID ):
    if exists(userID):
        finder = cU.find_one({"userID": int(userID)}, {"authortag": 1})
        return finder
    return False

def getUsername ( userID ):    
    if exists(userID):
        finder = cU.find_one({"userID": int(userID)}, {"username": 1})
        return finder
    return False

def getLikedImages ( userID ):    
    if exists(userID):
        finder = cU.find_one({"userID": int(userID)}, {"likedImages": 1})
        return finder
    return False



    
#helper functions    
def counter_cU():
    return cU.count()
