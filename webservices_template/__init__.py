import configparser
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

# config
config = configparser.ConfigParser()
config.read("config.ini")

# default
app.config['SWAGGER_JSON_URL'] = config['DEFAULT']['SWAGGER_JSON_URL']

if app.config['TESTING']:
    # test
    app.config['DEBUG'] = config['TEST'].getboolean('DEBUG')
    app.config['DATABASE_URI'] = config['TEST']['DATABASE_URI']
else:
    # prod
    app.config['DATABASE_URI'] = config['PROD']['DATABASE_URI']

SWAGGER_URL = '/api/docs'  # no trailing slash
SWAGGER_JSON_URL = app.config['SWAGGER_JSON_URL']

# swagger blueprint
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, SWAGGER_JSON_URL, config={'supportedSubmitMethods': ['get']})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
