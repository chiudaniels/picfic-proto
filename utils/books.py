from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import string, re
import users, images

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

def parseBookRaw(textStr, metaStr):
    textArrRaw = textStr.split("\n")
    metaArrRaw = metaStr.split("\n")
    return parseBook(textArrRaw, metaArrRaw)

def parseBookFile(textFilename, metaFilename):
    metaFile = open(metaFilename, "r")
    metaList = metaFile.readlines()
    metaFile.close()
    textFile = open(textFilename, "r")
    textText = textFile.readlines()
    textFile.close()
    return parseBook(textText, metaList)
    
def parseBook(textArr, metaArr):
    session = Session()

    #cleanse both arrs, prelim, (quotes don't matter the future is now)
    printable = set(string.printable)

    textText = []
    metaList = []

    for ln in textArr:
        line = filter(lambda x: x in printable, ln)
        if line.isspace():
            continue
        else:
            textText.append(line)
    for ln in metaArr:
        line = filter(lambda x: x in printable, ln)
        if line.isspace():
            continue
        else:
            metaList.append(line)
    #ur gonna need a better regex filter
    
    #Make book
    bT = metaList[0]
    bA = metaList[1]
    bR = metaList[2]
    bB = metaList[3]
    bM = metaList[4]
    aID = 1
    newBook = Book(bA, bT, bR, bB, bM, aID)
    
    session.add(newBook)
    session.flush()
    #retrieve that bookID!
    bookID = newBook.bookID
    #Distinguish chapters for parsing, modularized for future
    chapterMasterArr = []
    curChDict = {}
    curChDict["text"] = []
    for line in textText:
        if "CHAPTER" in line.upper():
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

    session.close()
    
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
            curPageStartCC = curCC #like list, non-last inclusive
            pageCC += newCCStr
        else:
            line = line.strip()
            curCC += len(line) + 1 #put in the extra character count for the bar. Image cc is gonna get screwweeedddd :((
            processedText += line + "|"
    #PUSH LAST CHAPTER BOOKMARKS!
    newCCStr = str(curPageStartCC) + "," + str(curCC)
    pageCC += newCCStr
    processedText = processedText[:-1]
    newChapter = Chapter(bookID, chTitle, chNum, processedText, pageCC)
    session.add(newChapter)
    session.commit()
    session.close()

def setCover( bookID, url ):
    session = Session()
    book = session.query(Book).filter(Book.bookID == bookID).one()
    book.coverUrl = url
    session.commit()
    session.close()

def setBackground( bookID, url ):
    session = Session()
    book = session.query(Book).filter(Book.bookID == bookID).one()
    book.backgroundUrl = url
    session.commit()
    session.close()
    
def getBookPreview( bookID ):
    print "getting book preview"
    print bookID
    session = Session()
    book = session.query(Book).filter(Book.bookID == bookID).one()
    ret =  {
        "bookID" : bookID,
        "title" : book.title,
        "coverUrl" : book.coverUrl,
        "author" : book.author
    }
    session.close()
    return ret


def getBookLanding( bookID ):
    bookID = int(bookID)
    session = Session()
    book = session.query(Book).filter_by(bookID = bookID).one()

    if book == None:
        session.close()
        return { "bookID" : bookID, "status": 0 }
    else:
        ret = { "bookID" : bookID }
        ret["meta"] = {
            "title": book.title,
            "author": book.author,
            "misc": book.misc,
            "blurb": book.blurb.split("|"),
            "release": book.release
        }
        ret["imageData"] = images.getImageDataBook(bookID)
        ret["coverUrl"] = book.coverUrl
        ret["backgroundUrl"] = book.backgroundUrl
        ret["status"] = 1
        session.close()
        return ret


def getPageData( bookID, chNum, userID ):
    session = Session()
    bookID = int(bookID)
    chNum = int(chNum)
    bookmark = users.getCC(userID, bookID) #gets character count
    print "GET PAGE DATA DEBUG"
    print bookmark
    
    properChQ = session.query(UserBook).filter(UserBook.readerID == userID, UserBook.bookID == bookID)
    if properChQ.count() == 0:
        properCh = 0
    else:
        properCh = properChQ.one().curChapter
    if chNum != properCh:
        bookmark = 0
        properChQ.one().curChapter = chNum
        properChQ.one().curCC = 0
        session.commit()
    
    ret = {"status": 0}
    
    book = getBook(bookID)
    if book != None:
        ret["bookID"] = bookID
        ret["bookLength"] = getBookLength(bookID)
        ret["chNum"] = chNum
        chapterID = getChapterID(bookID, chNum)
        ret["chTitle"] = getChapterTitle(chapterID)
        ret["pgData"] = getPageInfo(bookmark, chapterID)
        ret["pgData"]["curCC"] = bookmark
        start = ret["pgData"]["startCC"]
        end = ret["pgData"]["endCC"]
        if start == -1 and end == -1:
            ret["imageData"] = images.getImageDataChapter(chapterID) 
        else:
            ret["imageData"] = images.getImageDataPage(chapterID, start, end)
        ret["status"] = 1

    session.close()
    return ret


