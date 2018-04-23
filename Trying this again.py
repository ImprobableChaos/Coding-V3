#############################
#My A-level Computing Project
#############################


#Importing the extensions for the project
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, Response
from data import teacherPosts, quizzes
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3
from functools import wraps

#Importing the other .py files
from database import *
from data import *

app =  Flask(__name__) #creating instance of flask class

#Config sqlite
#conn = sqlite3.connect("projectdatabase.db",check_same_thread=False)
#cursor = conn.cursor()

#cursor.execute("DROP TABLE IF EXISTS users")
#cursor.execute("""CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,firstname text,surname text,email text, password text,role text) """)
#conn.commit()
#conn.close()



Teacherposts = teacherPosts()
q = quizzes()
d = Database()

@app.context_processor
def inject_database():
    return {"d":d}

@app.before_request
def connect_database():
    g.db = sqlite3.connect("projectdatabase.db",check_same_thread=False)

@app.teardown_appcontext
def close_database():
    try:
        g.db.close()
    except Exception:
        pass

def check_for_topic(topic):
    connect_database()
    cursor = g.db.cursor()
    cursor.execute("""SELECT * from questions WHERE topic = ?""", (topic,))
    result = cursor.fetchone()

    conn.close()
    #if result

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args,**kwargs):
            id = session["ID"]
            if d.get_current_user_role(id) not in roles:
                return flash("You are not logged in")
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@app.route("/")
def home():
    return render_template("home.html")

#class QuestionsForms(Form):
    #Question = StringField("Question", [validators.Length(min=1)])
    #Answer = StringField("Answer", [validators.Length(min=1)])
    #Topic = StringField("Topic", [validators.Length(min=1)])
    #Choices = StringField("Multiple Choice Answers, Enclose with [] and separate the choices with commas (a,b)")

@app.route("/makequiz")#,methods="GET","POST")
@requires_roles("admin")
def makequestions():
    #form = RegisterForm(request.form)
    #if request.method == "POST" and form.validate():
        #question = form.Question.data
        #answer = form.Answer.data
        #topic = form.Topic.data

        #if check_for_topic(topic) == False:
            # execute query
            #d.add_question(question, answer, topic)
            #flash("Question has been successfully added")
            #redirect(url_for("home"))
        #else:
            #flash("That is not a valid Topic")
            #return render_template("makequestions.html", form=form)

        #return redirect(url_for("home"))
    return render_template("makequestions.html")

#List of posts
@app.route("/teacherposts")
def teacherposts():
    return render_template("teacherposts.html", teacherposts = Teacherposts)

#Single posts
@app.route("/teacherpost/<string:id>/")
def teacherpost(id,title,author,create_date,body):
    return render_template("teacherpost.html",id=id,title=title,author=author,create_date=create_date,body=body)

@app.route("/Quizzes")
def quizzes():
    return render_template("quizzes.html", quizzes = q)

@app.route("/Quizzes/<string:quizid>/")
def quiz(quizid):
    return render_template("Quiz.html", quizid = quizid)

#Register Class
class RegisterForm(Form):
    firstname = StringField("First name", [validators.Length(min=1, max=16)])
    surname = StringField("Surname", [validators.Length(min=1, max=30)])
    email = StringField("Email", [validators.Email(message="That is not a valid email address")])
    password=PasswordField("Password",[
        validators.DataRequired(),
        validators.EqualTo("confirm",message="Passwords do not match")
    ])
    confirm = PasswordField("Confirm Password")

#User registration
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        firstname = form.firstname.data
        surname = form.surname.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data)) #encrypting the password for security

        if d.check_for_student(email)== False:
            #execute query
            d.add_teacher(firstname, surname, email, password)
            flash("You are now Registered and can log in", "success")
        else:
            flash("There is already a user registered under the same email")
            return render_template("register.html", form=form)

        return redirect(url_for("home"))
    return render_template("register.html", form=form)

#User log in

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #Get form fields
        email = request.form["email"]
        password_candidate = request.form["password"]
        d.login(email, password_candidate)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["logged_in"] = False
    flash("You are now logged out")
    return render_template("home.html")

@app.route("/dashboard")
@requires_roles("admin","user")
def dashboard():
    id = session["ID"]
    return render_template("dashboard.html",name=d.get_name(id))


if __name__ == "__main__": #means that it is the script that is going to be executed
    app.secret_key="itsasecret"
    app.run(debug = True) #running the application
    # debug = True so i dont have to keep restarting the server to update the webpage
