import sqlite3
from logger_server import app


def connect_db():
    print("DATABASE URI IN database.py %s" % app.config['DATABASE_URI'])
    conn = sqlite3.connect(app.config['DATABASE_URI'])
    return conn, conn.cursor()


def setup_db():
    conn, c = connect_db()
    c.execute("""
            CREATE TABLE IF NOT EXISTS messages
            (message TEXT,
            message_type TEXT,
            time REAL,
            email TEXT)
            """)

    c.execute("""
            CREATE TABLE IF NOT EXISTS users
            (id TEXT,
            username TEXT,
            password_hash TEXT,
            created_at REAL,
            PRIMARY KEY (id))
            """)

    conn.commit()


def clear_db(messages=True, users=False):
    conn, c = connect_db()

    if messages:
        c.execute("""
                   DELETE FROM messages
                   """)
    if users:
        c.execute("""
                   DELETE FROM users
                   """)
    conn.commit()
