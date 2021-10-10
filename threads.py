from db import db
import users

def count_by_topic(topic_id):
    sql = "SELECT COUNT(*) FROM threads WHERE topic_id=:id"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()[0]

def create_thread(topic_id, header, init_msg):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (topic_id, user_id, header, init_msg, created_at) " \
            "VALUES (:topic_id, :user_id, :header, :init_msg, NOW())"
    db.session.execute(sql, {
        "topic_id": topic_id,
        "user_id": user_id,
        "header": header,
        "init_msg": init_msg,
    })
    db.session.commit()
    return True

def get_all_by_topic(topic_id):
    sql = "SELECT * FROM threads WHERE topic_id=:id ORDER BY id"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchall()

def get_all_by_topic_with_usernames(topic_id):
    sql = "SELECT * FROM threads T, users U WHERE topic_id=:id AND T.user_id=U.id ORDER BY T.id"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchall()

def get_by_id(thread_id):
    sql = "SELECT * FROM threads T, users U WHERE T.id=:id AND T.user_id=U.id"
    result = db.session.execute(sql, {"id": thread_id})
    return result.fetchone()