def getPageAJAX(bID, chN, curCC, curPg):
    session = Session()
    bookID = int(bID)
    chNum = int(chN)
    curCC = int(curCC)
    curPg = int(curPg)
    ret = {"status": 0}
    book = getBook(bookID)
    if book != None:
        chapterID = getChapterID(bookID, chNum)
        ret["bookID"] = bookID
        ret["chNum"] = chNum
        ret["pgData"] = getPageInfoAJAX(curPg, chapterID)
        start = ret["pgData"]["startCC"]
        end = ret["pgData"]["endCC"]
        if start == -1 and end == -1:
            ret["imageData"] = images.getImageDataChapter(chapterID) 
        else:
            ret["imageData"] = images.getImageDataPage(chapterID, start, end)
        ret["status"] = 1
        ret["bookLength"] = getBookLength(bookID)
    session.close()
    return ret

def getEndOfChCC(bID, chN):
    print "end of ch cc debug"
    print chN
    #i'm lazy
    session = Session()
    chapter = session.query(Chapter).filter(Chapter.chapterID == getChapterID(bID, chN)).one()
    pageCCStrArr = chapter.pageCC.split(":")
    lastPair = pageCCStrArr[-1].split(",")
    session.close()
    return int(lastPair[1]) - 1
#return getPageInfo(  , getChapterID(bID, chN))["endCC"] - 1

def getChLength(bID, chN):
    session = Session()
    chapter = session.query(Chapter).filter(Chapter.chapterID == getChapterID(bID, chN)).one()
    chLength = chapter.pageCC.count(":") + 1
    session.close()
    return chLength
    
#Returns: images. that's it. and chN 
def getChapterSummary(bID, chN):
    ret = {}
    bID = int(bID)
    chN = int(chN)
    ret["imageData"] = images.getImageDataChapter(getChapterID(bID, chN))
    ret["bookID"] =bID
    ret["bookLength"] = getBookLength(bID)
    ret["chapterNum"] = chN
    ret["pgNum"] = -1
    return ret
    
#Helpers ======================================
def getBook( bookID ):
    bookID = int(bookID)
    session = Session()
    book = session.query(Book).filter_by(bookID = bookID).one()
    session.close()
    return book

def getBookLength( bookID ):
    session = Session()
    ret = session.query(Chapter).filter_by(bookID = bookID).count()
    session.close()
    return ret
    
#Returns {"pgNum", "text", "chLength", "curCC", "startCC", "endCC"}
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
        
    if cc == -1: #get gallery info
        ret["pgNum"] = -1
        ret["text"] = []
        ret["startCC"] = -1
        ret["endCC"] = -1
        ret["curCC"] = -1
    else:
        thePairIndex = 0
        ret["pgNum"] = 1 #default
        for i in range(ret["chLength"]):
            pair = pageCCArr[i]
            if cc >= pair[0] and cc < pair[1]:
                ret["pgNum"] = i + 1 #user index friendly af
                thePairIndex = i
                break
            print pageCCArr[thePairIndex]
        textStr = chapter.text[pageCCArr[thePairIndex][0]:pageCCArr[thePairIndex][1]]
        #ugh...
        ret["text"] = textStr.split("|")
        #RESUME EDITING WHITE SPACE IS A NIGHTMARE
        ret["curCC"] = pageCCArr[thePairIndex][0]
        ret["startCC"] = ret["curCC"]
        ret["endCC"] = pageCCArr[thePairIndex][1]
        #note: you're gonna hate urself
    session.close()
    return ret

def getPageInfoAJAX( pgN, chID ):
    ret = {}
    session = Session()
    chapter = session.query(Chapter).filter_by(chapterID = chID).one()
    pageCCStrArr = chapter.pageCC.split(":")
    pageCCArr = []
    ret["pgNum"] = pgN

    debug(pgN)
    print "\n\n\n"
    
    for pair in pageCCStrArr:
        strPair = pair.split(",")
        pageCCArr.append([int(strPair[0]), int(strPair[1])])

    ret["chLength"] = len(pageCCArr)
    if pgN == -1: #get gallery info
        ret["pgNum"] = -1
        ret["text"] = []
        ret["startCC"] = -1
        ret["endCC"] = -1
        ret["curCC"] = -1
    else:
        thePairIndex = pgN - 1
        textStr = chapter.text[pageCCArr[thePairIndex][0]:pageCCArr[thePairIndex][1]]
        ret["text"] = textStr.split("|")
        ret["curCC"] = pageCCArr[thePairIndex][0]
        ret["startCC"] = pageCCArr[thePairIndex][0]
        ret["endCC"] = pageCCArr[thePairIndex][1]
    #print "curCC retrieved from db"
    #print ret["curCC"]
    #print "end"
    #note: you're gonna hate urself
    session.close()
    return ret


def getChapterID( bookID, chNum ):
    session = Session()
    res = session.query(Chapter).filter(Chapter.bookID == bookID, Chapter.chapterNum == chNum) #should only give one
    if res.count() != 1:
        session.close()
        return None #something's wrong
    ret =res.one().chapterID
    session.close()
    return ret


def getChapterTitle( chapterID ):
    session = Session()
    res = session.query(Chapter).filter(Chapter.chapterID == chapterID)
    if res.count() != 1:
        session.close()
        return None #something's wrong
    ret = res.one().title
    session.close()
    return ret
    
def getBookTitle( bookID ):
    session = Session()
    res = session.query(Book).filter(Book.bookID == bookID)
    ret = res.one().title
    session.close()
    return ret
    
def debug(s):
    print "DEBUG"
    print s
    print "END DEBUG"


#parseBookManual("../data/texts/aStudyInScarlet.txt", "../data/texts/sampleMeta.txt")
