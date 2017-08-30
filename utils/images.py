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
    session.close()
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
        session.close()
        # print "Retlist\n", retList # Debugging
        for i in range(len(retList)):
            retList[i]['username'] = users.getUsername(int(retList[i]['uploaderID']))
        return retList
    session.close()
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
        session.close()
        for i in range(len(retList)):
            retList[i]['username'] = users.getUsername(int(retList[i]['uploaderID']))
        return retList
    session.close()
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
        session.close()
        for i in range(len(retList)):
            retList[i]['username'] = users.getUsername(int(retList[i]['uploaderID']))
        return retList
    session.close()
    return []

#For a user - unused lmao
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
        session.close()
        return retList
    session.close()
    return []

def getArtPreview(artID, uID):
    session = Session()
    art = session.query(Art).filter(Art.artID == artID).one()
    prev = art.asDict()
    prev["bookTitle"] = books.getBook(prev["bookID"]).title
    prev["uploaderName"] = users.getUsername( prev["uploaderID"] )
    prev["isLiked"] = 0#not liked
    if uID == None or not users.isActive(uID):
        prev["isLiked"] = -1 #can't like
    elif isLiked(uID, artID):
        prev["isLiked"] = 1
    session.close()
    return prev

# == Likes ======================================================

def getNumLikes(artID):
    session = Session()
    imgQ = session.query(Art).filter(Art.artID == artID)
    ret = len(imgQ.one().likers)
    session.close()
    return ret
    
def isLiked(uID, artID):    
    session = Session()
    ret = session.query(Art).filter(Art.likers.any(userID = uID)).count() != 0
    session.close()
    return ret

def likeImage(uID, artID):
    session = Session()
    if users.isActive(uID):
        user = session.query(User).filter(User.userID == uID).one()
        art = session.query(Art).filter(Art.artID == artID).one().likers.append(user)
        session.commit()
        session.close()
        return True
    else:
        session.close()
        return False
