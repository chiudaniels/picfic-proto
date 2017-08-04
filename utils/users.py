from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

def addUser( fN, lN, uN, email, pwd, bM, bD, bY, gender, authTokens ):
    session = Session()
    newUser = User(uN, pwd, "", email)
    session.add(newUser)
    session.flush()
    uID = newUser.userID
    newUserProfile = UserProfile(uID, fN, lN, bM, bD, bY, gender)
    session.add(newUserProfile)
    session.commit()
    return uID

def deleteUser( uID ):
    session = Session()
    usr = session.query(User).filter_by(userID = uID).one()
    session.delete(usr)
    session.commit()

def getUser( uID ):
    session = Session()
    usr = session.query(User).filter_by(userID = uID).one()
    return usr

def getProfile( username ):
    session = Session()
    userID = session.query(User.userID).filter(User.username == username).one()[0]
    profileInfo = session.query(UserProfile).filter(UserProfile.userID == userID).one().asDict()
    return profileInfo

def getProfileSensitive( username ):
    session = Session()
    usr = session.query(User).filter(User.username == username).one()
    return {"email" : usr.email,
            "username" : username
    }


def isNameTaken( username ):
    session = Session()
    usr = session.query(User).filter_by(username = username)   
    if usr.count() == 0:
        print "usr DNE"
        return False
    return True

def getCC( uID, bookID ):
    session = Session()
    usr = session.query(UserBook).filter(UserBook.readerID == uID, UserBook.bookID == bookID)
    if usr.count() == 0:
        #wtf
        newUserBook = UserBook(uID, bookID)
        session.commit()
        return 0
    else:
        entry = usr.one()
        return entry.curCC
    return 0

def bookmark( uID, bID, chN, ccStart ):
    session = Session()
    usr = session.query(UserBook).filter(UserBook.readerID == uID, UserBook.bookID == bID)
    if usr.count() == 0:
        #wtf
        newUserBook = UserBook(uID, bID)
        session.add(newUserBook)
        session.commit()
        return False
    else:
        print "commiting bookmark"
        entry = usr.one()
        entry.curChapter = chN
        entry.curCC = ccStart
        print "entry set"
        print entry.curCC
        session.commit()
    return True

#UserBook junction
def getChapter( uID, bookID ):
    session = Session()
    if uID != None:
        uID = int(uID)
        bookID = int(bookID)
        usr = session.query(UserBook).filter(UserBook.readerID == uID, UserBook.bookID == bookID)
        if usr.count() == 0:
            newUserBook = UserBook(uID, bookID)
            session.add(newUserBook)
            session.commit()
            return 1
        else:
            return usr.one().curChapter
    return 1

def getHashed( email ):
    session = Session()
    usr = session.query(User).filter(User.email == email)
    return usr.one().passData

def getHashedFromID( uID ):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    return usr.one().passData

def setPass( uID, newHash ):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    usr.passData = newHash
    session.commit()

def getUserID( email ):
    session = Session()
    usr = session.query(User).filter(User.email == email)
    return usr.one().userID

def getUserIDFromUsername( uN ):
    session = Session()
    usr = session.query(User.userID).filter(User.username == uN)
    return usr.one()[0]
    
def getUsername( uID ):
    session = Session()
    usr = session.query(User.username).filter(User.userID == uID)
    return usr.one()[0]

def isActive(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID).one()
    return usr.usergroup != 0

def isAdmin(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID).one()
    return usr.usergroup == 2

def activate(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    usr.one().activate()
    return uID

def promote(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    usr.one().promote()
    return uID

def getUsergroup(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    return uID.usergroup
    
def follow(uID, toFollowID):
    session = Session()
    if isActive(uID):
        follower = session.query(User).filter(User.userID == uID).one()
        toFollow = session.query(User).filter(User.userID == toFollowID).one()
        follower.following.append(toFollow)
        toFollow.followedBy.append(follower) #possibly redundant/bad because of back_populate...
        return True
    else:
        return False

#Implement a cleaning mechanism for old profile pictures...    
def setImage( uID, url ):
    session = Session()
    p = session.query(User).filter(User.userID == userID).one()
    p.picUrl = url
    session.commit()


#for profile page
def getActivity( username ):
    uID = getUserIDFromUsername(username)
    ret = {}
    ret.update(getStories(uID))
    ret.update(getReading(uID))
    ret.update(getLikedArt(uID))
    ret.update(getUploadedArt(uID))
    return ret
    
def getStories( uID ):
    session = Session()
    myStories = []
    q = session.query(Books.bookID).filter(Books.authorID == uID).all()
    for bID in q:
        myStories.append(books.getBookPreview(bID))
    return {"myStories": myStories}
    
def getReading( uID ):
    session = Session()
    myShelf = []
    q = session.query(User.books).filter(userID == uID).one()
    for bID in q:
        myShelf.append(books.getBookPreview(bID))
    return {"myShelf": myShelf}

def getUploadedArt( uID ):
    session = Session()
    myUploads = []
    q = session.query(Art).filter(uploaderID == uID).all()
    for aID in q:
        myUploads.append(images.getArtPreview(aID))
    return {"uploadedArt": myUploads}

def getLikedArt( uID ):
    session = Session()
    myLiked = []        
    q = session.query(User.liked).filter(userID == uID).one()
    for aID in q:
        myLiked.append(images.getArtPreview(aID))
    return {"uploadedArt": myLiked}
