import json
from flask import Flask, request, Response
from logger_server.exceptions import InvalidPayload
from logger_server.models import insert_message

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    return 'Hello, World!'


@app.route('/', methods=['POST'])
def post():
    data = json.loads(request.data)
    if 'message' not in data:
        raise InvalidPayload("message is required")
    insert_message(data['message'], data.get("message_type"))
    return Response(status=201)
