from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

def addUser( name, passData ):#add attributes
    session = Session()
    newUser = User(name, passData, "", "") 
    session.add(newUser)

    session.commit()

def deleteUser( uID ):
    session = Session()
    usr = session.query(User).filter_by(userID = uID).one()
    session.delete(usr)
    session.commit()

def getUser( uID ):
    session = Session()
    usr = session.query(User).filter_by(userID = uID).one()
    return usr


def getCC( uID, bookID ):
    return 0
"""
UserBook junction
def getBookMark( uID, bookID ):
    session = Session()
    if uID != None:
        uID = int(uID)
        bookID = int(bookID)
        usr = session.query(User).filter_by(userID = uID).one()
        
    return None
"""
