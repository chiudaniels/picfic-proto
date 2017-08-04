from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import users, books, images

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

#Admin page code, etc

def getAdminPageData():
    return None


def adminAction():
    return None

