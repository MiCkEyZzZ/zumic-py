from zumic.client import Client
from tests.mocks.mock_connection import MockConnection

def test_set_get_delete_cycle_with_mock():
    client = Client(connection=MockConnection())

    assert client.set("foo", "bar") is True
    assert client.get("foo") == "bar"
    assert client.exists("foo") is True
    assert client.delete("foo") == 1
    assert client.get("foo") is None
