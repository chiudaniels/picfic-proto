from flask import Flask, render_template, request, session, url_for, redirect, send_from_directory
import flask
from utils import users, books, gallery, images, userDb
from werkzeug.utils import secure_filename
import json, os
from bson import BSON
from bson import json_util

app = Flask(__name__)
app.secret_key = "secrets"

UPLOAD_FOLDER = "static/data/images/"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png"])

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
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
    return render_template("launchpad.html", isLoggedIn = isLoggedIn() )

# == Settings =======================================

@app.route("/settings/")
def settings():
    if isLoggedIn():
        return render_template( "settings.html" )
    return redirect( url_for('root'), isLoggedIn = isLoggedIn() )

# == About ==========================================

@app.route("/about/")
def about():
    return render_template( "about.html", isLoggedIn = isLoggedIn() )



# == Book Gallery Browsing ==========================

@app.route("/gallery/")
def galleryRoute():
    return redirect("/gallery/browse/page/1", isLoggedIn = isLoggedIn() )

@app.route("/gallery/browse/page/<pageNum>")
def galleryPage(pageNum):
    return render_template("gallery.html", isLoggedIn = isLoggedIn() )
"""
    data = gallery.getPage(getUserID(), pageNum) #<-- get back later
    
    if len(data) == 0:
        return render_template("gallery.html", isLoggedIn = isLoggedIn(), message = "There are no books at this time")
    else:
        return render_template("gallery.html", isLoggedIn = isLoggedIn(), galleryData = data , message = "You are viewing the gallery")
"""

# == Book landing page ==============================

@app.route("/books/<int:bookID>")
def bookLanding(bookID):
    metadata = books.getBookLanding(bookID)
    return render_template("bookLandingTemp.html", isLoggedIn = isLoggedIn(), data = metadata)


# == reading =====


@app.route("/books/<int:bookID>/read")
def bookRedir(bookID):
    #get user progress
    return redirect("/books/" + str(bookID) + "/read/" + userDb.getBookmark(getUserID(), bookID)[0])

#How do i pass data about the page to the router if not in the url?
@app.route("/books/<int:bookID>/read/<int:chNum>")
def bookPage(bookID, chNum):
    data = books.getPageData( bookID, chNum, getUserID() )
    return render_template("chapter_template.html", isLoggedIn = isLoggedIn(), pageData = data)

#How do i pass data about the page to the router if not in the url?
@app.route("/getPage/", methods = ["POST"])
def bookPageAJAX():
    print "next page ajax"
    bID = request.form.get("bookID")
    chN = request.form.get("chNum")
    pgN = request.form.get("pgNum")
    data =  books.getPageAJAX(bID, chN, pgN)
#    print jsonify(data)
    return json.dumps(data)

#How do i pass data about the page to the router if not in the url?
@app.route("/bookmark/", methods = ["POST"])
def bookmark():
    bID = request.form.get("bookID")
    chN = request.form.get("chNum")
    pgN = request.form.get("pgNum")
    if isLoggedIn():
        data =  userDb.bookmark(getUserID(), bID, chN, pgN)
    return None


#=================== END SITE NAVIGATION =======================

# Login Routes ======================================

@app.route("/login/", methods=["POST"])
def login():

    # request
    uN = request.form["username"]
    pwd = request.form["password"]
    #auth
    msg = ""
    
    if users.isValidAccountInfo( uN, pwd ):
        session['uID'] = users.getUserID( uN )
        print 'logged in!'
        return redirect( url_for('root'))
    else:
        return flask.Response("fail")


@app.route("/logout/")
def logout():
    session.pop('uID')
    return redirect( url_for('root') )

@app.route("/register/", methods=["POST"])
def register():
    # request
    # IDS: name, makeEmail, confirmEmail, month, day, year, gender
    uN = request.form["username"]
    pwd = request.form["makePass"]
    pwd2 = request.form["confirmPass"]
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
    return redirect(url_for('settings'))

@app.route('/changeTag/', methods = ['POST'])
def changeTag():
    if isLoggedIn():
        d = request.form
        newTag = d["tag"]
        users.changeTag( getUserID(), newTag )
    return redirect(url_for('settings'))




# Photo Upload ==================================================================

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        #flash('No file part')
        print "work"
        return redirect(request.url)
    file = request.files['file']
    print "work2"
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        #flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        markerID = request.form["markerID"]
        caption = request.form["caption"]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        images.saveImage(filename, markerID, getUserID(), caption)
        url = request.url.replace("/upload/", "")
        return redirect(url)
    return None

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)




# General Helpers =====================================

# Login Helpers
def isLoggedIn():
    return "uID" in session

def getUserID():
    if isLoggedIn():
        return session["uID"]
    else:
        return None

# Error Handling =======================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


    
if __name__ == "__main__":
    app.debug = True
    app.run()
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    
print __name__



