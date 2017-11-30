import json
from flask import request, flash, jsonify
from flask.views import MethodView
from flask_login import login_user, login_required
from logger_server.exceptions import InvalidPayload
from logger_server.models import User, Message
from logger_server import app


class Messages(MethodView):
    @login_required
    def post(self):
        data = json.loads(request.data)
        if 'message' not in data:
            raise InvalidPayload("message is required")
        message = Message(data['message'], data.get('message_type')).save()
        return jsonify(message.to_dict())


app.add_url_rule('/messages/', view_func=Messages.as_view('messages_api'), methods=['POST'])


class Users(MethodView):
    def get(self, user_id):
        return jsonify(User.get(user_id).to_dict())


app.add_url_rule('/users/', view_func=Users.as_view('users_api'), methods=['GET'])


@app.route('/login', methods=['GET'])
def login():
    user = User.get(request.form['username'])
    if user.validate(request.form['password']):
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
