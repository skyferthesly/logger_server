from logger_server import app
from flask import jsonify


class InvalidPayload(Exception):
    status_code = 400

    def __init__(self, message, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload

    def to_dict(self):
        ret = dict(self.payload or ())
        ret['message'] = self.message
        return ret


@app.errorhandler(InvalidPayload)
def prepare_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
