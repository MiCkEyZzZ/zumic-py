from typing import Optional, Union
import socket

from zumic.exceptions import ConnectionError, InvalidResponse, ResponseError

CRLF = b"\r\n"

class Connection:
    def __init__(self, host: str = "localhost", port: int = 6379, timeout: Optional[float] = None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.__sock: Optional[socket.socket] = None

    def connect(self):
        if self.__sock:
            return
        try:
            self.__sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        except (socket.timeout, socket.error) as e:
            # Декодируем байты для вывода в строку
            raise ConnectionError(f"Не удалось подключиться к {self.host}:{self.port}") from e

    def disconnect(self):
        if self.__sock:
            try:
                self.__sock.close()
            finally:
                self.__sock = None

    def send(self, data: bytes):
        if not self.__sock:
            raise ConnectionError("Нет активного соединения")
        try:
            self.__sock.sendall(data)
        except socket.error as e:
            raise ConnectionError("Ошибка отправки данных") from e

    def receive(self, bufsize: int = 4096) -> bytes:
        if not self.__sock:
            raise ConnectionError("Нет активного соединения")
        try:
            data = self.__sock.recv(bufsize)
            if not data:
                raise InvalidResponse("Пустой ответ от сервера")
            return data
        except socket.error as e:
            raise ConnectionError("Ошибка получения данных") from e

    def pack_command(self, *args: Union[str, bytes]) -> bytes:
        parts = []
        parts.append(f"*{len(args)}".encode("utf-8") + CRLF)
        for arg in args:
            if isinstance(arg, str):
                arg = arg.encode("utf-8")
            parts.append(f"${len(arg)}".encode("utf-8") + CRLF)
            parts.append(arg + CRLF)
        return b"".join(parts)

    def send_command(self, *args: Union[str, bytes]):
        self.disconnect()
        packed = self.pack_command(*args)
        self.send(packed)

    def read_response(self) -> Union[str, int, None]:
        response = self.receive()
        if not response:
            raise InvalidResponse("Пустой ответ от сервера")

        prefix = response[0:1]
        payload = response[1:].decode(errors="replace").strip()

        if prefix == b"+":
            return payload
        elif prefix == b":":
            return int(payload)
        elif prefix == b"$":
            length = int(payload)
            if length == -1:
                return None
            data = self.receive(length + 2)  # плюс \r\n
            return data[:-2].decode(errors="replace")
        elif prefix == b"-":
            # Тут декодируем payload в строку, чтобы не было ошибки mypy
            raise ResponseError(payload)
        else:
            # Декодируем prefix, чтобы в сообщении была строка, а не байты
            raise InvalidResponse(f"Неизвестный префикс: {prefix.decode(errors='replace')}")
