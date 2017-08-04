from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import users, images, books

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

def getGallery():
    session = Session()
    bookList = session.query(Book).limit(5).all()
    ret = []
    for book in bookList:
        if book.approval != 0:
            ret.append(books.getBookPreview(book.bookID))
    return ret
