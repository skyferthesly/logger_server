import json
import hashlib
from flask import Flask, request, Response, flash
from flask.views import MethodView
from flask_login import login_user
from logger_server.exceptions import InvalidPayload
from logger_server.models import insert_message, User

app = Flask(__name__)


class Messages(MethodView):
    def post(self):
        data = json.loads(request.data)
        if 'message' not in data:
            raise InvalidPayload("message is required")
        insert_message(data['message'], data.get("message_type"))
        return Response(status=201)

app.add_url_rule('messages/', view_func=Messages, methods=['POST'])


class Users(MethodView):
    def get(self, user_id):
        return json.dumps(User.get(user_id).to_dict())

app.add_url_rule('users/', view_func=Users, methods=['GET'])


@app.route('login', methods=['GET'])
def login(username, password):
    user = User.get(username)
    if user.validate(password):
        login_user(user)
        flash('Logged in successfully')

        # TODO: check request.args.get('next') to ensure protection from redirects
        # TODO: http://flask.pocoo.org/snippets/62/

# @app.route('/', methods=['GET'])
# def get():
#     return 'Hello, World!'
#
#
# @app.route('/', methods=['POST'])
# def post():
#     data = json.loads(request.data)
#     if 'message' not in data:
#         raise InvalidPayload("message is required")
#     insert_message(data['message'], data.get("message_type"))
#     return Response(status=201)
