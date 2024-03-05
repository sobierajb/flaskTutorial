from flaskr.db import get_db

def get_all():
    db = get_db()
    posts = db.execute('SELECT p.Id, title, body, created, updated, author_id, username '
                       'FROM post p '
                       'JOIN user u ON p.author_id=u.id ' 
                       'ORDER BY p.created DESC '
                       ).fetchall()
    return posts

def get_by_id(id):
    db = get_db()
    post = db.execute('SELECT p.Id, title,body,created,updated,author_id,username '
                      'FROM post p '
                      'JOIN user u ON p.author_id = u.id '
                      'WHERE p.id = ? ',
                      (id,)
                      ).fetchone()
    return post

def create(title,body,author_id):
    db = get_db()
    c =  db.cursor()
    db.execute('INSERT INTO post (title,body,author_id) '
               'VALUES (?,?,?)',
               (title,body,author_id)
               )
    db.commit()
    return c.lastrowid
    
def update(id, title,body): 
    db = get_db()
    c = db.cursor()
    db.execute('UPDATE post SET title=?, body = ?, updated = CURRENT_TIMESTAMP '
               'WHERE id=?',
               (title,body,id)
               )
    db.commit()
    return c.lastrowid

def delete(id):
    db = get_db()
    db.execute('DELETE FROM post WHERE id=?',(id,))
    db.commit()
