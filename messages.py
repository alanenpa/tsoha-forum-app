from db import db
import users
import topics
import threads

def count_by_topic(topic_id):
    sql = "SELECT COUNT(*) FROM messages WHERE topic_id=:id"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()[0]

def get_all_messagecounts_by_topic():
    topiclist = topics.get_all()
    dict = {}
    for topic in topiclist:
        dict[topic.topic] = count_by_topic(topic.id) + threads.count_by_topic(topic.id)
    return dict

def count_by_thread(thread_id):
    sql = "SELECT COUNT(*) FROM messages WHERE thread_id=:id"
    result = db.session.execute(sql, {"id": thread_id})
    return result.fetchone()[0]

def get_all_by_thread_with_usernames(thread_id):
    sql = "SELECT * FROM messages M, users U WHERE thread_id=:id AND M.user_id=U.id ORDER BY sent_at"
    result = db.session.execute(sql, {"id": thread_id})
    return result.fetchall()

def get_latest_message_by_topic(topic_id):
    sql = "SELECT * FROM messages M, users U WHERE M.topic_id=:id AND M.user_id=U.id ORDER BY M.sent_at DESC"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()

def get_all_latest_messages_by_topic():
    topiclist = topics.get_all()
    dict = {}
    for topic in topiclist:
        dict[topic.topic] = get_latest_message_by_topic(topic.id)
    return dict

def post_message(topic_id, thread_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (topic_id, thread_id, user_id, content, sent_at) VALUES (:topic_id, :thread_id, :user_id, :content, NOW())"
    db.session.execute(sql, {
        "topic_id": topic_id,
        "thread_id": thread_id,
        "user_id": user_id,
        "content": content,
    })
    db.session.commit()
    return True