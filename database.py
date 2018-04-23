import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

class Database():

    #def add_question(self):

    def add_student(self,firstname, surname, email, password):

        conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
        cursor = conn.cursor()

        role = "user"

        cursor.execute("""INSERT INTO users(id, firstname, surname, email, password,role) VALUES (NULL,?,?,?,?,?)""",
                       (firstname, surname, email, password, role,))

        conn.commit()

        conn.close()

    def add_teacher(self,firstname, surname, email, password):

        conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
        cursor = conn.cursor()

        role = "admin"

        cursor.execute("""INSERT INTO users(id, firstname, surname, email, password, role) VALUES (NULL,?,?,?,?,?)""",
                       (firstname, surname, email, password,role,))

        conn.commit()

        conn.close()


    def check_for_student(self,email):

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute("""SELECT * from users WHERE email = ?""",(email,))

        data = cursor.fetchone()

        conn.close()

        if data == None:
            return False
        else:
            return True



    def login(self, email, password_candidate):

        conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""SELECT * from users WHERE email = ?""",(email,))
        data = cursor.fetchone()

        conn.close()

        if data != None:

            password = data[4]

            if sha256_crypt.verify(password_candidate, password):
                flash("You are now logged in.")
                session["logged_in"] = True
                session["ID"] = self.get_id(email)
                redirect(url_for("home"))
            else:
                flash("Invalid login")
                return render_template("login.html")

        else:
            flash("Email not found")
            return render_template("login.html")

    def get_id(self,email):

        conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""SELECT id from users WHERE email = ?""", (email,))
        id = cursor.fetchone()[0]

        conn.close()

        return id


    def get_name(self,id):
        conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""SELECT * from users WHERE id = ?""", (id,))

        firstname = cursor.fetchone()[1]

        conn.close()

        return firstname


    def get_current_user_role(self,id):

        conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""SELECT role from users WHERE id = ?""", (id,))

        role = cursor.fetchone()[0]


        conn.close()

        return role
