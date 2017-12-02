import sqlite3
import time
import hashlib
from uuid import uuid4


class Message(object):
    def __init__(self, message, message_type=None, _time=None, email=None):
        self.message = message
        self.message_type = message_type or 'INFO'
        self.time = _time or time.time()
        self.email = email

    def save(self):
        conn = sqlite3.connect("logger.db")
        c = conn.cursor()
        c.execute("""
                INSERT INTO messages
                VALUES (?, ?, ?, ?)
                """, (self.message, self.message_type, self.time, self.email))
        conn.commit()
        return self

    def to_dict(self):
        d = dict()
        d['message'] = self.message
        d['message_type'] = self.message_type
        d['time'] = self.time
        d['email'] = self.email
        return d

    @classmethod
    def get_top(cls, timestamp=None, message_type=None, page=None, page_size=None, reverse_sort=None):
        conn = sqlite3.connect("logger.db")
        c = conn.cursor()

        q = "SELECT * FROM messages AS m"
        wheres = list()
        params = list()
        if timestamp:
            wheres.append("m.time = ?")
            params.append(timestamp)
        if message_type:
            wheres.append('m.message_type = ?')
            params.append(message_type)

        if wheres:
            q += " WHERE %s" % " AND ".join(wheres)

        q += ' ORDER BY m.time %s' % ('' if reverse_sort else 'desc')
        if page:
            if not page_size:
                page_size = 1
            limit = page_size
            offset = page * page_size - page_size if page != 1 else 0
            q += ' LIMIT %s OFFSET %s' % (limit, offset)

        print(q)
        print(params)
        res = c.execute(q, params)
        messages = []
        for r in res:
            messages.append(cls(r[0], r[1], r[2], r[3]))
        return messages

    @classmethod
    def get_aggregate(cls):
        conn = sqlite3.connect("logger.db")
        c = conn.cursor()
        res = c.execute("""
                SELECT strftime('%-H', datetime(m.time, 'unixepoch', 'localtime')), COUNT(*)
                FROM messages AS m
                GROUP BY strftime('%-H', m.time)
                """)

        response = dict()
        for r in res:
            response[r[0]]: r[1]
        return response

    @classmethod
    def validate_message_type(cls, message_type):
        if message_type in ['INFO', 'ERROR']:
            return True


class User(object):
    def __init__(self, username, password_hash, id=None, created_at=None):
        self.username = username
        self.password_hash = password_hash
        self.id = id or str(uuid4())
        self.created_at = created_at or time.time()

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
            return True
