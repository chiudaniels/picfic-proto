from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import string, re
import users, images

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

def parseBookAuto(textFile):
    return None

def parseBookManual(textFilename, metaFilename):
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
    aID = 1
    newBook = Book(bA, bT, bR, bB, bM, aID)
    
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
        chapterID = getChapterID(bookID, chNum)
        ret["bookID"] = bookID
        ret["bookLength"] = getBookLength(bookID)
        ret["chNum"] = chNum
        ret["chTitle"] = getChapterTitle(chapterID)
        ret["pgData"] = getPageInfo(bookmark, chapterID)
        ret["pgData"]["curCC"] = bookmark
        start = ret["pgData"]["startCC"]
        end = ret["pgData"]["endCC"]
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
        ret["imageData"] = images.getImageDataPage(chapterID, start, end)
        ret["status"] = 1
        ret["bookLength"] = getBookLength(bookID)
    session.close()
    return ret

def getEndOfChCC(bID, chN):
    #i'm lazy
    session = Session()
    chapter = session.query(Chapter).filter(Chapter.chapterID == getChapterID(bID, chN)).one()
    pageCCStrArr = chapter.pageCC.split(":")
    lastPair = pageCCStrArr[-1].split(",")
    session.close()
    return int(lastPair[1]) - 1
#return getPageInfo(  , getChapterID(bID, chN))["endCC"] - 1

#Returns: images. that's it. and chN 
def getChapterSummary(bID, chN):
    ret = {}
    ret["imageData"] = images.getImageDataChapter(getChapter(bID, chN))
    ret["bookID"] = bID
    ret["chapterNum"] = chN
    
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
    session.close()
    return res.one().chapterID


def getChapterTitle( chapterID ):
    session = Session()
    res = session.query(Chapter).filter(Chapter.chapterID == chapterID)
    if res.count() != 1:
        session.close()
        return None #something's wrong
    session.close()
    return res.one().title
    

def debug(s):
    print "DEBUG"
    print s
    print "END DEBUG"


#parseBookManual("../data/texts/aStudyInScarlet.txt", "../data/texts/sampleMeta.txt")
