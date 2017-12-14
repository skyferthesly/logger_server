import pip
import sys
from setuptools import setup, find_packages

setup(name='webservices_template',
      packages=find_packages(exclude=['tests']),
      version='0.1',
      license='MIT',

      description='Template webservices that allow storing and retrieving log messages with basic auth',
      long_description=open('README.md').read(),

      url='https://github.com/skyferthesly/webservices_template',

      author='Skyler Moore-Firkins',
      author_email='brehon1104@gmail.com',

      install_requires=['pytest>=3.3.0',
                        'requests>=2.18.4',
                        'flask>=0.12.2',
                        'flask-swagger>=0.2.13',
                        'flask-swagger-ui>=3.0.12',
                        'pytest-flask>=0.10.0',
                        'pytest-runner>=3.0',
                        'flask-cors>=3.0.3'
                        ],
      setup_requires=['flask>=0.12.2',
                      'pytest>=3.3.0',
                      'pytest-runner>=3.0',
                      'flask-swagger>=0.2.13',
                      'flask-swagger-ui>=3.0.12',
                      'flask-cors>=3.0.3'],
      tests_require=['pytest>=3.3.0'],
      test_suite='tests'
      )

if len(sys.argv) > 1 and sys.argv[1] == 'install':
    from webservices_template.database import setup_db
    from webservices_template.models import create_admin_user

    # TODO: pip.main is not part of the public interface
    pip.main(["install", 'git+https://github.com/skyferthesly/logger_client'])
    setup_db()
    create_admin_user()
