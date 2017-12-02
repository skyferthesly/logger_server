import json
import re
from flask import jsonify
from flask.views import MethodView
from logger_server.exceptions import InvalidPayload
from logger_server.models import User, Message
from logger_server import app
from functools import wraps
from flask import request, Response
from flask_swagger import swagger


def bad_auth_response():
    return Response('Incorrect username/password', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return bad_auth_response()
        user = User.get_by_username(auth.username)
        if not user or not user.validate(auth.password):
            return bad_auth_response()
        return f(*args, **kwargs)

    return decorated


class Messages(MethodView):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    @login_required
    def get(self):
        """
        Gets messages
        ---
        tags:
          - messages
        parameters:
          - in: query
            name: timestamp
            type: float
            required: false
            description: get messages with timestamp
          - in: query
            name: message_type
            type: string
            required: false
            description: filter by message type. possible options are INFO and ERROR
          - in: page
            name: page
            type: int
            required: false
            description: page number
          - in: query
            name: page_size
            type: int
            required: false
            description: page size
          - in: query
            name: reverse_sort
            type: boolean
            required: false
            description: by default, messages are sorted descending wrt to time. this sorts them ascending
        responses:
          200:
            description: messages
          401:
            description: unauthorized
        """
        message_type = request.args.get('message_type')
        if message_type:
            message_type = message_type.upper()
            if not Message.validate_message_type(message_type):
                raise InvalidPayload("message_type is invalid")

        return jsonify([m.to_dict() for m in Message.get_top(timestamp=request.args.get('timestamp', type=float),
                                                             message_type=request.args.get('message_type', type=str),
                                                             page=request.args.get('page', type=int),
                                                             page_size=request.args.get('page_size', type=int),
                                                             reverse_sort=request.args.get('reverse_sort', type=bool)
                                                             )])

    @login_required
    def post(self):
        """
        Creates a new message
        ---
        tags:
          - messages
        parameters:
          - in: body
            name: message
            type: string
            required: true
            description: the body of the message
          - in: body
            name: message_type
            type: string
            required: false
            description: the type of message, either INFO or ERROR. defaults to INFO
          - in: body
            name: email
            required: false
            description: email
        responses:
          200:
            description: the message was created.
          401:
            description: unauthorized
        """
        data = json.loads(request.data)
        if 'message' not in data:
            raise InvalidPayload("message is required")
        email = data.get('email')
        if email and not re.match(self.email_regex, email):
            raise InvalidPayload("email is invalid")
        message_type = data.get('message_type')
        if message_type:
            message_type = message_type.upper()
            if not Message.validate_message_type(message_type):
                raise InvalidPayload("message_type is invalid")

        message = Message(data['message'], message_type, email=email).save()
        return jsonify(message.to_dict())


app.add_url_rule('/messages/', view_func=Messages.as_view('messages_api'), methods=['GET', 'POST'])


class AggregateMessageData(MethodView):
    @login_required
    def get(self):
        """
        Returns aggregate message data by hour
        ---
        tags:
          - messages
        responses:
          200:
            description: aggregate message data
          401:
            description: unauthorized
        """
        return jsonify(Message.get_aggregate())


app.add_url_rule('/messages/aggregated/', view_func=AggregateMessageData.as_view('aggregate_messages_api'),
                 methods=['GET'])


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "0.1"
    swag['info']['title'] = "Simplified Central Logger API"
    swag['info']['description'] = "API to store and retrieve log messages"
    swag['info']['contact'] = "brehon1104@gmail.com"
    swag['info']['url'] = 'https://github.com/skyferthesly/logger_server'
    return jsonify(swag)
