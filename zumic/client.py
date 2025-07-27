from typing import Any, Optional, Union
from zumic.connection import Connection
from zumic.connection_protocol import ConnectionProtocol
from zumic.exceptions import InvalidResponse, ResponseError, ConnectionError


class Client:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 6379,
        timeout: Optional[float] = None,
        connection: Optional[ConnectionProtocol] = None,
    ) -> None:
        self.connection: ConnectionProtocol = connection or Connection(
            host=host, port=port, timeout=timeout
        )

    def execute(self, *args: Union[str, bytes]) -> Any:
        try:
            self.connection.send_command(*args)
            return self.connection.read_response()
        except (ResponseError, InvalidResponse, ConnectionError) as e:
            raise e

    def ping(self) -> bool:
        return self.execute("PING") == "PONG"

    def set(self, key: str, value: str) -> bool:
        return self.execute("SET", key, value) == "OK"

    def get(self, key: str) -> Optional[str]:
        return self.execute("GET", key)

    def delete(self, key: str) -> int:
        return self.execute("DEL", key)

    def exists(self, key: str) -> bool:
        return bool(self.execute("EXISTS", key))

    def close(self) -> None:
        self.connection.disconnect()
