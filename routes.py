from app import app
from flask import redirect, render_template, request
import users
import topics
import threads
import messages

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"]
        topics.create_topic(topic)
    adminrights = users.is_admin()
    topiclist = topics.get_all()
    threadlist = {}
    messagelist = {}
    latestmessages = {}
    for topic in topiclist:
        threadcount = threads.count_by_topic(topic.id)
        msgcount = messages.count_by_topic(topic.id)
        threadlist[topic.topic] = threadcount
        messagelist[topic.topic] = msgcount + threadcount
        latestmessages[topic.topic] = messages.get_latest_message_by_topic(topic.id)
    return render_template(
        "index.html",
        topics=topiclist,
        threads=threadlist,
        messages=messagelist,
        latestmessages=latestmessages,
        adminrights=adminrights
    )

@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        header = request.form["header"]
        init_msg = request.form["init_msg"]
        if not threads.create_thread(id, header, init_msg):
            return render_template("error.html", message="Ketjun luonti epäonnistui")
    threadlist_with_usernames = threads.get_all_by_topic_with_usernames(id)
    threadlist = threads.get_all_by_topic(id)
    msgcount = {}
    counter = 0
    for thread in threadlist:
        msgcount[counter] = messages.count_by_thread(thread.id)
        counter += 1
        # Refaktoroi?
    return render_template("topicview.html", topic_id=id, threads=threadlist_with_usernames, thread_ids=threadlist, msgcount=msgcount)

@app.route("/topic/<int:topic_id>/thread/<int:thread_id>", methods=["GET", "POST"])
def thread(topic_id, thread_id):
    if request.method == "POST":
        content = request.form["content"]
        if not messages.post_message(topic_id, thread_id, content):
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
        password = request.form["password"]
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