from flaskr.db import get_db 
from werkzeug.security import generate_password_hash,check_password_hash


def get_by_name(username):
    db = get_db()
    user = db.execute(
        "SELECT * FROM user where username=?",(username,)
    ).fetchone()
    return user

def get_by_id(id):
    db = get_db()
    user = db.execute(
        "SELECT * FROM user where id=?",(id,)
    ).fetchone()
    return user
    

def create(username,password):
    db = get_db()
    c=db.cursor()
    try:      
        db.execute(
            "INSERT INTO user (username,password) VALUES (?,?)",(username, generate_password_hash(password) )
        ) 
        db.commit()
    except db.IntegrityError:
        return "User already exists"
    else: 
        return None

def authorize(user,password):
    if user is not None:
        return check_password_hash(user['password'],password)
    return False
