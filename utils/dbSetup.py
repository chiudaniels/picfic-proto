from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Table, CheckConstraint, UniqueConstraint

from sqlalchemy.orm import sessionmaker, relationship
#from sqlalchemy.sql.functions import GenericFunction
import datetime
from sqlalchemy import create_engine

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

"""
Concerns:
userChapter / userBook - possible poor db design
text/url in text storage? ("Chapters" table)
pageCC : array or string? 
do we care about who likes or just like count?
do we care about who's reading? 
following omitted for now (self referencing is scary)
Constraints are not comprehensive
#Not worrying about deletes right now
#Fix datetime dear god

Questions:
What happens when user deletes account? (Set cascade delete on User class)

Notes:
back_populates - refers to attribute in noted relation's class
relationships follow - this to relation : 1 this to many relation
association table means no extra info.
one to many: many holds foreign key (user is usually the one)
primary_key must be last
NO ASSOCIATION PROXY IS USED

using ch ID (for PK) and ch Num 

"""


followingTable = Table('Following', Base.metadata,
    Column('followerID', Integer, ForeignKey('Users.userID')),
    Column('followedID', Integer, ForeignKey('Users.userID'))
)

"""
usergroup key:
0 - unactivated
1 - activated
2 - admin/editor

Bcrypt used for hash
"""
class User(Base):
    __tablename__ = "Users"

    userID = Column(Integer, primary_key = True)
    username = Column(String(32), unique = True)
    #tag = Column(String, unique = True) #is that a thing?
    email = Column(String, unique = True)
    passData = Column(String)
    usergroup = Column(Integer, CheckConstraint("usergroup >= 0"))
    authTokens = Column(String)

    #Relationships
    userProfile = relationship("UserProfile", back_populates="user", cascade="all, delete, delete-orphan") #one to one
    art = relationship("Art", back_populates="uploader") #one to many

    #people (list) this user is following
    following = relationship("User", secondary= "Following",
                             primaryjoin = "User.userID == Following.c.followerID",
                             secondaryjoin = "User.userID == Following.c.followedID",
                             back_populates="followedBy") #back_populates Following.followed
    followedBy = relationship("User", secondary="Following",
                              primaryjoin = "User.userID == Following.c.followedID",
                              secondaryjoin = "User.userID == Following.c.followerID",
                              back_populates="following")
    
    liked = relationship("Art", secondary = "Likes", back_populates="likers") #many to many
    
    books = relationship("UserBook", back_populates="reader") #many to many
    chapters = relationship("UserChapter", back_populates="reader") #many to many
    
    def __repr__(self):
        return "<User(name='%s', id='%d')>" % (
            self.username, self.userID)

    def __init__(self, username, password, authtokens, email):
        self.usergroup = 0
        self.username = username
        self.passData = password
        self.authtokens = authtokens
        self.email = email

    def activate():
        self.usergroup = 1

    def promote():
        self.usergroup = 2
        
class UserProfile(Base):
    __tablename__ = "UserProfiles"

    userID = Column(Integer, ForeignKey("Users.userID"), primary_key = True)
    firstName = Column(String(20))
    lastName = Column(String(20))
    birthday = Column(Date) #Edit
    gender = Column(String) #Edit
    address = Column(String)
    reference = Column(String)
    favoriteBooks = Column(String(200))
    favoriteAuthors = Column(String(200))
    favoriteGenres = Column(String(200))
    hobbies = Column(String(250))
    about = Column(String(250))
    picUrl = Column(String(250))
    joinDate = Column(Date, default=datetime.datetime.now())
    
    #Relationships
    user = relationship("User", back_populates="userProfile", uselist = False) #one to one
    
    def __repr__(self):
        return "<UserProfile(id='%d')>" % (
            self.userID)

    def __init__(self, uID, fN, lN, bM, bD, bY, gender):
        self.userID = uID
        self.firstName = fN
        self.lastName = lN
        #package birthday
        bday = datetime.datetime(bY, bM, bD)
        self.birthday = bday
        self.gender = "" #figure this out
        self.about = "Nothing about me just yet!"
        self.hobbies = "Nothing written yet!"
        self.favoriteBooks = "Nothing written yet!"
        self.favoriteAuthors = "Nothing written yet!"
        self.favoriteGenres = "Nothing written yet!"
        self.picUrl = "defaultProfilePic.jpg"
        
    #add permission levels    
    def asDict(self):
        return {
            "firstName" : self.firstName,
            "lastName" : self.lastName,
            "birthday" : self.birthday.strftime("%B %d, %Y"),
            "gender" : self.gender,
            "about" : self.about,
            "hobbies" : self.hobbies,
            "favBooks" : self.favoriteBooks,
            "favAuthors" : self.favoriteAuthors,
            "favGenres" : self.favoriteGenres,
            "picUrl" : self.picUrl
        }
        
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
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
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

    def __init__(self, uID, caption, cStart, cEnd, url, bookID, chID):
        self.uploaderID = uID
        self.caption = caption
        self.ccStart = cStart
        self.ccEnd = cEnd
        self.urlName = url
        self.bookID = bookID
        self.chapterID = chID
        #self.timestamp = 0

    def asDict(self):
        return {"uploaderID" : self.uploaderID,
                "caption" : self.caption,
                "urlName" : self.urlName,
                "bookID" : self.bookID
        }
        
