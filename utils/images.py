from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import users, books

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
def getImageDataPage(chID, startCC, endCC):
    session = Session()
    imgQ = session.query(Art.uploaderID, Art.caption, Art.urlName).filter(Art.chapterID == chID, Art.startCC > ccStart, Art.ccEnd < endCC)
    #print imgQ
    
    if imgQ.count() != 0:
        imgList = imgQ.all()
        print imgList
        retList = []
        for entry in imgList:
            retList.append(entry.__dict__)
        return retList
    
    return []

#For a chapter
def getImageDataChapter(chID):
    session = Session()
    imgQ = session.query(Art.uploaderID, Art.caption, Art.urlName).filter(Art.chapterID == chID)
    #print imgQ
    
    if imgQ.count() != 0:
        imgList = imgQ.all()
        print imgList
        print "chapter data retrieval"
        retList = []
        for entry in imgList:
            retList.append(entry.__dict__)
        return retList

    return []


#For a book
def getImageDataBook(bID):
    session = Session()
    imgQ = session.query(Art.uploaderID, Art.caption, Art.ccStart, Art.ccEnd, Art.urlName).filter(Art.bookID == bID)
    #print imgQ
    
    if imgQ.count() != 0:
        imgList = imgQ.all()
        print imgList
        print "book data retrieval"
        retList = []
        for entry in imgList:
            retList.append(entry.__dict__)
        return retList
    return []


#For a user
def getImageDataUser(uID):
    session = Session()
    imgQ = session.query(Art.caption, Art.bookID, Art.urlName).filter(Art.uploaderID == uID)
    #print imgQ
    
    if imgQ.count() != 0:
        imgList = imgQ.all()
        print imgList
        retList = []
        for entry in imgList:
            retList.append(entry.__dict__)
            retList[-1]["bookTitle"] = books.getBook(retList[-1]["bookID"]).title
        print "user data retrieval"
        return retList

    return []

#Conglomerate with like data
#def getImageData():


