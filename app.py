from flask import Flask, render_template, request, session, url_for, redirect
from utils import users, books, gallery
import json, os


app = Flask(_name_)
app.secret_key = "secrets"

#UPLOAD_FOLDER = join(dirname(), "maps/")

#Site navigation

#Reminder: Minimum Viable Product!

#TODO:
#Launchpad
#User settings
#Book gallery
#Book page

# == Launchpad ======================================

@app.route("/")
def root():
    return render_template("launch.html")

# == Settings =======================================

@app.route("/settings/")
def settings():
    if isLoggedIn():
        return render_template( "settings.html" )
    return redirect( url_for('root') )

# == About ==========================================

@app.route("/about/")
def about():
    return render_template( "about.html", isLoggedIn = isLoggedIn() )



# == Book Gallery Browsing ==========================

@app.route("/gallery/")
def galleryRoute():
    return redirect("/gallery/browse/page/1")

@app.route("/gallery/browse/page/<pageNum>")
def galleryPage(pageNum):
    data = gallery.getPage(getUserID(), pageNum) #<-- get back later
    if len(data) == 0:
        return render_template("gallery.html", isLoggedIn = isLoggedIn(), message = "There are no books at this time")
    else:
        return render_template("gallery.html", isLoggedIn = isLoggedIn(), galleryData = data , message = "You are viewing the gallery")


# == Book landing page ==============================

@app.route("/books/<bookID>")
def bookLanding(bookID):
    metadata = books.getBookMetadata(bookID)
    return render_template("bookLanding.html", isLoggedIn = isLoggedIn(), bookData = metadata)


# == reading =====

@app.route("/books/<bookID>/read")
def bookRedir(bookID):
    return redirect("/books/<bookid>/read/1/1")

@app.route("books/<bookID>/read/<chNum>/<pgNum>")
def bookPage(bookID, chNum, pgNum):
    data = books.getPageData(bookID, chNum, pgNum)
    if data == None or len(data) == 0:
        print "Something went wrong"
    else:
        return render_template("bookPage.html", isLoggedIn = isLoggedIn(), pageData = data , message = "You are reading")

    
#=================== END SITE NAVIGATION =======================

# Login Routes ======================================

@app.route("/login/", methods=["POST"])
def login():
    # request
    uN = request.form["username"]
    pwd = request.form["password"]
    #auth
    msg = ""
    if 'login' in request.form:
        if users.isValidAccountInfo( uN, pwd ):
            session['uID'] = users.getUserID( uN )
        else:
            msg = "Invalid credentials"
    else:
        message = "How"
    return redirect( url_for('root', message=msg) )

@app.route("/logout/")
def logout():
    session.pop('uID')
    return redirect( url_for('root') )

@app.route("/register/", methods=["POST"])
def register():
    # request
    uN = request.form["username"]
    pwd = request.form["password"]
    #reg
    msg = ""
    if users.canRegister(uN):
        users.registerAccountInfo( uN, pwd )
        session['uID'] = users.getUserID( uN )
    else:
        msg = "User already exists"
    return redirect( url_for('root', message=msg) )

# Setting Routes ======================================

@app.route('/changePass/', methods = ['POST'])
def changePass():
    if isLoggedIn():
        d = request.form
        old = d["pass"]
        new1 = d["pass1"]
        new2 = d["pass2"]
        users.changePass( getUserID(), old, new1, new2 )
    return redirect(url_for('root'))


# General Helpers =====================================

# Login Helpers
def isLoggedIn():
    return "uID" in session

def getUserID():
    if isLoggedIn():
        return session["uID"]
    else:
        return None

if __name__ == "__main__":
    app.debug = True
    app.run()
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    
print __name__
