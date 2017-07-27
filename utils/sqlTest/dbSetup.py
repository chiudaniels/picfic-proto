from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

class User(Base):
    __tablename__ = "Users"

    userID = Column(Integer, primary_key = True)
    username = Column(String)
    tag = Column(String)
    email = Column(String)
    passData = Column(String)
    usergroup = Column(Integer)
    authTokens = Column(String)

    def __repr__(self):
        return "<User(name='%s', id='%d')>" % (
            self.username, self.userID)

class UserProfile(Base):
    __tablename__ = "UserProfiles"

    userID = Column(Integer, primary_key = True, ForeignKey("Users.userID"))
    birthday = Column(Integer) #Edit
    gender = Column(String) #Edit
    address = Column(String)
    reference = Column(String)
    favorites = Column(String)
    interest = Column(String)

    def __repr__(self):
        return "<UserProfile(id='%s')>" % (
            self.userID)

class Art(Base):
    __tablename__ = "Art"

    artID = Column(Integer, primary_key = True)
    uploaderID = Column(Integer, ForeignKey("Users.userID"))
    caption = Column(String)
    
                        
    
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
