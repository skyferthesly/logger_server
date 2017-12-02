import pip
import hashlib
from setuptools import setup, find_packages
from logger_server.setup_db import setup_db
from logger_server.models import User

setup(name='logger_server',
      packages=find_packages(exclude=['tests']),
      version='0.1',
      license='MIT',

      description='Webservices that allow storing and retrieving log messages with basic auth',
      long_description=open('README.md').read(),

      url='https://github.com/skyferthesly/logger_server',

      author='Skyler Moore-Firkins',
      author_email='brehon1104@gmail.com',

      install_requires=['pytest',
                        'requests',
                        'flask',
                        ]
      )

# TODO: pip.main is not part of the public interface
pip.main(["install", 'git+https://github.com/skyferthesly/logger_client'])
setup_db()
User('admin1', hashlib.sha3_512('pass1'.encode('utf-8')).hexdigest()).save()
