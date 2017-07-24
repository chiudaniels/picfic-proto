from flask import Flask, render_template, request, session, url_for, redirect, send_from_directory
from utils import users, books, gallery
from werkzeug.utils import secure_filename
import json, os


app = Flask(__name__)
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

@app.route("/books/<bookID>")
def bookLanding(bookID):
    metadata = books.getBookMetadata(bookID)
    return render_template("bookLandingTemp.html", isLoggedIn = isLoggedIn(), data = metadata)


# == reading =====


@app.route("/books/<bookID>/read")
def bookRedir(bookID):
    return redirect("/books/" + str(bookID) + "/read/1/1")

@app.route("/books/<bookID>/read/<chNum>/<pgNum>")
def bookPage(bookID, chNum, pgNum):
    data = books.getPageData(bookID, chNum, pgNum)
    if data == None or len(data) == 0:
        print "Something went wrong"
    else:
        return render_template("chapter_template.html", isLoggedIn = isLoggedIn(), pageData = data , message = "You are reading")

    
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
    pwd2 = request.form["password2"]
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



# Photo Upload ==================================================================

#UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), "images/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image/upload/', methods=['POST'])
def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return None

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
