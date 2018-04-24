import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

class Database():

    def add_question(self,question, answer, topic):

        conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO questions(qid, question, answer, topic) VALUES (NULL,?,?,?)""",(question, answer, topic,))

        conn.commit()

        conn.close()

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

        conn = sqlite3.connect("projectdatabase.db",check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""SELECT * from users WHERE email = ?""",(email,))

        data = cursor.fetchone()

        conn.close()

        if data is None:
            return False
        else:
            return True



    def get_login(self, email, password_candidate):

        conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""SELECT * from users WHERE email = ?""",(email,))
        data = cursor.fetchone()

        conn.close()

        return data

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

    def check_for_topic(self,topic):

        conn = sqlite3.connect("projectdatabase.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""SELECT * from questions WHERE topic = ?""", (topic,))
        result = cursor.fetchone()

        conn.close()

        if result is not None:
            return True
        else:
            return False
