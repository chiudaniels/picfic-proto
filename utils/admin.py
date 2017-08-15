from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import users, books, images, os

# admin.py - Administrative Functions for the Admin Page

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

# getAdminPageData () - returns data used to populate admin page
# pre  : 
# post : dict - all the data for all users, stories and art
#        { dict stories : dictionary form of the story object
#          dict users   : user data
#          dict art     : art data } 
def getAdminPageData():
    session = Session()
    userDataL = session.query(User).all()
    userData = []
    for user in userDataL:
        print user
        d = user.adminDict()
        #this some kinda ghetto join
        d1 = session.query(UserProfile).filter(UserProfile.userID == d["userID"]).one().adminDict()
        d.update(d1)
        userData.append(d)
        if d["usergroup"] == 1:
            d["usergroup"] = "unactivated"
        elif d["usergroup"] == 2:
            d["usergroup"] = "active"
        elif d["usergroup"] == 3:
            d["usergroup"] = "admin"
    storyDataL = session.query(Book).all()
    storyData = []
    for story in storyDataL:
        d = story.adminDict()
        d["username"] = users.getUsername(d["authorID"])
        storyData.append(d)
    artDataL = session.query(Art).all()
    artData = []
    for art in artDataL:
        d = art.adminDict()
        d["title"] = books.getBookTitle(d["bookID"])
        d["username"] = users.getUsername(d["uploaderID"])
 	artData.append(d)  	
    ret = {
   	"stories": storyData,
   	"users": userData,
   	"art": artData
    }
    session.close()
    return ret

# adminAction (..) - executes actions on admin page
# pre  : dict dat - data with keys describing what action to perform
#        { String type  : string form of table accessed [see in line comments]
#          String act   : string form of action performed [see in line comments]
#          String rowID : string form of entry }
# post : action is executed, database is changed appropriately 
def adminAction(dat):
    session = Session()
    data = {}
    for key in dat.keys():
        data[key] = int(dat[key])
    print data
    rowID = data["rowID"] # Robustify Later With Error Checking
    if data["type"] == 0: #story
        story = session.query(Book).filter(Book.bookID == rowID)
        if data["act"] == 1: #approve
            story.one().approve()
        elif data["act"] == 2: #delete
            chapter = session.query(Chapter).filter(Chapter.bookID == rowID)
            # print "Wow!:", chapter.all() # Debugging
            for ch in chapter:
                userchapter = session.query(UserChapter).filter(UserChapter.chapterID == ch.chapterID)
                userchapter.delete()
                chapterart = session.query(Art).filter(Art.chapterID == ch.chapterID)
                chapterart.delete()
            chapter.delete()
            art = session.query(Art).filter(Art.bookID == rowID)
            art.delete()
            userbook = session.query(UserBook).filter(UserBook.bookID == rowID)
            userbook.delete()
            img = os.path.join("static/data/bookCovers/", story.one().coverUrl)
            print img
            try:
                os.remove(img)
            except:
                print "Image does not exist."
            story.delete()
    elif data["type"] == 1: #art
        art = session.query(Art).filter(Art.artID == rowID)
        if data["act"] == 1: #delete
            art.delete()
    elif data["type"] == 2: #user
        user = session.query(User).filter(User.userID == rowID)
        if data["act"] == 1: #promote
            user.one().promote()
        elif data["act"] == 2: #delete
            user.delete()
    session.commit()
    session.close()
    return {"status" : "True"}

