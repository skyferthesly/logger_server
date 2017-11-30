import sqlite3
import time
import hashlib
from uuid import uuid4


class Message(object):
    def __init__(self, message, message_type=None, _time=None):
        self.message = message
        self.message_type = message_type or 'INFO'
        self.time = _time or time.time()

    def save(self):
        conn = sqlite3.connect("logger.db")
        c = conn.cursor()
        c.execute("""
                INSERT INTO messages
                VALUES (?, ?, ?)
                """, (self.message, self.message_type, self.time))
        conn.commit()
        return self

    def to_dict(self):
        d = dict()
        d['message'] = self.message
        d['message_type'] = self.message_type
        d['time'] = self.time
        return d


class User(object):
    def __init__(self, username, password_hash, id=None, created_at=None):
        self.username = username
        self.password_hash = password_hash
        self.id = id or str(uuid4())
        self.created_at = created_at or time.time()
        self.authenticated = False

    @classmethod
    def get_by_username(cls, username):
        conn = sqlite3.connect("logger.db")
        c = conn.cursor()
        res = c.execute("""
                    SELECT * FROM users
                    WHERE username = ?
                    """, (username,)).fetchone()
        if res:
            return cls(res[1], res[2], res[0], res[3])

    @classmethod
    def get(cls, user_id):
        conn = sqlite3.connect("logger.db")
        c = conn.cursor()
        res = c.execute("""
                    SELECT * FROM users
                    WHERE id = ?
                    """, (user_id,)).fetchone()
        if res:
            return cls(res[1], res[2], res[0], res[3])

    def save(self):
        conn = sqlite3.connect("logger.db")
        c = conn.cursor()
        c.execute("""
                INSERT INTO users
                VALUES (?, ?, ?, ?)
                """, (self.id, self.username, self.password_hash, time.time()))
        conn.commit()

    def to_dict(self):
        d = dict()
        d['username'] = self.username
        d['id'] = self.id

    def validate(self, password):
        if self.password_hash == hashlib.sha3_512(password.encode('utf-8')).hexdigest():
            self.authenticated = True
            return True
