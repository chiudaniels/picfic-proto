from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import string, re, datetime
import users, images

# books.py - Book Parsing, Data Mutators and Chapters

Session = sessionmaker()
engine = create_engine('postgresql+psycopg2://postgres:picfic@localhost/picfic')

Session.configure(bind=engine)

# parseBookForm (..) - parses book uploaded by form
# pre  : String title - title of the book
#        String author - author of the book
#        String blurb - blurb of the book
#        String storyText - story text, unparsed
#        int    userID - user's ID
#        String coverUrl - filename of the book cover image
# post : int bID - book ID of created book
#        database is updated with details of the new book
def parseBookForm(title, author, blurb, storyText, userID, coverUrl):
    metaList = [title, author, datetime.date.today(), blurb, "", userID]
    storyArr = storyText.split("\n")
    # print storyArr # Debugging
    bID = parseBook(storyArr, metaList)
    setCover(bID, coverUrl)
    return bID

# parseBookRaw (..) - formats raw data and parses book
# pre  : String textStr - string with book text
#        String metaStr - string with author, title, blurb
# post : int RET - book ID of created book
#        database is updated with details of the new book, default book cover
def parseBookRaw(textStr, metaStr):
    textArrRaw = textStr.split("\n")
    metaArrRaw = metaStr.split("\n")
    return parseBook(textArrRaw, metaArrRaw)

# May Not Be Used
def parseBookFile(textFilename, metaFilename):
    metaFile = open(metaFilename, "r")
    metaList = metaFile.readlines()
    metaFile.close()
    textFile = open(textFilename, "r")
    textText = textFile.readlines()
    textFile.close()
    return parseBook(textText, metaList)

# parseBookCustom (..)   - parses data and updates database with book
# pre  : File textFile   - file with text
#        String title    - title of the book
#        String author   - author name
#        String blurb    - blurb of the book
#        String coverUrl - filename of the cover
#        int userID - user's ID
# post : int bID - ID of created book
#        book is created in database
def parseBookCustom(textFile, title, author, blurb, userID, coverUrl):
    metaList = [title, author, datetime.date.today(), blurb, "", userID]
    textText = textFile.readlines()
    textFile.close()
    bID = parseBook(textText, metaList)
    setCover(bID, coverUrl)
    return bID
# Temporary Function - For New Framework
def parseBookCustom2(title, author, blurb, userID, coverUrl):
    metaList = [title, author, datetime.date.today(), blurb, "", userID]
    textText = ["CHAPTER 1", "Default Text"]
    bID = parseBook(textText, metaList)
    setCover(bID, coverUrl)
    return bID

# createBook (..) - parses data and creates book in database - replaces ParseBookCustom Functions
def createBook(title, author, blurb, userID, coverUrl):
    # Initialize database connection
    session = Session()
    printable = set(string.printable)

    # Book Variables
    newBook = Book(author,
                   title,
                   datetime.date.today(),
                   blurb,
                   "",
                   userID) 
    session.add(newBook)
    session.flush()
    bookID = newBook.bookID
    session.commit()
    session.close()
    setCover(bookID, coverUrl)
    
    print "New Book Created:", bookID # Debugging
    return bookID
    
# DEPRECATED
# parseBook (..) - parses data and updates database with book
# pre  : String[] textArr - array of each line in a story
#        Object[] metaArr - array of metadata
# post : int bookID - book ID of created book
#        book is created in database
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
        line = ln
        if isinstance(line, basestring):
            line = filter(lambda x: x in printable, ln)
            
        if isinstance(line, basestring) and line.isspace():
            continue
        else:
            metaList.append(line)
    #ur gonna need a better regex filter
    # double check carriage returns for windows - \r\n vs \n 

    print "MetaArr:\t", metaArr # Debugging
    print "MetaList:\t", metaList # Debugging
    for c in range(len(metaList)):
        print c, metaList[c]
    
    #Make book
    bT = metaList[0] # Book Title
    bA = metaList[1] # Book Author
    bR = metaList[2] # Date/Time Published
    bB = metaList[3] # Book Blurb
    bM = metaList[4] # Book Miscellany
    aID = metaList[5] # Author ID
    newBook = Book(bA, bT, bR, bB, bM, aID)
    
    session.add(newBook)
    session.flush()
    #retrieve that bookID!
    bookID = newBook.bookID
    print "MAKING NEW BOOK\n\n\n"
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
            # print "Title:", curChDict["title"] # Debugging
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
    return bookID

