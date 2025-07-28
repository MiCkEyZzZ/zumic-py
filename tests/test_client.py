import pytest

from zumic.client import Client

from tests.mocks.mock_connection import MockConnection

def make_client_with_response(responses):
    mock = MockConnection()
    mock.set_responses(responses)
    return Client(connection=mock), mock

def test_ping_simple():
    client, mock = make_client_with_response(["PONG"])
    assert client.ping() is True
    assert mock.commands[0] == ("PING",)

def test_ping_with_message():
    client, mock = make_client_with_response(["hello"])
    assert client.ping("hello")
    assert mock.commands[0] == ("PING", "hello")

def test_set_get():
    client, mock = make_client_with_response(["OK", "world"])
    assert client.set("foo", "world")
    assert client.get("foo") == "world"

def test_delete_exists():
    client, mock = make_client_with_response([1, 1])
    assert client.delete("foo") is True
    assert client.exists("foo") is True

def test_keys():
    client, mock = make_client_with_response([["foo", "bar"]])
    assert client.keys("*") == ["foo", "bar"]

def test_ttl_expire():
    client, mock = make_client_with_response([42, True])
    assert client.ttl("foo") == 42
    assert client.expire("foo", 100)

def test_type():
    client, mock = make_client_with_response(["string"])
    assert client.type("foo") == "string"

def test_incr_decr_incrby_decrby():
    client, mock = make_client_with_response([2, 0, 7, 2])
    assert client.incr("foo") == 2
    assert client.decr("foo") == 0
    assert client.incrby("foo", 7) == 7
    assert client.decrby("foo", 5) == 2

def test_append_strlen():
    client, mock = make_client_with_response([6, 6])
    assert client.append("foo", "barbaz") == 6
    assert client.strlen("foo") == 6

def test_flushdb_flushall_dbsize():
    client, mock = make_client_with_response(["OK", "OK", 15])
    assert client.flushdb() is True
    assert client.flushall() is True
    assert client.dbsize() == 15

def test_close_context_manager():
    client, mock = make_client_with_response([])
    with client as c:
        assert c is client
    assert not mock.is_connected()

def test_execute_empty():
    client, mock = make_client_with_response([])
    with pytest.raises(ValueError):
        client.execute()
