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
def getImageDataPage(chID, ccStart, ccEnd):
    session = Session()
    imgQ = session.query(Art).filter(Art.chapterID == chID, Art.ccStart > ccStart, Art.ccEnd < ccEnd)
    #print imgQ
    
    if imgQ.count() != 0:
        imgList = imgQ.all()
        print imgList
        retList = []
        for entry in imgList:
            retList.append(entry.asDict())
        return retList
    
    return []

#For a chapter
def getImageDataChapter(chID):
    session = Session()
    imgQ = session.query(Art).filter(Art.chapterID == chID)
    #print imgQ
    
    if imgQ.count() != 0:
        imgList = imgQ.all()
        print imgList
        print "chapter data retrieval"
        retList = []
        for entry in imgList:
            retList.append(entry.asDict())
        return retList

    return []


#For a book
def getImageDataBook(bID):
    session = Session()
    imgQ = session.query(Art).filter(Art.bookID == bID)
    #print imgQ
    
    if imgQ.count() != 0:
        imgList = imgQ.all()
        print imgList
        print "book data retrieval"
        retList = []
        for entry in imgList:
            retList.append(entry.asDict())
        return retList
    return []


#For a user
def getImageDataUser(uID):
    session = Session()
    imgQ = session.query(Art).filter(Art.uploaderID == uID)
    #print imgQ
    
    if imgQ.count() != 0:
        imgList = imgQ.all()
        print imgList
        retList = []
        for entry in imgList:
            retList.append(entry.asDict())
            retList[-1]["bookTitle"] = books.getBook(retList[-1]["bookID"]).title
        print "user data retrieval"
        return retList
    return []

#Conglomerate with like data
#def getImageData():


# == Likes ======================================================

def getNumLikes(artID):
    session = Session()
    imgQ = session.query(Art).filter(Art.artID == artID)
    return len(imgQ.one().likers)

def isLiked(uID, artID):    
    session = Session()
    return session.query(Art).filter(Art.likers.any(userID = uID).count()).count() != 0
    
def likeImage(uID, artID):
    session = Session()
    if users.isActive(uID):
        user = session.query(User).filter(User.userID == uID).one()
        art = session.query(Art).filter(Art.artID == artID).one().likers.append(user)
        return True
    else:
        return False
