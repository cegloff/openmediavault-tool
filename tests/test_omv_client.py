import pytest
import responses
from omv_client import OMVClient, OMVError

@responses.activate
def test_login_success():
    responses.add(responses.POST, 'http://omv:80/rpc.php',
                  json={'jsonrpc': '2.0', 'result': 'token123', 'id': 1}, status=200)
    client = OMVClient('omv', username='user', password='pass')
    client.login()
    assert client.auth_token == 'token123'
    assert client.logged_in

@responses.activate
def test_login_failure():
    responses.add(responses.POST, 'http://omv:80/rpc.php',
                  json={'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'Access denied'}, 'id': 1}, status=200)
    client = OMVClient('omv', username='user', password='pass')
    with pytest.raises(OMVError):
        client.login()

@responses.activate
def test_list_shares():
    responses.add(responses.POST, 'http://omv:80/rpc.php',
                  json={'jsonrpc': '2.0', 'result': [{'name': 'shared'}], 'id': 1}, status=200)
    client = OMVClient('omv', username='user', password='pass')
    shares = client.list_shares()
    assert shares == [{'name': 'shared'}]

@responses.activate
def test_get_filesystem_info():
    responses.add(responses.POST, 'http://omv:80/rpc.php',
                  json={'jsonrpc': '2.0', 'result': [{'label': 'shared', 'mounted': True}], 'id': 1}, status=200)
    client = OMVClient('omv', username='user', password='pass')
    info = client.get_filesystem_info('shared')
    assert info['mounted']
