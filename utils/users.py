from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import hashlib

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

def addUser( fN, lN, uN, email, pwd, bM, bD, bY, gender, authTokens ):
    session = Session()
    pwd = hasher(pwd)
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
    print "checkmate"
    print usr.count()
    print usr.one().curCC
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

def isValidAccountInfo( email, pwd ):
    hashedPass = hasher(pwd)
    session = Session()
    usr = session.query(User).filter(User.email == email, User.passData == hashedPass)
    return usr.count() != 0

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

def changePass( uN, old, new ):
    return True
    
def changeTag( uID, tag ):
    return True

def hasher(unhashed):
    return hashlib.md5(unhashed).hexdigest()
