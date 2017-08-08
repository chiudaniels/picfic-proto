from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import users, images

def getUploadStoryData(uID):
    ret = {}
    ret["data"] = users.getUsername(uID)
    return ret
    
