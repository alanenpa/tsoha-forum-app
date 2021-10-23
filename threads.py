from db import db
import users
import topics

def count_by_topic(topic_id):
    sql = "SELECT COUNT(*) FROM threads WHERE topic_id=:id AND visible=TRUE"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()[0]

def get_all_threadcounts_by_topic():
    topiclist = topics.get_all()
    dict = {}
    for topic in topiclist:
        dict[topic.topic] = count_by_topic(topic.id)
    return dict

def create_thread(topic_id, header, init_msg):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (topic_id, user_id, header, init_msg, created_at, visible) " \
          "VALUES (:topic_id, :user_id, :header, :init_msg, NOW(), TRUE)"
    db.session.execute(sql, {
        "topic_id": topic_id,
        "user_id": user_id,
        "header": header,
        "init_msg": init_msg,
    })
    db.session.commit()
    return True

def get_all_by_topic(topic_id):
    sql = "SELECT T.id, T.header, T.init_msg, T.created_at, U.id AS user_id, U.username " \
          "FROM threads T, users U WHERE topic_id=:id AND T.visible=TRUE AND T.user_id=U.id ORDER BY T.created_at"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchall()

def search_by_keyword(keyword):
    sql = "SELECT T.id, T.topic_id, T.init_msg, T.created_at, U.username " \
          "FROM threads T, users U WHERE T.init_msg LIKE :keyword AND T.visible=TRUE AND T.user_id=U.id"
    result = db.session.execute(sql, {"keyword": "%" + keyword + "%"})
    return result.fetchall()

def get_by_id(thread_id):
    # toiminta visible-kolumnin kanssa ??
    sql = "SELECT * FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id": thread_id})
    return result.fetchone()

def delete_thread(thread_id):
    sql = "UPDATE threads SET visible=FALSE WHERE id=:id"
    db.session.execute(sql, {"id": thread_id})
    db.session.commit()

def is_visible(thread_id):
    sql = "SELECT visible FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id": thread_id})
    return result.fetchone()[0]
