from flask import redirect, render_template, request
from app import app
import users
import topics
import threads
import messages

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"]
        if len(topic) < 3 or len(topic) > 50:
            return render_template("error.html", message="Aiheen täytyy olla 3-50 merkkiä")
        topics.create_topic(topic)
    adminrights = users.is_admin()
    topiclist = topics.get_all()
    threadcounts = threads.get_all_threadcounts_by_topic()
    messagecounts = messages.get_all_messagecounts_by_topic()
    latestmessages = messages.get_all_latest_messages_by_topic()
    return render_template(
        "index.html",
        topics=topiclist,
        threadcounts=threadcounts,
        messagecounts=messagecounts,
        latestmessages=latestmessages,
        adminrights=adminrights
    )

@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        header = request.form["header"]
        if len(header) < 3 or len(header) > 300:
            return render_template("error.html", message="Otsikon täytyy olla 3-300 merkkiä")
        init_msg = request.form["init_msg"]
        if len(init_msg) > 5000:
            return render_template("error.html", message="Aloitusviesti on liian pitkä (>5000 merkkiä)")
        if not threads.create_thread(id, header, init_msg):
            return render_template("error.html", message="Ketjun luonti epäonnistui")
    threadlist = threads.get_all_by_topic(id)
    msgcount = messages.get_all_messagecounts_by_thread(id)
    return render_template(
        "topicview.html",
        topic_id=id,
        threads=threadlist,
        msgcount=msgcount
    )

@app.route("/topic/<int:topic_id>/thread/<int:thread_id>", methods=["GET", "POST"])
def thread(topic_id, thread_id):
    if request.method == "POST":
        content = request.form["content"]
        if len(content) < 1 or len(content) > 5000:
            return render_template("error.html", message="Viestin täytyy olla 1-5000 merkkiä")
        elif not messages.post_message(topic_id, thread_id, content):
            return render_template("error.html", message="Viestin lähetys epäonnistui")
    messagelist = messages.get_all_by_thread_with_usernames(thread_id)
    thread = threads.get_by_id(thread_id)
    op = users.get_by_id(thread.user_id)
    return render_template("threadview.html", topic_id=topic_id, messages=messagelist, thread=thread, op=op)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", message="Käyttäjätunnuksen täytyy olla 3-20 merkkiä")
        password = request.form["password"]
        if len(username) < 10 or len(username) > 40:
            return render_template("error.html", message="Salasanan täytyy olla 10-40 merkkiä")
        password2 = request.form["password2"]
        admin = request.form["admin"]
        if password != password2:
            return render_template("error.html", message="Salasanat eivät ole samat")
        if users.sign_up(username, password, admin):
            return render_template("newuser.html", username=username)
        else:
            return render_template("error.html", message="Käyttäjätunnuksen luonti epäonnistui")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.sign_in(username, password)
        if user:
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")

@app.route("/signout")
def signout():
    users.sign_out()
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    if request.method == "POST":
        keyword = request.form["keyword"]
        if len(keyword) < 1:
            return render_template("error.html", message="Anna hakusana")
        messagelist = messages.search_by_keyword(keyword)
        init_messagelist = threads.search_by_keyword(keyword)
        return render_template("search.html", messages=messagelist, init_messages=init_messagelist)