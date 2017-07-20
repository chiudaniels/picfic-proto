import books, images

#Gallery data retrieval functions

def getPage(userID, PageNum=1, searchQuery=""):
    return books.getGalleryPage(PageNum, searchQuery, userID)


#Data returned should be a list of json objects with each entry being map link data
    #ie. [name:a, author:b, date_updated:c, thumbnail: d (OPTIONAL)]

def userPullImages(userID):
    return images.userFind(userID)
    
#by date updated OR popularity (date updated for now)
#10 entries per page
#def getPage(pageNum):
    # return None
