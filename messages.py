from db import db
import users
import topics
import threads

def count_by_topic(topic_id):
    sql = "SELECT COUNT(*) FROM messages WHERE topic_id=:id AND visible=TRUE"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()[0]

def get_all_messagecounts_by_topic():
    topiclist = topics.get_all()
    dict = {}
    for topic in topiclist:
        dict[topic.topic] = count_by_topic(topic.id) + threads.count_by_topic(topic.id)
    return dict

def count_by_thread(thread_id):
    sql = "SELECT COUNT(*) FROM messages WHERE thread_id=:id AND visible=TRUE"
    result = db.session.execute(sql, {"id": thread_id})
    return result.fetchone()[0]

def get_all_messagecounts_by_thread(topic_id):
    threadlist = threads.get_all_by_topic(topic_id)
    list = []
    for thread in threadlist:
        list.append(count_by_thread(thread.id))
    return list

def get_all_by_thread_with_usernames(thread_id):
    sql = "SELECT M.id, M.content, M.sent_at, U.id AS user_id, U.username FROM messages M, users U " \
          "WHERE thread_id=:id AND M.visible=TRUE AND M.user_id=U.id ORDER BY sent_at"
    result = db.session.execute(sql, {"id": thread_id})
    return result.fetchall()

def get_latest_message_by_topic(topic_id):
    sql = "SELECT * FROM messages M, users U WHERE M.topic_id=:id AND M.visible=TRUE AND M.user_id=U.id ORDER BY M.sent_at DESC"
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()

def get_all_latest_messages_by_topic():
    topiclist = topics.get_all()
    dict = {}
    for topic in topiclist:
        dict[topic.topic] = get_latest_message_by_topic(topic.id)
    return dict

def search_by_keyword(keyword):
    sql = "SELECT * FROM messages M, users U WHERE M.content LIKE :keyword AND M.visible=TRUE AND M.user_id=U.id"
    result = db.session.execute(sql, {"keyword": "%" + keyword + "%"})
    return result.fetchall()

def post_message(topic_id, thread_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (topic_id, thread_id, user_id, content, sent_at, visible)" \
          "VALUES (:topic_id, :thread_id, :user_id, :content, NOW(), TRUE)"
    db.session.execute(sql, {
        "topic_id": topic_id,
        "thread_id": thread_id,
        "user_id": user_id,
        "content": content,
    })
    db.session.commit()
    return True

def delete_message(message_id):
    sql = "UPDATE messages SET visible=FALSE WHERE id=:id"
    db.session.execute(sql, {"id": message_id})
    db.session.commit()
