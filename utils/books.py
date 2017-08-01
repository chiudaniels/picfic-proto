from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import string, re
import userDb, images

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

def parseBook(textFilename, metaFilename):
    session = Session()

    #Make book
    metaFile = open(metaFilename, "r")
    metaList = metaFile.readlines()
    metaFile.close()
    bT = metaList[0]
    bA = metaList[1]
    bR = metaList[2]
    bB = metaList[3]
    bM = metaList[4]
    newBook = Book(bA, bT, bR, bB, bM)

    session.add(newBook)
    session.flush()
    #retrieve that bookID!
    bookID = newBook.bookID
    printable = set(string.printable)
    #Distinguish chapters for parsing, modularized for future
    textFile = open(textFilename, "r")
    textText = textFile.readlines()
    chapterMasterArr = []
    curChDict = {}
    curChDict["text"] = []
    for ln in textText:
        line = filter(lambda x: x in printable, ln)
        if line.isspace():
            continue
        if "CHAPTER" in line:
            print "Chapter detected"
            #flush last chapter's text to array, reset
            if "title" in curChDict.keys():
                print "last chapter appended"
                #print curChDict
                chapterMasterArr.append(curChDict)
            curChDict = {"title": line, "text": []}
            #print "Title"
            print curChDict["title"]
        else: #regular or page break, whatever
            curChDict["text"].append(line)
    #flush last chapter
    if "title" in curChDict.keys():
        chapterMasterArr.append(curChDict)
    session.commit()
    #done splitting, parse them all
    for i in range(len(chapterMasterArr)):
        ch = chapterMasterArr[i]
        #print ch["text"]
        addNewChapter(ch["title"], ch["text"], bookID, i + 1)

    textFile.close()
    return True

def addNewChapter(chTitle, chText, bookID, chNum): #chText is array
    session = Session()
    #chText is an array
    curCC = 0
    processedText = ""
    pageCC = ""
    curPageStartCC = 0
    
    """Current formatting for pageCC
    <int>,<int>:<int>,<int>:...
    
    """
    #off by one hell
    for line in chText:
        if "--------" in line:#page break
            #print "page break reee"
            newCCStr = str(curPageStartCC) + "," + str(curCC) + ":"
            #print newCCStr
            curPageStartCC = curCC + 1
            pageCC += newCCStr
        else:
            line = line.strip()
            curCC += len(line)
            processedText += line
    pageCC = pageCC[:-1]
    
    newChapter = Chapter(bookID, chTitle, chNum, processedText, pageCC)
    session.add(newChapter)
    session.commit()

#parseBook("../data/texts/aStudyInScarlet.txt", "../data/texts/sampleMeta.txt")

    
def getBookLanding( bookID ):
    bookID = int(bookID)
    session = Session()
    book = session.query(Book).filter_by(bookID = bookID).one()

    if book == None:
        return { "bookID" : bookID, "status": 0 }
    else:
        ret = { "bookID" : bookID }
        ret["meta"] = {
            "title": book.title,
            "author": book.author,
            "misc": book.misc,
            "blurb": book.blurb,
            "release": book.release
        }
        ret["status"] = 1
        return ret


def getPageData( bookID, chNum, userID ):
    bookID = int(bookID)
    chNum = int(chNum)
    bookmark = userDb.getCC(userID, bookID) #gets character count
    
    ret = {"status": 0}
    
    book = getBook(bookID)
    if book != None:
        chapterID = getChapterID(bookID, chNum)
        ret["bookID"] = bookID
        ret["bookLength"] = getBookLength(bookID)
        ret["chNum"] = chNum
        ret["chTitle"] = getChapterTitle(chapterID)
        ret["pgData"] = getPageInfo(bookmark, chapterID)
        start = ret["pgData"]["startCC"]
        end = ret["pgData"]["endCC"]
        ret["imageData"] = images.getImageData(chapterID, start, end)
        ret["status"] = 1
    return ret


def getPageAJAX(bID, chN, pgN):
    session = Session()
    bookID = int(bID)
    chNum = int(chN)
    pgNum = int(pgN)
    ret = {"status": 0}
    book = getBook(bookID)
    if book != None:
        chapterID = getChapterID(bookID, chNum)
        ret["bookID"] = bookID
        ret["chNum"] = chNum
        ret["pgData"] = getPageInfoAJAX(pgNum, chapterID)
        start = ret["pgData"]["startCC"]
        end = ret["pgData"]["endCC"]
        ret["imageData"] = images.getImageData(chapterID, start, end)
        ret["status"] = 1
        ret["bookLength"] = getBookLength(bookID)
    return ret
        
#Helpers ======================================
def getBook( bookID ):
    bookID = int(bookID)
    session = Session()
    book = session.query(Book).filter_by(bookID = bookID).one()
    return book

def getBookLength( bookID ):
    session = Session()
    return session.query(Chapter).filter_by(bookID = bookID).count()
                                                             
#Returns {"pgNum", "text", "chLength", "curCC"}
def getPageInfo( cc, chID ):

    ret = {}
    session = Session()
    chapter = session.query(Chapter).filter_by(chapterID = chID).one()
    pageCCStrArr = chapter.pageCC.split(":")
    pageCCArr = []
    for pair in pageCCStrArr:
        strPair = pair.split(",")
        pageCCArr.append([int(strPair[0]), int(strPair[1])])

    ret["chLength"] = len(pageCCArr)
    thePairIndex = 0
    ret["pgNum"] = 1 #default
    for i in range(ret["chLength"]):
        pair = pageCCArr[i]
        print pair
        if cc >= pair[0] and cc < pair[1]:
            ret["pgNum"] = i + 1 #user index friendly af
            thePairIndex = i
            break
    textStr = chapter.text[pageCCArr[thePairIndex][0]:pageCCArr[thePairIndex][1] + 1] #don't drop the last char
    
    ret["text"] = re.split("\r\n|\n",textStr)
    #RESUME EDITING WHITE SPACE IS A NIGHTMARE
    ret["curCC"] = cc
    ret["startCC"] = pageCCArr[thePairIndex][0]
    ret["endCC"] = pageCCArr[thePairIndex][1]
    #note: you're gonna hate urself
    return ret

def getPageInfoAJAX( pgN, chID ):
    ret = {}
    session = Session()
    chapter = session.query(Chapter).filter_by(chapterID = chID).one()
    pageCCStrArr = chapter.pageCC.split(":")
    pageCCArr = []
    ret["pgNum"] = pgN
    
    for pair in pageCCStrArr:
        strPair = pair.split(",")
        pageCCArr.append([int(strPair[0]), int(strPair[1])])

    ret["chLength"] = len(pageCCArr)
    thePairIndex = pgN - 1
    textStr = chapter.text[pageCCArr[thePairIndex][0]:pageCCArr[thePairIndex][1] + 1] #don't drop the last char
    ret["text"] = textStr.split("\r\n")
    ret["curCC"] = pageCCArr[thePairIndex][0]
    print "curCC retrieved from db"
    print ret["curCC"]
    print "end"
    #note: you're gonna hate urself
    return ret

    
def getChapterID( bookID, chNum ):
    session = Session()
    res = session.query(Chapter).filter(Chapter.bookID == bookID, Chapter.chapterNum == chNum) #should only give one
    if res.count() != 1:
        return None #something's wrong
    return res.one().chapterID


def getChapterTitle( chapterID ):
    session = Session()
    res = session.query(Chapter).filter(Chapter.chapterID == chapterID)
    if res.count() != 1:
        return None #something's wrong
    return res.one().title
    

def debug(s):
    print "DEBUG"
    print s
    print "END DEBUG"
