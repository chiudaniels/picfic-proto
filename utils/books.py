from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbSetup import *
import string

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
    print "DEBUGGING!!!\n\n"
    print bookID
    print "END DEBUG\n\n"
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
        #print ch
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
            newCCStr = str(curPageStartCC) + "," + str(curCC) + ":"
            curPageStartCC = curCC + 1
            pageCC += newCCStr
        else:
            curCC += len(line)
            processedText += line
        pageCC = pageCC[:-1]
        
    newChapter = Chapter(bookID, chTitle, chNum, processedText, pageCC)
    session.add(newChapter)
    session.commit()
    print "Chapter added"
    print "CHapter stats"
    print chTitle
    print chText
    print chNum

parseBook("../data/texts/aStudyInScarlet.txt", "../data/texts/sampleMeta.txt")

    
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
    return None


def getBook( bookID ):
    bookID = int(bookID)
    session = Session()
    book = session.query(Book).one()
    print book
    return book

#getBook(11)
