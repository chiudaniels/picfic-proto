from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import users, images

# getUploadStoryData (..) - returns user's name given user's ID 
# pre  : int uID - user ID 
# post : dict ret - dictionary with single key returning user's name
#        { String data : user's name } 
def getUploadStoryData(uID):
    ret = {}
    ret["data"] = users.getUsername(uID)
    return ret
    
