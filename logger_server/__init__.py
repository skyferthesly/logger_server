import configparser
import sys
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# config
config = configparser.ConfigParser()
config.read("config.ini")

# default
app.config['DEBUG'] = config['DEFAULT'].getboolean('DEBUG')
app.config['TESTING'] = config['DEFAULT'].getboolean('TESTING')
app.config['SWAGGER_JSON_URL'] = config['DEFAULT']['SWAGGER_JSON_URL']

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    # test
    app.config['DEBUG'] = config['TEST'].getboolean('DEBUG')
    app.config['TESTING'] = config['TEST'].getboolean('TESTING')
    app.config['DATABASE_URI'] = config['TEST']['DATABASE_URI']
else:
    # prod
    app.config['DATABASE_URI'] = config['PROD']['DATABASE_URI']

SWAGGER_URL = '/api/docs'  # no trailing slash
SWAGGER_JSON_URL = app.config['SWAGGER_JSON_URL']

# swagger blueprint
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, SWAGGER_JSON_URL, config={'supportedSubmitMethods': ['get']})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
