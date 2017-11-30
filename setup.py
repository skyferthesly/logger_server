from setuptools import setup, find_packages
import pip

setup(name='logger_server',
      packages=find_packages(exclude=['tests']),
      version='0.1',
      license='MIT',

      description='Webservices that allow storing and retrieving log messages with basic auth',
      long_description=open('README.md').read(),

      url='https://github.com/skyferthesly/logger_server',

      author='Skyler Moore-Firkins',
      author_email='brehon1104@gmail.com',

      setup_requires=['pytest',
                      'requests',
                      'flask'
                      ]
      )

# TODO: pip.main is not part of the public interface
pip.main(["install", 'git+https://github.com/skyferthesly/logger_client'])
