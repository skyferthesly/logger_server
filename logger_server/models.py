import sqlite3
import time
import hashlib
from uuid import uuid4
from logger_server.setup import login_manager


def insert_message(message, message_type='INFO'):
    conn = sqlite3.connect("logger.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO messages
        VALUES (?, ?, ?)
        """, (message, message_type, time.time()))
    conn.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class User(object):
    def __init__(self, username, password_hash, id=None):
        self.username = username
        self.password_hash = password_hash
        self.id = id or str(uuid4())

    @classmethod
    def get(cls, user_id):
        conn = sqlite3.connect("logger.db")
        c = conn.cursor()
        res = c.execute("""
                    SELECT * FROM users
                    WHERE users.id = ?
                    """, user_id).fetchone()
        return cls(res[1], res[2], res[0])

    def save(self):
        conn = sqlite3.connect("logger.db")
        c = conn.cursor()
        c.execute("""
                INSERT INTO users
                VALUES (?, ?, ?, ?)
                """, (self.id, self.username, self.password_hash, time.time()))
        conn.commit()

    def validate(self, password):
        return self.password_hash == hashlib.sha3_512(password)

    def is_authenticated(self):
        pass

    def is_active(self):
        pass

    def is_anonymous(self):
        return False

    def get_id(self):
        pass

    def to_dict(self):
        pass
