import pymongo 
from pymongo import MongoClient

pM = db.photos;

def addPhoto( url, photoID ):
    if exists( photoID ):
        finder = cM.find_one(
            { "photoID" : int(photoID) }
        )  
        print finder["outline"]
        if finder["outline"] == []:
            pM.update_one(
                {"photoID" : int(photoID)},
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
                {"photoID" : int(photoID)},
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

def exists( photoID ):
    finder = cM.find_one(
        { "photoID" : int(photoID) }
        )
    return finder is not None
