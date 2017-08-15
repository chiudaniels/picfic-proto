from flask import Flask, render_template, request, session, url_for, redirect, send_from_directory, abort, flash
from flask_mail import Mail, Message
from threading import Thread
from itsdangerous import URLSafeSerializer, BadSignature
import flask
from utils import users, books, gallery, images, admin, uploadStory
from werkzeug.utils import secure_filename
import json, os
from bson import BSON
from bson import json_util
#from utils import decorators import async
from flask_bcrypt import Bcrypt
import cStringIO

app = Flask(__name__)
bcrypt = Bcrypt(app)
mail=Mail(app)
app.secret_key = "secrets"

UPLOAD_FOLDER = "static/data/"
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

@app.route("/", methods=['GET', 'POST'])
def root():
    print gallery.getGallery()
    print isLoggedIn()
    return render_template("launchpad.html", isLoggedIn = isLoggedIn(), data ={"books": gallery.getGallery()} )

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
    #"myShelf", "myStories", "likedArt", "uploadedArt"
    profileData.update( users.getActivity(username) )
    #get visibility options - add in later
    userVis = 0
    if isLoggedIn() and username == users.getUsername( getUserID() ):
        userVis = 1
        profileData.update( users.getProfileSensitive( username ) )
    return render_template( "profile.html", isLoggedIn = isLoggedIn(), data = profileData, perm = userVis )


@app.route("/saveProfile/", methods = ['POST'])
def saveProfile():
    #try to eventually sanitize this
    users.saveProfile(request.form.to_dict(), getUserID())
    return json.dumps({"status":1})

@app.route("/saveProfilePic/", methods = ['POST'])
def saveProfilePic():
    print "saving profile pic"
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        print "shocking"
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "profilePics/", filename))
        users.saveProfilePic(getUserID(), filename)
        return json.dumps({"status": 1})
    return None


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
    return render_template("bookLanding.html", isLoggedIn = isLoggedIn(), data = metadata, showMenu = 0)

@app.route("/getBookLandingImages/", methods=['POST'])
def bookLandingImages(): #lazy jump
    metadata = books.getBookLanding(int(request.form["bookID"]))
    print "no screw you"
    return json.dumps(metadata["imageData"])


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
    data.update(books.getTableOfContents(bookID, getUserID()))
    return render_template("chapter_template.html", isLoggedIn = isLoggedIn(), pageData = data, showMenu = 1)

#todo : refuse permission if access not given
#todo: grant free access on chapters 

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
    if isLoggedIn():
        data =  users.bookmark(getUserID(), bID, chN, ccStart)
        return json.dumps({"status":1})
    return None

@app.route("/getEndOfChPage/", methods = ["POST"])
def endOfCh():
    bID = request.form.get("bookID")
    chN = request.form.get("chNum")
    data = {"endOfChCC" : books.getEndOfChCC(bID, chN),
            "chLength" : books.getChLength(bID, chN)
    }
    return json.dumps(data)

@app.route("/chapterGallery/", methods = ["POST"])
def chapterGallery():
    bID = request.form.get("bookID")
    chN = request.form.get("chNum")
    print books.getChapterSummary(bID, chN)
    return json.dumps(books.getChapterSummary(bID, chN))


#=================== END SITE NAVIGATION =======================

# Login Routes ======================================

@app.route("/login/", methods=["POST"])
def login():

    # request
    email = request.form["loginEmail"]
    pwd = request.form["loginPass"]
    #auth
    msg = ""
    if users.getHashed(email) and bcrypt.check_password_hash(users.getHashed(email), pwd) :
        session['uID'] = users.getUserID( email )
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
    hashedPwd = bcrypt.generate_password_hash(pwd)
    #reg
    if not users.isNameTaken(uN): #and email
        session['uID'] = users.addUser( fN, lN, uN, email, hashedPwd, bM, bD, bY, gender, "")
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
        if bcrypt.check_password_hash(users.getHashedFromID(getUserID()), old):
            users.setPass( getUserID(), bcrypt.generate_password_hash(new) )
    return redirect(url_for('settings'))

@app.route('/forgotPass/', methods = ['POST'])
def forgotPass():
    return redirect(url_for('root'))

@app.route('/changeTag/', methods = ['POST'])
def changeTag():
    if isLoggedIn():
        d = request.form
        newTag = d["tag"]
        users.changeTag( getUserID(), newTag )
    return redirect(url_for('settings'))

# Story Upload ==================================================================
@app.route('/uploadStory/')
# uploadStoryPage - renders landing page for uploading stories
def uploadStoryPage():
    print "Logged In Status:", isLoggedIn() # Debugging
    print "Active Status:", users.isActive(getUserID()) # Debugging
    if isLoggedIn() and users.isActive(getUserID()):
        data = uploadStory.getUploadStoryData(getUserID())
        return render_template('uploadStory.html', isLoggedIn = isLoggedIn(), data = data)
    return redirect('/')

# Create Later - Not Needed for MVP
@app.route('/uploadStoryFile/', methods = ['POST'])
def uploadStoryFile():
    return True

