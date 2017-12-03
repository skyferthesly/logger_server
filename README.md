# Simplified Central Logger
Prototype for a webservice to store and retrieve log messages.

# Getting Started
Clone the project, run the standard `python setup.py install`. This will
install all dependencies including the external client.

Starting webservices:

    1. export FLASK_APP=logger_server/controllers.py
    2. flask run

Starting client:

    1. export SIMPLIFIED_LOGGER_SERVER_URI=<YOUR_SERVER_URI>
    2. export MESSAGES_ENDPOINT=<YOUR_MESSAGES_ENDPOINT>
    3. python logger_server/client.py

SERVER_URI for local is http://127.0.0.1:5000/ by default.\
MESSAGES_ENDPOINT is messages/ by default.

**Note**: it is unusual to import a client into a server project. This
is ONLY to prove that the client can be installed as an external dependency.
You find can more information about the client [here](https://github.com/skyferthesly/logger_client).

# Usage
The API is documented using swagger. After starting the server, head over
to <YOUR_SERVER_URI>/api/docs/ for documentation on how to use the API. \
**NOTE**: if you're running the server locally, the default address will
 be http://127.0.0.1:5000/api/docs/

This prototype has one user with credentials: \
username: admin1\
password: pass1

Additionally, tests can be ran via `python setup.py test`
# Improvements
**Sqlite**\
Sqlite is a file-based database and doesn't have the bells and whistles that
a proper server-based database has. As such, a multiple user system, or
a system that requires many write operations will fall short with Sqlite.
For this prototype, Sqlite did the job, but once this app is used in
production, given that it's a logger server which will require heavy
write operations, Sqlite needs to be upgraded
to a proper RDBMS such as PostgreSQL.

**Authentication**\
This API uses a very simple basic authentication check when accessing
the endpoints. There is no mechanism for session or token based authentication.
As such, granular access to specific endpoints isn't possible. Additionally,
this auth system is susceptible to brute force attacks as no record of
login attempts is stored. For the next iteration of this app, a proper
server-side session management system should be implemented.

**Client Identification**\
Currently, this API doesn't differentiate messages sent by different clients.
Something as simple as having a "client" table with an id and name would
suffice in allowing clients to store messages with its specific identifier.

**Filtering by Message Content**\
Being able to filter by user_id or client_id would be a welcomed addition
to this API's functionality. To achieve this, first we need to store
this extra data with the message. After that, it's as simple as passing
it as a query parameter to the messages GET endpoint. It will work just
like filtering for message_type or paging does today.

**Data Maintenance**\
Being a central logging server, the messages data could be huge after
only a short time. A mechanism to trim messages either by an expiration
date (e.g. deletion after 30 days), and/or by maximum allowed messages
would be beneficial. This can be achieved by a scheduled operation. One
simple implementation is a `while True` loop that runs a cleanup query
against the messages tables, and goes to sleep for a set amount of time.
There's also a python library called sched that could achieve this task
with a larger toolset.
