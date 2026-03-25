import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_tables():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS content(id INTEGER PRIMARY KEY, user_id INT, tool TEXT, input TEXT, output TEXT)")

    conn.commit()
    conn.close()

def register_user(u,p):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username,password) VALUES(?,?)",(u,hash_password(p)))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(u,p):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",(u,hash_password(p)))
    user = c.fetchone()
    conn.close()
    return user

def save_content(uid,tool,i,o):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("INSERT INTO content(user_id,tool,input,output) VALUES(?,?,?,?)",(uid,tool,i,o))
    conn.commit()
    conn.close()

def get_user_content(uid):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT tool,input,output FROM content WHERE user_id=?",(uid,))
    data = c.fetchall()
    conn.close()
    return data