# uploadStoryText - backend for story upload
@app.route('/uploadStoryText/', methods = ['POST'])
def uploadStoryText():
    print "Story being uploaded..." # Debugging
    print "Debugging Fields:", request.form # Debugging
    print "Debugging Files:", request.files # Debugging
    print "Number of Keys:", len(request.form) # Debugging
    print "Number of Files:", len(request.files) # Debugging
    if request.method == 'POST':
        # NEW FRAMEWORK - STORY UPLOADED AS TEXT IN TEXTAREA
        # Retrieving Fields - Add Defaults Later
        title = request.form["title"]
        author = request.form["author"]
        blurb = request.form["blurb"]
        print title, author, "\n", blurb # Debugging
        
        # Verifying Data
        try:
            print request.files # Debugging
            cover = request.files['file'] # FileStorage object
            covertype = cover.mimetype # file type 
            if (covertype != "image/jpeg" and covertype != "image/png"):
                return "Invalid image file." # Redirect - TODO
            covername = secure_filename(str(getUserID()) + "_" + title + "_" + cover.filename) # filename
        except:
            return "No image selected." # Redirect - TODO
        print "Cover Filename:", covername # Debugging
        print "Cover Filetype:", covertype # Debugging

        # Saving Cover as File
        cover.save(os.path.join(app.config['UPLOAD_FOLDER'] + "bookCovers/",
                                covername))
        print "File Saved In:", os.path.join(app.config['UPLOAD_FOLDER'] + "bookCovers/", covername) # Debugging        

        # Creating Book
        bID = books.parseBookCustom2(title, author, blurb, getUserID(), covername)
        print "Book Created - Book ID:", bID # Debugging

        # Redirect - Change Later
        username = users.getUsername(getUserID())
        profileData = users.getProfile(username)
        profileData.update( users.getActivity(username) )
        return flask.Response(render_template('uploadingChapter.html', isLoggedIn = isLoggedIn(), data = profileData))

    '''
        # OLD FRAMEWORK - STORY UPLOADED AS .TXT FILE
        print "WOW! A story is being made!" # Debugging
        # files = request.files.getlist('file[]')
        print request.files
        file1 = request.files['file[0]']
        print "hello"
        file2 = request.files['file[1]']
        textFile = None
        coverFile = None
        if file1.filename.endswith('.txt'):
            textFile = file1
            coverFile = file2
        else:
            textFile = file2
            coverFile = file1
        coverFile = request.files['file[0]']
        textFile = request.files['file[1]']
        print "hello"
        if coverFile.filename == '' or textFile.filename == '':
            print "sucky file"
            return redirect(request.url)
        if coverFile and allowed_file(coverFile.filename):
            print "what's up"
            filename = secure_filename(coverFile.filename)
            print "g"
            coverFile.save(os.path.join(app.config['UPLOAD_FOLDER'] + "bookCovers/", filename))
            
            print "oh"
            #make the book first
            print request.form
            title = request.form["title"]
            author = request.form["author"]
            #text = request.form["storyText"]
            blurb = request.form["blurb"]
            #print "boi"
            #print text
            #books.parseBookForm(title, author, blurb, text, getUserID(), filename)
            books.parseBookCustom(textFile, title, author, blurb, getUserID(), filename)
            print "and it was mada mada!"
            return redirect(request.url) 
        return False # Failure - Missing Fields
        '''
    return False # Not POST 
    
@app.route('/uploadStoryCoverPic/', methods = ['POST'])
def uploadStoryCover():
    return True #see cover art

@app.route('/uploadChapter/', methods = ['GET'])
def uploadChapter():
    username = users.getUsername(getUserID())
    profileData = users.getProfile(username)
    profileData.update( users.getActivity(username) )
    return render_template('uploadingChapter.html', isLoggedIn = isLoggedIn(), data = profileData)

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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "images/", filename))
        images.uploadArt(filename, getUserID(), caption, cStart, cEnd, bID, chN)
        url = request.url.replace("/uploadArt/", "")
        return redirect(url)
    return None

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



# Admin ==================================================================
@app.route('/admin/')
def adminPage():
    if isLoggedIn():
        uID = getUserID()
        if users.isAdmin(uID):
            print admin.getAdminPageData()
            return render_template("admin.html", data = admin.getAdminPageData(), isLoggedIn = isLoggedIn())
    return redirect(url_for('page_not_found', e = None))

@app.route('/adminAction/', methods = ['POST'])
def adminAction():
    if isLoggedIn():
        uID = getUserID()
        if users.isAdmin(uID):
            return json.dumps(admin.adminAction(request.form))
    return redirect(url_for('page_not_found', e = None))


#Emailing and business below


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jealocker@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'jealocker@gmail.com'
app.config['MAIL_PASSWORD'] = 'lockeryolo1'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


####################################################### SENDING EMAIL BASICS
@app.route("/nogoof")
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
        uID = s.loads(payload)
    except BadSignature:
        abort(404)

    users.activate(uID)
    flash('User activated')
    return redirect(url_for('root'))

def get_activation_link(uID): #user
    s = get_serializer()
    payload = s.dumps(uID) # payload = s.dumps(user.id)
    return url_for('confirm_account', payload=payload, _external=True)
#why is this a url_for

# General Helpers =====================================
 
# Login Helpers
def isLoggedIn():
    if "uID" in session:
        return users.getUsergroup(session["uID"])
    else:
        return 0

def getUserID():
    if isLoggedIn():
        return session["uID"]
    else:
        return None

# Error Handling =======================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/debug/', methods=['POST'])
def debug():
    ret = "Request Data:<br>"
    formdata = request.values
    print formdata
    for kv in formdata:
        ret += str(kv) + ", " + str(formdata[kv]) + "<br>"
    return ret

# RUN APP - NO FUNCTIONS AFTER THIS POINT ============================================    
if __name__ == "__main__":
    app.debug = True
    app.run()
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    
print __name__
