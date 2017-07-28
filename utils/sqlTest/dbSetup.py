from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Table, CheckConstraint

from sqlalchemy.orm import sessionmaker, relationship


from sqlalchemy import create_engine

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

"""
Concerns:
userChapter / userBook - possible poor db design
text/url in text storage? ("Chapters" table)
pageCC : array or string? 
do we are about who likes or just like count?
do we care about who's reading? 
following omitted for now (self referencing is scary)

Notes:
back_populates - refers to attribute in noted relation's class
relationships follow - this to relation : 1 this to many relation
association table means no extra info.
one to many: many holds foreign key (user is usually the one)
primary_key must be last
NO ASSOCIATION PROXY IS USED

using ch ID (for PK) and ch Num 

"""

class User(Base):
    __tablename__ = "Users"

    userID = Column(Integer, primary_key = True)
    username = Column(String)
    tag = Column(String)
    email = Column(String)
    passData = Column(String)
    usergroup = Column(Integer)
    authTokens = Column(String)

    #Relationships
    userProfile = relationship("UserProfile", back_populates="user") #one to one
    art = relationship("Art", back_populates="uploader") #one to many

    #following = relationship("User", secondary="Following", back_populates="followed")
    #followed = relationship("User", secondary="Following", back_populates="following")
    liked = relationship("Art", secondary = "Likes", back_populates="likers") #many to many
    
    books = relationship("UserBook", back_populates="reader") #many to many
    chapters = relationship("UserChapter", back_populates="reader") #many to many
    
    def __repr__(self):
        return "<User(name='%s', id='%d')>" % (
            self.username, self.userID)

class UserProfile(Base):
    __tablename__ = "UserProfiles"

    userID = Column(Integer, ForeignKey("Users.userID"), primary_key = True) 
    birthday = Column(Integer) #Edit
    gender = Column(String) #Edit
    address = Column(String)
    reference = Column(String)
    favorites = Column(String)
    interest = Column(String)

    #Relationships
    user = relationship("User", back_populates="userProfile", uselist = False) #one to one
    
    def __repr__(self):
        return "<UserProfile(id='%d')>" % (
            self.userID)

class Art(Base):
    __tablename__ = "Art"

    artID = Column(Integer, primary_key = True)
    uploaderID = Column(Integer, ForeignKey("Users.userID"))
    caption = Column(String)
    bookID = Column(Integer, ForeignKey("Books.bookID"))
    chapterID = Column(Integer, ForeignKey("Chapters.chapterID")) #to make this a foreign key or not?
    #character count start
    ccStart = Column(Integer)
    ccEnd = Column(Integer)
    urlName = Column(String)
    timestamp = Column(DateTime)

    #Relationships
    uploader = relationship("User", back_populates="art") #many to one
    book = relationship("Book", back_populates="art") #many to one
    chapter = relationship("Chapter", back_populates="art") #many to one
    likers = relationship("User", secondary = "Likes", back_populates="liked") #many to many
    
    #Constraints
    CheckConstraint('ccStart > 0', name='posCC')
    CheckConstraint('ccEnd > 0', name='limCC')

    def __repr__(self):
        return "<Art(id='%d',uploader='%d'),>" % (
            self.artID, self.uploaderID)
    
class Book(Base):
    __tablename__ = "Books"

    bookID = Column(Integer, primary_key = True)
    #Author is just string rn, extend to author profiles
    author = Column(String)
    release = Column(Date)
    title = Column(String)
    misc = Column(String)
    blurb = Column(String)

    #Relationships
    art = relationship("Art", back_populates="book")
    chapters = relationship("Chapter", back_populates="book") #one to many
    readers = relationship("UserBook", back_populates="book")
    
    def __repr__(self):
        return "<Book(id='%d')>" % (
            self.bookID )
    
class Chapter(Base):
    __tablename__ = "Chapters"

    chapterID = Column(Integer, primary_key = True)
    bookID = Column(Integer, ForeignKey("Books.bookID"))
    chapterNum = Column(Integer)
    title = Column(String)
    charCount = Column(Integer)
    price = Column(Integer) #Change to money
    release = Column(Date)
    misc = Column(String)
    pageCC = Column(String) #some typa array...
    text = Column(String) #or use url

    book = relationship("Book", back_populates="chapters") #many to one
    #readers = relationship("", back_populates="") #I don't really care about this...
    #revenue? maybe. (Analytics)
    readers = relationship("UserChapter", back_populates="chapter")
    
    
    def __repr__(self):
        return "<Chapter(bookID='%d', chapterNum='%d')>" % (
            self.bookID, self.chapterNum )

#=== Many many relationships / Association tables / Association Objects =========================

likeTable = Table('Likes', Base.metadata,
    Column('userID', Integer, ForeignKey('Users.userID')),
    Column('artID', Integer, ForeignKey('Art.artID'))
)
"""
followingTable = Table('Following', Base.metadata,
    Column('followerID', Integer, ForeignKey('Users.userID')),
    Column('followedID', Integer, ForeignKey('Users.userID'))
)
"""
"""
class Like(Base):
    __tablename__ = "Likes"

    userID = Column(Integer, primary_key = True)
    artID = Column(Integer, primary_key = True)
    ForeignKeyConstraint(["userID", "artID"], ["Users.userID", "Art.artID"]) #required to composite

    def __repr__(self):
        return "<Like(userID='%d', artID='%d')>" % (
            self.userID, self.artID )


class Following(Base): #user-user following
    __tablename__ = "Following"

    followerID = Column(Integer, ForeignKey("Users.userID"))
    followedID = Column(Integer, ForeignKey("Users.userID"))
"""

class UserBook(Base): #book-user config
    __tablename__ = "UserBook"

    readerID = Column(Integer, ForeignKey("Users.userID"), primary_key = True)
    bookID = Column(Integer, ForeignKey("Books.bookID"), primary_key = True)
    curChapter = Column(Integer)
    curCC = Column(Integer)

    reader = relationship("User", back_populates="books") #user's "books/reading list" are getting back populated when readers are edited
    book = relationship("Book", back_populates="readers") #the book has a "readers" list
    
class UserChapter(Base):
    __tablename__ = "UserChapter"

    readerID = Column(Integer, ForeignKey("Users.userID"), primary_key = True)
    chapterID = Column(Integer, ForeignKey("Chapters.chapterID"), primary_key = True)
    permissions = Column(Integer)
    config = Column(String)

    reader = relationship("User", back_populates="chapters") #user's "books/reading list" are getting back populated when readers are edited
    chapter = relationship("Book", back_populates="readers") #the book has a "readers" list

    
# END CLASS DEFINITIONS ======================================


def makeTables():
    Base.metadata.create_all(engine)

makeTables()


"""
import psycopg2

conn = psycopg2.connect("dbname=picfic user=postgres")
cur = conn.cursor()

makeUserTable = "CREATE TABLE Users (
userID INT PRIMARY KEY,
username character varying(32) UNIQUE,
pSalt TEXT,
pHash TEXT,
userGroup INT NOT NULL
);"

makeAuthTable = "CREATE TABLE UserAuth (

);"

conn.commit()
conn.close()
"""
