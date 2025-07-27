from typing import Union
from zumic.connection_protocol import ConnectionProtocol

class MockConnection(ConnectionProtocol):
    def __init__(self):
        self.store = {}

    def send_command(self, *args: Union[str, bytes]):
        self.last_command = [a.decode() if isinstance(a, bytes) else a for a in args]

    def read_response(self):
        cmd = self.last_command
        if cmd[0] == "SET":
            self.store[cmd[1]] = cmd[2]
            return "OK"
        elif cmd[0] == "GET":
            return self.store.get(cmd[1])
        elif cmd[0] == "DEL":
            return int(self.store.pop(cmd[1], None) is not None)
        elif cmd[0] == "EXISTS":
            return int(cmd[1] in self.store)
        elif cmd[0] == "PING":
            return "PONG"
        return None

    def disconnect(self):
        pass