# addNewChapter (..) - adds a new chapter to existing book
# pre  : String   chTitle - title of chapter
#        String[] chText - text for new chapter
#        int    bookID - ID of book
#        int    chNum - chapter number
# post : int added - 1 if success, -1 if failure
#        adds a new chapter to the given book
def addNewChapter(chTitle, chText, bookID, chNum): #chText is array
    session = Session()
    #chText is an array
    curCC = 0
    processedText = ""
    pageCC = ""
    curPageStartCC = 0
    
    # Current formatting for pageCC
    # <int>,<int>:<int>,<int>:...

    #off by one hell
    if len(chText) == 0:
        return -1 # Fail
    for line in chText:
        line = line.strip()
        if line == "": # Multiple blank lines in a row
            continue
        elif "***" in line: #page break
            #print "page break reee"
            newCCStr = str(curPageStartCC) + "," + str(curCC) + ":"
            #print newCCStr
            curPageStartCC = curCC #like list, non-last inclusive
            pageCC += newCCStr
        else:
            curCC += len(line) + 1 #put in the extra character count for the bar. Image cc is gonna get screwweeedddd :((
            processedText += line + "|"

    #PUSH LAST CHAPTER BOOKMARKS!
    newCCStr = str(curPageStartCC) + "," + str(curCC)
    pageCC += newCCStr
    processedText = processedText[:-1]
    added = -1 # Fail
    try:
        newChapter = Chapter(bookID, chTitle, chNum, processedText, pageCC)
        session.add(newChapter)
        session.commit()
        added = 1 # Success
    except:
        pass # Do Nothing
    session.close()
    return added
    
# setCover (..) - changes book cover
# pre  : int    bookID - id of book to update
#        String url - filename of image 
# post : book cover is updated
def setCover( bookID, url ):
    session = Session()
    book = session.query(Book).filter(Book.bookID == bookID).one()
    book.coverUrl = url
    session.commit()
    session.close()

# Unused 
# setBackground (..) - changes book background
# pre  : int    bookID - id of book to update
#        String url - filename of background image
# post : book cover is updated
def setBackground( bookID, url ):
    session = Session()
    book = session.query(Book).filter(Book.bookID == bookID).one()
    book.backgroundUrl = url
    session.commit()
    session.close()

# getBookPreview (..) - gets preview of book data for use on launchpad
# pre  : int    bookID - id of book to update
#        String url - filename of background image
# post : dict ret - dictionary with preview data
#        { int    bookID   : ID of book
#          String title    : title of book
#          String coverUrl : filename of book cover
#          String author   : author name } 
def getBookPreview( bookID ):
    # print "getting book preview" # Debugging
    # print bookID # Debugging
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
 

# getBookLanding (..) - get data for book landing page 
# pre  : int    bookID - id of book to update
# post : dict ret - dictionary with preview data
#        { int    status    : status of function (0 - fail, 1 - success)
#          int    bookID    : ID of book
#          String coverUrl  : filename of book cover
#          String backgroundUrl : filename of book background
#          String author    : author name
#          dict imageData : list of dictionaries of art pieces associated with book
#          dict meta      : metadata about book [see code] } 
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

# getTableOfContents (..) - get data for table of contents
# pre  : int bookID - id of book to update
#        int userID - id of user  
# post : dict RET - dictionary of an array of dictionaries with ToC data
#        chData { 
#        [ { int    chapterNum : chapter number
#            String title      : title of chapter
#            int    permit     : whether user can read the book } ] } 
def getTableOfContents( bookID, userID ):
    bookID = int(bookID)
    session = Session()
    chapters = session.query(Chapter).filter(Chapter.bookID == bookID).order_by(Chapter.chapterNum).all()
    ret = []
    for chapter in chapters:
        chData = {"chapterNum" : chapter.chapterNum,
                  "title" : chapter.title,
                  "permit" : getPermit(chapter.chapterID, userID)
        }
        ret.append(chData)
    session.close()
    return {"chData" : ret}

# getPermit (..) - get permission status 
# pre  : int chapterID - id of chapter
#        int userID    - id of user  
# post : int ret - permission status (1 - allowed to read, 0 - can't read) 
def getPermit( chapterID, userID ):
    session = Session()
    ret = 1 #change this to get default
    if userID != None:
        q = session.query(UserChapter).filter(UserChapter.readerID == userID, UserChapter.chapterID == chapterID)
        if q.count() == 1:
            ret = q.one().permissions    
    session.close()
    return ret

