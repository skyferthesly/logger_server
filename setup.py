import pip
import sys
from setuptools import setup, find_packages

setup(name='logger_server',
      packages=find_packages(exclude=['tests']),
      version='0.2',
      license='MIT',

      description='Webservices that allow storing and retrieving log messages with basic auth',
      long_description=open('README.md').read(),

      url='https://github.com/skyferthesly/logger_server',

      author='Skyler Moore-Firkins',
      author_email='brehon1104@gmail.com',

      install_requires=['pytest>=3.3.0',
                        'requests>=2.18.4',
                        'flask>=0.12.2',
                        'flask-swagger>=0.2.13',
                        'flask-swagger-ui>=3.0.12',
                        'pytest-flask>=0.10.0',
                        'pytest-runner>=3.0'
                        ],
      setup_requires=['flask>=0.12.2',
                      'pytest>=3.3.0',
                      'pytest-runner>=3.0',
                      'flask-swagger>=0.2.13',
                      'flask-swagger-ui>=3.0.12'],
      tests_require=['pytest>=3.3.0'],
      test_suite='tests'
      )

if len(sys.argv) > 1 and sys.argv[1] == 'install':
    from logger_server.database import setup_db
    from logger_server.models import create_admin_user

    # TODO: pip.main is not part of the public interface
    pip.main(["install", 'git+https://github.com/skyferthesly/logger_client'])
    setup_db()
    create_admin_user()
