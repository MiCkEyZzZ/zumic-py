import pytest
import socket

from zumic.connection import Connection
from zumic.exceptions import ConnectionError, ResponseError

class DummySocket:
    def __init__(self, recv_data=b"+PONG\r\n"):
        self._data = recv_data
        self.sent = []
        self.closed = False

    def sendall(self, data):
        self.sent.append(data)

    def recv(self, bufsize):
        r = self._data
        self._data = b""
        return r

    def close(self):
        self.closed = True

def test_pack_command():
    conn = Connection()
    cmd = conn.pack_command("PING")
    assert cmd == b"*1\r\n$4\r\nPING\r\n"

    cmd2 = conn.pack_command("SET", "foo", "bar")
    assert cmd2 == b"*3\r\n$3\r\nSET\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"

def test_send_and_receive(monkeypatch):
    conn = Connection()
    dummy = DummySocket()
    conn._sock = dummy  # type: ignore[assignment]
    conn._connected = True

    conn.send(b"hello")
    assert dummy.sent[0] == b"hello"

    r = conn.receive()
    assert r == b"+PONG\r\n"

def test_read_response_simple(monkeypatch):
    conn = Connection()
    dummy = DummySocket(b"+OK\r\n")
    conn._sock = dummy  # type: ignore[assignment]
    conn._connected = True

    assert conn.read_response() == "OK"

def test_read_response_error(monkeypatch):
    conn = Connection()
    dummy = DummySocket(b"-ERR error\r\n")
    conn._sock = dummy  # type: ignore[assignment]
    conn._connected = True

    with pytest.raises(ResponseError):
        conn.read_response()

def test_read_response_int(monkeypatch):
    conn = Connection()
    dummy = DummySocket(b":42\r\n")
    conn._sock = dummy  # type: ignore[assignment]
    conn._connected = True

    assert conn.read_response() == 42

def test_read_response_bulk(monkeypatch):
    class BulkSocket(DummySocket):
        def __init__(self):
            self._calls = 0
            self.sent = []
            self.closed = False

        def recv(self, bufsize):
            self._calls += 1
            if self._calls == 1:
                return b"$3\r\n"
            elif self._calls == 2:
                return b"foo\r\n"
            return b""

    conn = Connection()
    dummy = BulkSocket()
    conn._sock = dummy  # type: ignore[assignment]
    conn._connected = True

    # Подмена метода receive для чтения bulk данных
    monkeypatch.setattr(
        conn,
        "receive",
        lambda size=4096: b"$3\r\n" if size == 4096 else b"foo\r\n"
    )

    result = conn._parse_response(b"$3\r\n")
    assert result == "foo"

def raise_oserror(*args, **kwargs):
    raise OSError("fail")

def test_connect_fail(monkeypatch):
    conn = Connection(host="unreachable", port=12345)
    monkeypatch.setattr(socket, "create_connection", raise_oserror)
    with pytest.raises(ConnectionError):
        conn.connect()

def test_disconnect_closes(monkeypatch):
    conn = Connection()
    dummy = DummySocket()
    conn._sock = dummy  # type: ignore[assignment]
    conn._connected = True
    conn.disconnect()
    assert dummy.closed
    assert not conn._connected
