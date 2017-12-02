import sqlite3


def setup_db():
    conn = sqlite3.connect("logger.db")
    c = conn.cursor()
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


def clear_db():
    conn = sqlite3.connect("logger.db")
    c = conn.cursor()
    c.execute("""
               DELETE FROM messages
               """)
    c.execute("""
               DELETE FROM users
               """)
    conn.commit()
