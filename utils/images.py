from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import userDb, books

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

# Uploading Images
# Given: url, userID, caption, ccStart, ccEnd, bookID, chID
def uploadArt(url, uID, caption, cS, cE, bID, chN ):
    session = Session()
    chID = books.getChapterID(bID, chN)
    newImg = Art(uID, caption, cS, cE, url, bID, chID)
    session.add(newImg)
    session.flush()
    aID = newImg.artID
    session.commit()
    return aID

# Retrieving Images
#For a page
#Raw, img table
#Returns: {url, artistID, artistTag, caption, timestamp} #replace caption with cc?
#Get timestamp later
def getImageData(chID, startCC, endCC):
    session = Session()
    imgQ = session.query(Art.uploaderID, Art.caption, Art.ccStart, Art.ccEnd, Art.urlName).filter(Art.chapterID == chID)
    #print imgQ
    """
    if imgQ.count() != 0:
        imgList = imgQ.all()
        print imgList
        return imgList
"""
    return []

#For a chapter


#For a book


#For a user

#Conglomerate with like data
#def getImageData():


