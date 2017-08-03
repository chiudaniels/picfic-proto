from flask import Flask, render_template, request, session, url_for, redirect, send_from_directory, abort, flash
from flask_mail import Mail, Message
from threading import Thread
from itsdangerous import URLSafeSerializer, BadSignature
import flask
from utils import users, books, gallery, images
from werkzeug.utils import secure_filename
import json, os
from bson import BSON
from bson import json_util
#from .decorators import async

app = Flask(__name__)
mail=Mail(app)
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


# == User Profile ===================================
@app.route("/user/myProfile/")
def myProfileRedir():
    if isLoggedIn():
        return redirect('/user/' + str(users.getUsername(getUserID())))
    else:
        return redirect(url_for('root'))

@app.route("/user/<username>")
def userProfilePage(username):
    profileData = users.getProfile( username )
    profileData.update( users.getProfileSensitive( username ) )
    userVis = 0
    if isLoggedIn() and username == users.getUsername( getUserID() ):
        userVis = 1
    return render_template( "profile.html", isLoggedIn = isLoggedIn(), data = profileData, perm = userVis )


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
    return render_template("bookLanding.html", isLoggedIn = isLoggedIn(), data = metadata)

# == Chapter End page ===============================
@app.route("/books/<int:bookID>/read/<int:chNum>/gallery")
def chapterGallery(bookID, chNum):
    chapterGalData = books.getChapterSummary(bookID, chNum)
    return render_template("endOfChapterMockup.html", isLoggedIn = isLoggedIn(), data = chapterGalData)


# == reading =====


@app.route("/books/<int:bookID>/read")
def bookRedir(bookID):
    #get user progress - get appropriate chapter
    #temp - 
    if not isLoggedIn():
        return redirect("/books/" + str(bookID) + "/read/1")
    return redirect("/books/" + str(bookID) + "/read/" + str(users.getChapter(getUserID(), bookID)))

                    #Kill chNum?
#How do i pass data about the page to the router if not in the url?
@app.route("/books/<int:bookID>/read/<int:chNum>")
def bookPage(bookID, chNum):
    
    data = books.getPageData( bookID, chNum, getUserID() )
    #print data["pgData"]
    return render_template("chapter_template.html", isLoggedIn = isLoggedIn(), pageData = data)

#How do i pass data about the page to the router if not in the url?
@app.route("/getPage/", methods = ["POST"])
def bookPageAJAX():
    print "next page ajax"
    bID = request.form.get("bookID")
    chN = request.form.get("chNum")
    curCC =  request.form.get("curCC")
    curPg = request.form.get("curPg")
    data =  books.getPageAJAX(bID, chN, curCC, curPg)
    return json.dumps(data)

#dat do i pass data about the page to the router if not in the url?
@app.route("/bookmark/", methods = ["POST"])
def bookmark():
    bID = request.form.get("bookID")
    chN = request.form.get("chNum")
    ccStart = request.form.get("ccStart")
    pgNum = request.form.get("pgNum")
    if isLoggedIn():
        data =  users.bookmark(getUserID(), bID, chN, ccStart)
        return json.dumps({"status":1})
    return None

@app.route("/getEndOfChPage/", methods = ["POST"])
def endOfCh():
    bID = request.form.get("bookID")
    chN = request.form.get("chNum")
    data = {"endOfChCC" : books.getEndOfChCC(bID, chN)}
    return json.dumps(data)

#=================== END SITE NAVIGATION =======================

# Login Routes ======================================

@app.route("/login/", methods=["POST"])
def login():

    # request
    email = request.form["loginEmail"]
    pwd = request.form["loginPass"]
    #auth
    msg = ""
    
    if users.isValidAccountInfo( email, pwd ):
        session['uID'] = users.getUserID( email )
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
    d = request.form
    print d
    
    fN = request.form["fName"]
    lN = request.form["lName"]
    uN = request.form["username"]
    email = request.form["makeEmail"]
    pwd = request.form["makePass"]
    bM = int(request.form["bMonth"])
    bD= int(request.form["day"])
    bY = int(request.form["year"])
    gender = request.form["gender"]
    #reg
    print "trying to register"
    if not users.isNameTaken(uN): #and email
        print "adding user"
        session['uID'] = users.addUser( fN, lN, uN, email, pwd, bM, bD, bY, gender, "")
    else:
        msg = "User already exists"
    return redirect( url_for('root') )

# Setting Routes ======================================

@app.route('/changePass/', methods = ['POST'])
def changePass():
    if isLoggedIn():
        d = request.form
        old = d["oldPass"]
        new = d["newPass"]
        users.changePass( getUserID(), old, new )
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

@app.route('/uploadArt/', methods=['POST'])
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
        caption = request.form["caption"]
        bID = request.form["bookID"]
        chN = request.form["chapterNum"]
        cStart = request.form["startCC"]
        cEnd = request.form["endCC"]
        print "RECEIVING DATA FROM FORM"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        images.uploadArt(filename, getUserID(), caption, cStart, cEnd, bID, chN)
        url = request.url.replace("/uploadArt/", "")
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





app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jealocker@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'jealocker@gmail.com'
app.config['MAIL_PASSWORD'] = 'lockeryolo1'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


####################################################### SENDING EMAIL BASICS
@app.route("/")
def index():
   #confirm_account();
   get_activation_link()
   return "Sent"


#@async - important but im confused
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

##################################################### ACCOUNT CONFIRMATION; USER ACTIVATION URL STUFF
def confirm_account(payload):
    send_email("Confirm your account with PicFic",
               "jealocker@gmail.com",
               ["altermuse3@gmail.com"],
               render_template("testText.txt", payload=payload),
               render_template("testHtml.html", payload = payload))

def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeSerializer(secret_key)

@app.route('/users/activate/<payload>')
def activate_user(payload):
    s = get_serializer()
    try:
        user_id = s.loads(payload)
    except BadSignature:
        abort(404)

    user = User.query.get_or_404(user_id)
    user.activate()
    flash('User activated')
    return redirect(url_for('index'))

def get_activation_link(user): #user
    s = get_serializer()
    payload = s.dumps(user.id) # payload = s.dumps(user.id)
    return url_for('confirm_account', payload=payload, _external=True)


    
if __name__ == '__main__':
   app.run(debug = True)




