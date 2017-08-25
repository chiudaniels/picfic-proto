from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import books, images
import string, re

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

# addUser (..) - creates and adds user 
# pre  : String fN     - first name
#        String lN     - last name
#        String uN     - username
#        String email  - email
#        String pwd    - password
#        String gender - gender
#        int bM - birth month
#        int bD - birth day
#        int bY - birth year
#        String authTokens - authToken - unused
# post : int uID - user ID of created user
#        User and UserProfile are created in database 
def addUser( fN, lN, uN, email, pwd, bM, bD, bY, gender, authTokens ):
    session = Session()
    newUser = User(uN, pwd, "", email)
    session.add(newUser)
    session.flush()
    uID = newUser.userID
    newUserProfile = UserProfile(uID, fN, lN, bM, bD, bY, gender)
    session.add(newUserProfile)
    session.commit()
    session.close()
    return uID

# addUser (..) - creates and adds user 
# pre  : int uID - user ID
# post : user is deleted from the database
def deleteUser( uID ):
    session = Session()
    usr = session.query(User).filter_by(userID = uID).one()
    session.delete(usr)
    session.commit()
    session.close()

# getUser (..) - retrieves User object
# pre  : int uID - user ID
# post : User usr - User object from database
def getUser( uID ):
    session = Session()
    usr = session.query(User).filter_by(userID = uID).one()
    session.close()
    return usr

# getUser (..) - retrieves UserProfile object
# pre  : int uID - user ID
# post : UserProfile profileInfo - UserProfile object from database
def getProfile( username ):
    session = Session()
    userID = session.query(User.userID).filter(User.username == username).one()[0]
    profileInfo = session.query(UserProfile).filter(UserProfile.userID == userID).one().asDict()
    session.close()
    profileInfo['username'] = username
    return profileInfo

def getProfileSensitive( username ):
    session = Session()
    usr = session.query(User).filter(User.username == username).one()
    ret = {"email" : usr.email,
            "username" : username
    }
    session.close()
    return ret

def isNameTaken( username ):
    session = Session()
    usr = session.query(User).filter(User.username == username)
    if usr.count() == 0:
        session.close()
        return False # Not Taken
    session.close()
    return True # Taken

def isEmailTaken( email ):
    session = Session()
    usr = session.query(User).filter(User.email == email)   
    if usr.count() == 0:
        session.close()
        return False # Not Taken
    session.close()
    return True # Taken

def getCC( uID, bookID ):
    session = Session()
    usr = session.query(UserBook).filter(UserBook.readerID == uID, UserBook.bookID == bookID)
    if usr.count() == 0:
        #wtf
        newUserBook = UserBook(uID, bookID)
        session.commit()
        session.close()
        return 0
    else:
        entry = usr.one()
        session.close()
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
        session.close()
        return False
    else:
        entry = usr.one()
        #if int(pgN) != -1:
        entry.curChapter = chN
        entry.curCC = ccStart
        #else:
         #   entry.curChapter = chN
          #  entry.curCC = -1
        session.commit()
        session.close()
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
            session.close()
            return 1
        else:
            ret = usr.one().curChapter
            session.close()
            return ret     
    return 1

def getHashed( email ):
    session = Session()
    usr = session.query(User).filter(User.email == email)
    if usr.count() < 1:
        return False # No User With Matching Credentials
    ret =  usr.one().passData
    session.close()
    print "Successful Retrieval!"
    return ret

def getHashedFromID( uID ):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    ret = usr.one().passData
    session.close()
    return ret

def setPass( uID, newHash ):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    usr.passData = newHash
    session.commit()
    session.close()
    
def getUserID( email ):
    session = Session()
    usr = session.query(User).filter(User.email == email)
    ret = usr.one().userID
    session.close()
    return ret
    
def getUserIDFromUsername( uN ):
    session = Session()
    usr = session.query(User.userID).filter(User.username == uN)
    ret = usr.one()[0]
    session.close()
    return ret

def getUsername( uID ):
    session = Session()
    usr = session.query(User.username).filter(User.userID == uID)
    ret = usr.one()[0]
    session.close()
    return ret
    
def isActive(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID).one()
    ret = usr.usergroup > 0 # Change to 1 once activation becomes possible
    session.close()
    return ret

def isAdmin(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID).one()
    ret = usr.usergroup == 3
    session.close()
    return ret
    
def activateByID(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    usr.one().activate()
    session.commit()
    session.close()
    return uID

def promoteByID(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    usr.one().promote()
    session.commit()
    session.close()
    return uID

def getUsergroup(uID):
    session = Session()
    usr = session.query(User).filter(User.userID == uID)
    ret = usr.one().usergroup
    session.close()
    return ret

def follow(uID, toFollowID):
    session = Session()
    if isActive(uID):
        follower = session.query(User).filter(User.userID == uID).one()
        toFollow = session.query(User).filter(User.userID == toFollowID).one()
        follower.following.append(toFollow)
        toFollow.followedBy.append(follower) #possibly redundant/bad because of back_populate...
        session.commit()
        session.close()
        return True
    else:
        return False

#Implement a cleaning mechanism for old profile pictures...    
def saveProfilePic( uID, url ):
    session = Session()
    p = session.query(UserProfile).filter(UserProfile.userID == uID).one()
    p.picUrl = url
    print "what's gone wrong"
    session.commit()
    session.close()

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
    q = session.query(Book.bookID).filter(Book.authorID == uID).all()
    for bID in q:
        # print "BookID:", bID # Debugging
        myStories.append(books.getBookPreview(bID[0]))
    session.close()
    return {"myStories": myStories}
    
def getReading( uID ):
    session = Session()
    myShelf = []
    q = session.query(User).filter(User.userID == uID).one()
    for book in q.books:
        myShelf.append(books.getBookPreview(book.bookID))
    session.close()
    return {"myShelf": myShelf}

def getUploadedArt( uID ):
    session = Session()
    myUploads = []
    q = session.query(Art).filter(Art.uploaderID == uID).all()
    for art in q:
        myUploads.append(images.getArtPreview(art.artID, uID))
    session.close()
    return {"uploadedArt": myUploads}

def getLikedArt( uID ):
    session = Session()
    myLiked = []        
    q = session.query(User).filter(User.userID == uID).one()
    for like in q.liked:
        myLiked.append(images.getArtPreview(like.uploaderID, uID))
    session.close()
    return {"uploadedArt": myLiked}


def saveProfile(data, uID):
    session = Session()

    usrP = session.query(UserProfile).filter(User.userID == uID).one()
    usrP.favoriteBooks = data["bs"].strip()
    usrP.favoriteAuthors = data["authors"].strip()
    usrP.favoriteGenres = data["genre"].strip()
    usrP.about = data["about"].strip()
    session.commit()
    session.close()
