import sqlite3
from flask_login import LoginManager, login_user
from logger_server.controllers import app

login_manager = LoginManager()
login_manager.init_app(app)


def setup_db():
    conn = sqlite3.connect("logger.db")
    c = conn.cursor()
    c.execute("""
            CREATE TABLE messages
            (message TEXT,
            message_type TEXT,
            time REAL)
            """)

    c.execute("""
            CREATE TABLE users
            (id TEXT,
            username TEXT,
            password_hash TEXT,
            created_at REAL,
            PRIMARY KEY (id))
            """)

    conn.commit()
