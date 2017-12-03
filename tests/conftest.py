import pytest
import configparser
from logger_server.models import create_admin_user
from logger_server.controllers import app as _app
from logger_server.database import setup_db, clear_db


@pytest.fixture(scope='session')
def app():
    config = configparser.ConfigParser()
    config.read("config.ini")
    _app.config['DATABASE_URI'] = config['TEST']['DATABASE_URI']
    setup_db()
    create_admin_user()
    clear_db()
    return _app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()
