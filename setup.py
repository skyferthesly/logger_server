import pip
import sys
from setuptools import setup, find_packages
from logger_server.database import setup_db
from logger_server.models import create_admin_user

setup(name='logger_server',
      packages=find_packages(exclude=['tests']),
      version='0.2',
      license='MIT',

      description='Webservices that allow storing and retrieving log messages with basic auth',
      long_description=open('README.md').read(),

      url='https://github.com/skyferthesly/logger_server',

      author='Skyler Moore-Firkins',
      author_email='brehon1104@gmail.com',

      install_requires=['pytest',
                        'requests',
                        'flask',
                        'flask-swagger',
                        'flask-swagger-ui',
                        'pytest-flask',
                        'pytest_runner'
                        ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      test_suite='tests'
      )

if len(sys.argv) > 1 and not sys.argv[1] == 'test':
    # TODO: pip.main is not part of the public interface
    pip.main(["install", 'git+https://github.com/skyferthesly/logger_client'])
    setup_db()
    create_admin_user()
