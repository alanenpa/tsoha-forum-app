from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def get_by_id(user_id):
    sql = "SELECT * FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": user_id})
    return result.fetchone()

def sign_in(username, password):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def sign_up(username, password, admin):
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)"
        db.session.execute(sql, {"username": username, "password": password_hash, "admin": admin})
        db.session.commit()
    except:
        return False
    return sign_in(username, password)

def user_id():
    return session.get("user_id", 0)

def is_admin():
    id = user_id()
    if id == 0:
        return False
    sql = "SELECT admin FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()[0]

def sign_out():
    del session["user_id"]
