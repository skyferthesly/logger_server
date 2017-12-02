from uuid import uuid4
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # no trailing slash
API_URL = "http://127.0.0.1:5000/spec"  # TODO: move this to config

# swagger blueprint
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'supportedSubmitMethods': ['get']})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.secret_key = str(uuid4())
