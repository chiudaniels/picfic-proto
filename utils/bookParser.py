import pymongo
from pymongo import MongoClient
import string

server = MongoClient( "127.0.0.1 " )

db = server.picfic

cB = db.books


#If every page has a marker, give it one. Right now, there's one after every line.
def parseBook( textFilename, metaFilename ): #get the text formatted
    printable = set(string.printable)
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
    #bookData["meta"]["thumbName"] = metaList[4]
    bookData["galMeta"] = {
        "title": metaList[0],
        "author": metaList[1]
        #"thumbnail": metaList[4]
    }
    #hope that the blurb is 1 paragraph... or restructure
    
    textFile = open(textFilename, "r")
    textText = textFile.readlines()
    #goals: find the chapters, find the splits.
    #manually parse through text...
    chCt = 0
    pgCt = 0
    for ln in textText:        
        line = filter(lambda x: x in printable, ln)
        if line.isspace():
            continue
        if "CHAPTER" in line:
            bookData["chapters"].append({
                "bookID" : bookID,
                "pages" : [],
                "title": line
            })
            bookData['chapters'][chCt]["pages"].append(
                {"text": [],
                 "marker": newMarker()
                }
            )
            print "Chapter " + str(chCt)
            #print bookData["chapters"][chCt]
            print "CHAPTER INSERTED"
            pgCt = 0
            chCt += 1
        elif "--------" in line:#replace with ***, new page
            bookData['chapters'][chCt - 1]["pages"].append(
                {"text": [],
                 "marker": newMarker()
                }
            )            
            pgCt += 1
        else:
            #bookData['chapters'][chCt]["pages"][pgCt].append([line, newMarker()])
            #print chCt
            #print pgCt
            #if chCt == 1:
             #   print "Debugging"
              #  print pgCt
               # print bookData["chapters"][chCt - 1]["pages"]
            bookData['chapters'][chCt - 1]["pages"][pgCt]["text"].append(line)
            
    
    textFile.close()
    cB.insert_one(bookData)
    print bookData
    return True
    
def newMarker( ):
    markerData = {
        "imgs":[],
        "markerID": db.markers.count()
    }
    db.markers.insert_one(markerData)
    return markerData["markerID"]

parseBook("../data/texts/aStudyInScarlet.txt", "../data/texts/sampleMeta.txt")
