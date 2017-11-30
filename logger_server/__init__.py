from uuid import uuid4
from flask import Flask

app = Flask(__name__)
app.secret_key = str(uuid4())
