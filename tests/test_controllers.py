import base64
import json
from flask import url_for

headers = {"Authorization": "Basic %s" % base64.b64encode(bytes("admin1:pass1", 'ascii')).decode('ascii')}


def post_message(client, data):
    messages = client.post(url_for("messages"), data=json.dumps(data), headers=headers)
    assert messages.status_code == 200
    response_data = json.loads(messages.data)
    assert response_data['message'] == data['message']
    assert response_data['message_type'] == data['message_type']


def get_messages(client, query_string):
    messages = client.get(url_for("messages"), headers=headers, query_string=query_string)
    assert messages.status_code == 200
    return json.loads(messages.data)


def test_post_messages(client):
    data = {'message': 'a',
            'message_type': 'INFO'}
    post_message(client, data)


def test_get_messages(client):
    messages_data = get_messages(client, {})
    assert len(messages_data) == 1


def test_get_messages_params(client):
    # create 3 more messages
    data = {'message': 'b',
            'message_type': 'INFO'}
    post_message(client, data)

    data['message'] = 'c'
    data['message_type'] = 'ERROR'
    post_message(client, data)

    data['message'] = 'd'
    data['message_type'] = 'ERROR'
    post_message(client, data)

    # test message type
    query_string = {'message_type': 'INFO'}
    messages_data = get_messages(client, query_string)
    assert len(messages_data) == 2
    for message in messages_data:
        assert message['message_type'] == 'INFO'

    query_string = {'message_type': 'ERROR'}
    messages_data = get_messages(client, query_string)
    assert len(messages_data) == 2
    for message in messages_data:
        assert message['message_type'] == 'ERROR'

    # test paging
    query_string = {'page': 1,
                    'page_size': 2}
    messages_data = get_messages(client, query_string)
    assert len(messages_data) == 2
    assert messages_data[0]['message'] == 'd'
    assert messages_data[1]['message'] == 'c'

    query_string = {'page': 2,
                    'page_size': 2}
    messages_data = get_messages(client, query_string)
    assert len(messages_data) == 2
    assert messages_data[0]['message'] == 'b'
    assert messages_data[1]['message'] == 'a'

# TODO aggregate endpoint test
# TODO messages get error codes test