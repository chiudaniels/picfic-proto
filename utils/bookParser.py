import pymongo
from pymongo import MongoClient

server = MongoClient( "127.0.0.1 " )

db = server.picfic

cB = db.books

def parseBook( textFilename, metaFilename ): #get the text formatted
    bookData = {}
    bookData["meta"] = {}
    bookData["chapters"] = []
    bookData["markers"] = [] #just the ids
    bookID = db.books.count()
    bookData["bookID"] = bookID
    metaFile = open(metaFilename, "r")
    metaList = metaFile.readlines()
    metaFile.close()
    bookData["meta"]["title"] = metaList[0]
    bookData["meta"]["author"] = metaList[1]
    bookData["meta"]["misc"] = metaList[2]
    bookData["meta"]["blurb"] = metaList[3]
    #hope that the blurb is 1 paragraph... or restructure
    
    textFile = open(textFilename, "r")
    textText = textFile.readlines()
    #goals: find the chapters, find the splits.
    #manually parse through text...
    chCt = 0
    pageCt = 0
    for line in textText:
        if "CHAPTER" in line:
            bookData["chapters"][chCt] = {
                "bookID" : bookID,
                "pages" : [],
                "title": line
            }
            pageCt = 0
            chCount += 1
            bookData['chapters'][chCt][pgCt] = []
        elif "--------" in line:
            pageCt += 1
            bookData['chapters'][chCt][pgCt] = []
        else:
            bookData['chapters'][chCt][pgCt].append(line)
        
    textFile.close()
    cB.insert_one(bookData)
    return True
    
def newMarker():
    markerData = {
        "imgs":[],
        "markerID": db.markers.count()
    }
    db.markers.insert_one(markerData)
    return None
    
parseBook("../data/texts/sampleText.txt", "../data/texts/sampleMeta.txt")
