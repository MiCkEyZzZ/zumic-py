from typing import Union, Any

class MockConnection:
    def __init__(self):
        self.commands = []
        self.responses = []
        self.connected = True

    def connect(self):
        self.connected = True

    def is_connected(self) -> bool:
        return self.connected

    def send_command(self, *args: Any) -> None:
        self.commands.append(args)

    def read_response(self) -> Union[str, int, None]:
        if self.responses:
            return self.responses.pop(0)
        return None

    def disconnect(self):
        self.connected = False

    def set_responses(self, responses):
        self.responses = responses[:]