class Book(Base):
    __tablename__ = "Books"

    bookID = Column(Integer, primary_key = True)
    #Author is just string rn, extend to author profiles
    author = Column(String(50), nullable = False)
    release = Column(Date) #lol fix this
    title = Column(String(200))
    misc = Column(String)
    blurb = Column(String(2000))
    coverUrl = Column(String)
    backgroundUrl = Column(String)
    
    #Relationships
    art = relationship("Art", back_populates="book")
    chapters = relationship("Chapter", back_populates="book") #one to many
    readers = relationship("UserBook", back_populates="book")
    
    def __repr__(self):
        return "<Book(id='%d')>" % (
            self.bookID )

    def __init__(self, author, title, release, blurb, misc):
        self.author = author
        self.title = title
        self.release = release
        self.blurb = blurb
        self.misc = "FREE DOMAIN"
        self.coverUrl = "defaultBookPic.jpg"
        self.backgroundUrl = ""
        
class Chapter(Base):
    __tablename__ = "Chapters"

    chapterID = Column(Integer, primary_key = True)
    bookID = Column(Integer, ForeignKey("Books.bookID"))
    chapterNum = Column(Integer)
    title = Column(String(200))
    charCount = Column(Integer)
    price = Column(Integer) #Change to money
    release = Column(Date)
    misc = Column(String)
    pageCC = Column(String) #some typa array...
    text = Column(String) #or use url

    book = relationship("Book", back_populates="chapters") #many to one
    art = relationship("Art", back_populates="chapter") #one to many
    #readers = relationship("", back_populates="") #I don't really care about this...
    #revenue? maybe. (Analytics)
    readers = relationship("UserChapter", back_populates="chapter")
    
    def __repr__(self):
        return "<Chapter(bookID='%d', chapterNum='%d')>" % (
            self.bookID, self.chapterNum )

    def __init__(self, bookID, title, chNum, text, pageCC):
        self.bookID = bookID
        self.title = title
        self.chapterNum = chNum
        self.text = text
        self.price = 0
        self.pageCC = pageCC #import an algo from text
        self.charCount = len(text)

    
#=== Many many relationships / Association tables / Association Objects =========================

likeTable = Table('Likes', Base.metadata,
    Column('userID', Integer, ForeignKey('Users.userID')),
    Column('artID', Integer, ForeignKey('Art.artID'))
)

#need a class to configure relationship
"""
class Following(Base):
    __tablename__ = "Following"

    followerID = Column(Integer, ForeignKey("Users.userID"), primary_key = True)
    followedID = Column(Integer, ForeignKey("Users.userID"), primary_key = True)

    follower = relationship("User", back_populates="followedBy", foreign_keys=[followerID]) #user's "books/reading list" are getting back populated when readers are edited
    followed = relationship("User", back_populates="following", foreign_keys=[followedID]) #the book has a "readers" list
   
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
    curChapter = Column(Integer) #defaults as 0 anyway
    curCC = Column(Integer) #defaults as 0

    reader = relationship("User", back_populates="books") #user's "books/reading list" are getting back populated when readers are edited
    book = relationship("Book", back_populates="readers") #the book has a "readers" list

    def __init__(self, uID, bookID):
        self.bookID = bookID
        self.readerID = uID
        self.curCC = 0
        self.curChapter = 0
        
class UserChapter(Base):
    __tablename__ = "UserChapter"

    readerID = Column(Integer, ForeignKey("Users.userID"), primary_key = True)
    chapterID = Column(Integer, ForeignKey("Chapters.chapterID"), primary_key = True)
    permissions = Column(Integer)
    config = Column(String)

    reader = relationship("User", back_populates="chapters") #user's "books/reading list" are getting back populated when readers are edited
    chapter = relationship("Chapter", back_populates="readers") #the book has a "readers" list

    def __init__(self, uID, chID):
        self.chapterID = chID
        self.readerID = uID
        self.config = ""

    
# END CLASS DEFINITIONS ======================================


def makeTables():
    Base.metadata.create_all(engine)

makeTables()
