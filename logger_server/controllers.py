import json
import re
from flask import jsonify
from flask.views import MethodView
from logger_server.exceptions import InvalidPayload
from logger_server.models import User, Message
from logger_server import app
from functools import wraps
from flask import request, Response


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        user = User.get_by_username(auth.username)
        if not auth or not user or not user.validate(auth.password):
            return Response('Incorrect username/password', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)

    return decorated


class Messages(MethodView):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    @login_required
    def get(self):
        return jsonify([m.to_dict() for m in Message.get_top(request.args.get('count'))])

    @login_required
    def post(self):
        data = json.loads(request.data)
        if 'message' not in data:
            raise InvalidPayload("message is required")
        email = data.get('email')
        if not re.match(self.email_regex, email):
            raise InvalidPayload("email is invalid")
        message = Message(data['message'], data.get('message_type'), email=email).save()
        return jsonify(message.to_dict())


app.add_url_rule('/messages/', view_func=Messages.as_view('messages_api'), methods=['GET', 'POST'])


class AggregateMessageData(MethodView):
    def get(self):
        # TODO:
        pass


class Users(MethodView):
    def get(self, user_id):
        return jsonify(User.get(user_id).to_dict())

    def post(self):
        # TODO:
        pass


app.add_url_rule('/users/', view_func=Users.as_view('users_api'), methods=['GET'])
