from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

def addUser(Name, PassData):#add attributes
    session = Session()
    newUser = User(username= Name, passData = PassData)
    session.add(newUser)

    session.commit()

def deleteUser(uID):
    session = Session()
    usr = session.query(User).filter_by(userID = uID).one()
    session.delete(usr)
    session.commit()
    
deleteUser(3)
