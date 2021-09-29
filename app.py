from flask import Flask
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

import os
import re

app = Flask(__name__)
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
print('here')
print('URI 1:', uri)
print('URI 2:', getenv("DATABASE_URL"))
app.config["SQLALCHEMY_DATABASE_URI"] = uri
# app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")

db = SQLAlchemy(app)


@app.route("/")
def index():
    # result = db.session.execute("SELECT text FROM test")
    # print("hello")
    # print(result.fetchall())
    # print("goodbye")
    result = db.session.execute("SELECT * FROM users")
    print(result.fetchall())
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def result():
    if request.method == "GET":
        result = db.session.execute("SELECT * FROM users")
        print(result.fetchall())
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("signup.html", username=username)
        else:
            passwordHash = generate_password_hash(password)
            sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, false)"
            db.session.execute(sql, {"username": username, "password": passwordHash})
            db.session.commit()
            return render_template("newuser.html", username=username, password=password, passwordHash=passwordHash)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT * FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()
        print(user)
        if not user:
            print('missing user')
            return render_template("signin.html")
        else:
            passwordHash = user.password
            print('here')
            print('hash:', passwordHash)
            print('password:', password)
            print(check_password_hash(passwordHash, password))
            if check_password_hash(passwordHash, password):
                print('password correct')
                session["username"] = username
                return redirect("/")
            else:
                print('wrong password')
                return render_template("signin.html", username=username)


@app.route("/signout")
def signout():
    del session["username"]
    return redirect("/")
