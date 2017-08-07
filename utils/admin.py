from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import users, books, images

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

#Admin page code, etc

def getAdminPageData():
    session = Session()
    userDataL = session.query(User).all()
    userData = []
    for user in userData:
    	userData.append(user.adminDict())
 	storyDataL = session.query(Book).all()
 	storyData = []
 	for story in storyData:
    	storyData.append(story.adminDict())
 	artDataL = session.query(Art).all()
 	artData = []
 	for art in artDataL:
 		artData.append(art.adminDict())  	
   	ret = {
   		"story": storyData
   		"users": userData
   		"art": artData
   	}
    session.close()
    return ret


def adminAction():
    return None

