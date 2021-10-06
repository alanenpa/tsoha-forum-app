from flask import Flask
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

import os

app = Flask(__name__)
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")

db = SQLAlchemy(app)


@app.route("/", methods=["GET", "POST"])
def index():
    # result = db.session.execute("SELECT text FROM test")
    # print("hello")
    # print(result.fetchall())
    # print("goodbye")
    if request.method == "POST":
        topic = request.form["topic"]
        sql = "INSERT INTO topics (topic) VALUES (:topic)"
        db.session.execute(sql, {"topic": topic})
        db.session.commit()
    result = db.session.execute("SELECT * FROM topics")
    topics = result.fetchall()
    threads = {}
    for topic in topics:
        sql = "SELECT COUNT(*) FROM threads WHERE topic_id=:id"
        result = db.session.execute(sql, {"id": topic.id})
        count = result.fetchone()[0]
        threads[topic.topic] = count
    return render_template("index.html", topics=topics, threads=threads)

@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        header = request.form["header"]
        init_msg = request.form["init_msg"]
        print("")
        print(session)
        print(session["user_id"])
        print("")
        sql = "INSERT INTO threads (topic_id, user_id, header, init_msg, created_at) " \
              "VALUES (:topic_id, :user_id, :header, :init_msg, NOW())"
        db.session.execute(sql, {
            "topic_id": id,
            "user_id": session["user_id"],
            "header": header,
            "init_msg": init_msg,
        })
        db.session.commit()
    sql = "SELECT * FROM threads T, users U WHERE topic_id=:id AND T.user_id=U.id"
    result = db.session.execute(sql, {"id": id})
    threads = result.fetchall()
    sql = "SELECT COUNT(*) FROM messages WHERE thread_id=:id"
    result = db.session.execute(sql, {"id": 1})
    msgcount = result.fetchone()[0]
    print("")
    for thread in threads:
        print(thread)
        print("")
    # print(threads)
    print("")
    return render_template("topicview.html", topic_id=id, threads=threads, msgcount=msgcount)

@app.route("/thread/<int:id>")
def thread(id):
    sql = "SELECT * FROM messages M, users U WHERE thread_id=:id AND M.user_id=U.id"
    result = db.session.execute(sql, {"id": id})
    messages = result.fetchall()
    sql = "SELECT * FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    thread = result.fetchone()
    user_id = thread.user_id
    sql = "SELECT * FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": user_id})
    op = result.fetchone()
    print(thread)
    return render_template("threadview.html", messages=messages, thread=thread, op=op)


@app.route("/signup", methods=["GET", "POST"])
def signup():
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
            db.session.execute(
                sql, {"username": username, "password": passwordHash})
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
        print("")
        print(user)
        print("user.id", user.id)
        print("")
        if not user:
            print('missing user')
            return render_template("signin.html")
        else:
            passwordHash = user.password
            # print('here')
            # print('hash:', passwordHash)
            # print('password:', password)
            # print(check_password_hash(passwordHash, password))
            if check_password_hash(passwordHash, password):
                print('password correct')
                session["username"] = username
                session["user_id"] = user.id
                print("")
                print(session)
                print("")
                return redirect("/")
            else:
                print('wrong password')
                return render_template("signin.html", username=username)


@app.route("/signout")
def signout():
    del session["username"]
    return redirect("/")