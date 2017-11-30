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