# getPageData (..) - returns data about a page
# pre  : int bookID - id of book to update
#        int chNum  - chapter number of book
#        int userID - id of user 
# post : dict RET - dictionary of page metadata
#        { int status     : 0 - fail, 1 - success
#          int bookID     : book ID
#          int bookLength : chapter count of book
#          int chNum      : chapter of page
#          String chTitle : title of chapter
#          dict pgData : metadata of page [see getPageInfo] }
def getPageData( bookID, chNum, userID ):
    session = Session()
    bookID = int(bookID)
    chNum = int(chNum)
    bookmark = users.getCC(userID, bookID) #gets character count
    chapterID = getChapterID(bookID, chNum)
    print bookID # Debugging
    print chNum # Debugging
    print chapterID # Debugging
    #register in UserChapter when first page of book is retrieved

    if userID != None:
        usrChQ = session.query(UserChapter).filter(UserChapter.readerID == userID, UserChapter.chapterID == chapterID)
    if usrChQ.count() == 0:
        newUserChapter = UserChapter(userID, chapterID)
        session.add(newUserChapter)
        session.commit()
        
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

# getPageAJAX (..) - returns page data using AJAX 
# pre  : int bID   - book ID 
#        int chN   - chapter number
#        int curCC - current character count, where user has read up to 
#        int curPg - current page user is up to 
# post : dict RET - dictionary of page metadata
#        { int status     : 0 - fail, 1 - success
#          int bookID     : book ID
#          int bookLength : chapter count of book
#          int chNum      : chapter of page
#          dict imageData : image metadata
#          dict pgData    : metadata of page [see getPageInfoAJAX] }
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

# getEndOfChCC (..) - returns last character count of given chapter
# pre  : int bID   - book ID 
#        int chN   - chapter number
# post : int RET - char count of chapter - 1 
def getEndOfChCC(bID, chN):
    # print "end of ch cc debug" # Debugging
    # print chN # Debugging
    session = Session()
    chapter = session.query(Chapter).filter(Chapter.chapterID == getChapterID(bID, chN)).one()
    pageCCStrArr = chapter.pageCC.split(":")
    lastPair = pageCCStrArr[-1].split(",")
    session.close()
    return int(lastPair[1]) - 1

# getChLength (..) - returns page count of chapter 
# pre  : int bID   - book ID 
#        int chN   - chapter number
# post : int chLength - page count 
def getChLength(bID, chN):
    session = Session()
    chapter = session.query(Chapter).filter(Chapter.chapterID == getChapterID(bID, chN)).one()
    chLength = chapter.pageCC.count(":") + 1
    session.close()
    return chLength
    
# getChapterSummary (..) - get images for end of chapter 
# pre  : int bID   - book ID 
#        int chN   - chapter number
# post : dict ret - dictionary with image data
#        { dict imageData : dict of image data
#          int bookID     : book ID
#          int bookLength : length of book
#          int chapterNum : chapter number
#          int pgNum      : -1 } 
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
    
# Helpers ======================================
# getBook (..) - gets book object
# pre  : int bookID - book ID
# post : Book book - book object
def getBook( bookID ):
    bookID = int(bookID)
    session = Session()
    book = session.query(Book).filter_by(bookID = bookID).one()
    session.close()
    return book

# getBookLength (..) - gets number of chapters in a book
# pre  : int bookID - book ID
# post : int ret - number of chapters in given book
def getBookLength( bookID ):
    session = Session()
    ret = session.query(Chapter).filter_by(bookID = bookID).count()
    session.close()
    return ret

# Doc This Later
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
            # print pageCCArr[thePairIndex] # Debugging
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

# Doc This Later
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

# getChapterID (..) - get ID of chapter
# pre  : int bookID - book ID
#        int chNum  - chapter number 
# post : int ret - ID of chapter in given book 
def getChapterID( bookID, chNum ):
    session = Session()
    res = session.query(Chapter).filter(Chapter.bookID == bookID, Chapter.chapterNum == chNum) #should only give one
    if res.count() != 1:
        session.close()
        return None #something's wrong
    ret =res.one().chapterID
    session.close()
    return ret

# getChapterTitle (..) - get chapter's title
# pre  : int chapterID - ID of chapter 
# post : String ret - chapter title
def getChapterTitle( chapterID ):
    session = Session()
    res = session.query(Chapter).filter(Chapter.chapterID == chapterID)
    if res.count() != 1:
        session.close()
        return None #something's wrong
    ret = res.one().title
    session.close()
    return ret

# getBookTitle (..) - get book's title
# pre  : int bookID - book ID
# post : String ret - book title
def getBookTitle( bookID ):
    session = Session()
    res = session.query(Book).filter(Book.bookID == bookID)
    ret = res.one().title
    session.close()
    return ret

# Debugging Function, Prints __repr__ or __str__ of Object
def debug(s):
    print "DEBUG"
    print s
    print "END DEBUG"

#parseBookManual("../data/texts/aStudyInScarlet.txt", "../data/texts/sampleMeta.txt")
