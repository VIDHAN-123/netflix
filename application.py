from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "abcdef"

currentques=0



def authenticateUser(username, password):

    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()

    cur.execute("SELECT password FROM user WHERE username=?", (username,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    print('Password obtained from DB is', result)

    return False if result is None or result[0] != password else True

def addToDatabase(fname, lname, email, username, password):

    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO user(fname, lname, email, username, password) VALUES(?, ?, ?, ?, ?)",
     (fname, lname, email, username, password))

    conn.commit()

    cur.close()
    conn.close()

    print('User added to DB', (fname, lname, email, username, password))

def updatePassword(username, newpassword):

    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()

    checkUsername = "SELECT * FROM user WHERE username=?"

    cur.execute(checkUsername, (username,))

    if not cur.fetchone() is None:
        passwordUpdate = "UPDATE user SET password=? WHERE username=?"
        cur.execute(passwordUpdate, (newpassword, username))
        conn.commit()
        return True
    return False

@app.route('/', methods=["GET", "POST"])
def homepage():
    ''' Homepage of the website '''

    return render_template("netflixloginpage.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    ''' Login page for users '''
    if "user" in session:
        return redirect("/shop")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if authenticateUser(username, password):
            session["user"] = username
            return redirect("/shop")
        else:
        	return render_template("login.html")
    else:
    	return render_template("login.html")

@app.route('/login2', methods=["GET", "POST"])
def login2():
    ''' Login page for users '''
    if "user" in session:
        return redirect("/shop")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if authenticateUser(username, password):
            session["user"] = username
            return redirect("/shop")
        else:
        	return render_template("login2.html")
    else:
    	return render_template("login2.html")

@app.route('/register', methods=["GET", "POST"])
def createAccount():
    """ Register an account """

    if request.method == "GET":
        return render_template("register.html")

    else:

        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        addToDatabase(fname, lname, email, username, password)

        return redirect("/login")

@app.route('/register2', methods=["GET", "POST"])
def createAccount2():
    """ Register an account """

    if request.method == "GET":
        return render_template("register.html")

    else:

        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        addToDatabase(fname, lname, email, username, password)

        return redirect("/login2")

@app.route('/shop', methods=["GET", "POST"])
def videopage():
    ''' Homepage of the website '''

    return render_template("shop.html")

@app.route('/cycle', methods=["GET", "POST"])
def cyclepage():
    ''' Homepage of the website '''

    return render_template("cycle.html")

@app.route('/toy', methods=["GET", "POST"])
def toypage():
    ''' Homepage of the website '''

    return render_template("toy.html")

@app.route('/electric', methods=["GET", "POST"])
def electricpage():
    ''' Homepage of the website '''

    return render_template("electric.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    """ User logout """

    session.pop("user", None)
    return redirect("/")

@app.route('/reset', methods=["GET", "POST"])
def forgotPassword():
    ''' Reset user password '''

    if request.method == "GET":
        return render_template("forgot_password.html")
    else:
        username = request.form["username"]
        newpassword = request.form["password"]

        if updatePassword(username, newpassword):
            return redirect("/login")
        else:
            return redirect("/reset")



if __name__ == "__main__":
	app.run(debug=True,port=80)
