# logger_server
Basic webservices to store and retrieve log messages

# Getting Started
Clone the project, run the standard `python setup.py install`. This will install all dependencies including the external client.

Starting webservices:

    1. export FLASK_APP=logger_server/controllers.py
    2. flask run

Starting client:

    1. ipython logger_server/client.py
    
# Requirements
1. Must be able to store messages of two types: error, info
2. Must be able to retrieve list of log messages with basic filtration
3. Must be able to provide aggregate data
4. Must have authentication
5. Must have documentation
