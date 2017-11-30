import sqlite3
import time


def setup_db():
    conn = sqlite3.connect("logger.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE messages
    (message TEXT, message_type TEXT, time REAL)
    """)
    conn.commit()


def insert_message(message, message_type='INFO'):
    conn = sqlite3.connect("logger.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO messages
        VALUES (?, ?, ?)
        """, (message, message_type, time.time()))
    conn.commit()
