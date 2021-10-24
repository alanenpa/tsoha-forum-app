from db import db

def create_topic(topic):
    sql = "INSERT INTO topics (topic) VALUES (:topic)"
    db.session.execute(sql, {"topic": topic})
    db.session.commit()

def get_all():
    result = db.session.execute("SELECT * FROM topics")
    return result.fetchall()

def exists(topic_id):
    sql = "SELECT * FROM topics WHERE id=:id"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()
