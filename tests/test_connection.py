import pytest
from zumic.connection import Connection
from zumic.exceptions import ConnectionError

def test_connect_invalid_host():
    conn = Connection(host="256.256.256.256", port=9999, timeout=0.1)
    with pytest.raises(ConnectionError):
        conn.connect()

def test_receive_without_connect():
    conn = Connection()
    with pytest.raises(ConnectionError):
        conn.receive()

def test_send_without_connect():
    conn = Connection()
    with pytest.raises(ConnectionError):
        conn.send(b"PING")
