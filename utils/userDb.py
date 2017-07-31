from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

def addUser( name, passData, email ):#add attributes
    session = Session()
    newUser = User(name, passData, "", email) 
    session.add(newUser)
    session.commit()
    return newUser.userID

def deleteUser( uID ):
    session = Session()
    usr = session.query(User).filter_by(userID = uID).one()
    session.delete(usr)
    session.commit()

def getUser( uID ):
    session = Session()
    usr = session.query(User).filter_by(userID = uID).one()
    return usr

def doesUserExist( username ):
    session = Session()
    usr = session.query(User).filter_by(username = username)   
    if usr.count() == 0:
        print "usr is none"
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

def bookmark( uID, bID, chN, ccStart, pgN ):
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

def isValidAccountInfo( username, hashedPass ):
    session = Session()
    usr = session.query(User).filter(User.username == username, User.passData == hashedPass)
    return usr.count() != 0


def getUserID( username ):
    session = Session()
    usr = session.query(User).filter(User.username == username)
    return usr.one().userID
