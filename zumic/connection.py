from typing import Optional, Union, cast
import socket

from zumic.exceptions import ConnectionError, InvalidResponse, ResponseError

CRLF = b"\r\n"


class Connection:
    def __init__(
        self, host: str = "localhost", port: int = 6174, timeout: Optional[float] = None
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None
        self._connected = False

    def connect(self):
        """Устанавливает соединение с сервером."""
        if self._connected and self._sock:
            return

        try:
            self._sock = socket.create_connection(
                (self.host, self.port), timeout=self.timeout
            )
            self._connected = True
        except OSError as e:
            raise ConnectionError(
                f"Не удалось подключиться к {self.host}:{self.port}"
            ) from e

    def disconnect(self):
        """Закрывает соединение с сервером."""
        if self._sock:
            try:
                self._sock.close()
            except socket.error:
                pass  # Игнорируем ошибки при закрытии
            finally:
                self._sock = None
                self._connected = False

    def is_connected(self) -> bool:
        """Проверяет, активно ли соединение."""
        return self._connected and self._sock is not None

    def send(self, data: bytes):
        """Отправляет данные на сервер."""
        if not self.is_connected():
            self.connect()

        # Приводим тип, чтобы Pyright понял, что это не None
        sock = cast(socket.socket, self._sock)
        try:
            sock.sendall(data)
        except socket.error as e:
            self._connected = False
            raise ConnectionError("Ошибка отправки данных") from e

    def receive(self, bufsize: int = 4096) -> bytes:
        """Получает данные от сервера."""
        if not self.is_connected():
            raise ConnectionError("Нет активного соединения")

        # Явная проверка, чтобы Pyright сузил тип _sock до socket.socket
        if self._sock is None:
            # На всякий случай, хотя is_connected уже гарантирует, что сокет есть
            self._connected = False
            raise ConnectionError("Нет активного соединения")

        try:
            data = self._sock.recv(bufsize)
            if not data:
                self._connected = False
                raise ConnectionError("Соединение закрыто сервером")
            return data
        except socket.error as e:
            self._connected = False
            raise ConnectionError("Ошибка получения данных") from e

    def pack_command(self, *args: Union[str, bytes]) -> bytes:
        """Упаковывает команду в Zumic-протокол (ZSP)."""
        parts = []
        parts.append(f"*{len(args)}".encode("utf-8") + CRLF)

        for arg in args:
            if isinstance(arg, str):
                arg = arg.encode("utf-8")
            parts.append(f"${len(arg)}".encode("utf-8") + CRLF)
            parts.append(arg + CRLF)

        return b"".join(parts)

    def send_command(self, *args: Union[str, bytes]):
        """Отправляет команду на сервер."""
        if not args:
            raise ValueError("Команда не может быть пустой")

        packed = self.pack_command(*args)
        self.send(packed)

    def read_response(self) -> Union[str, int, None]:
        """Читает ответ от сервера."""
        response = self.receive()
        if not response:
            raise InvalidResponse("Пустой ответ от сервера")

        return self._parse_response(response)

    def _parse_response(self, response: bytes) -> Union[str, int, None]:
        """Парсит ответ сервера согласно RESP протоколу."""
        if len(response) < 2:
            raise InvalidResponse("Слишком короткий ответ от сервера")

        prefix = response[0:1]
        payload = response[1:].decode(errors="replace").strip()

        if prefix == b"+":  # Simple String
            return payload
        elif prefix == b":":  # Integer
            try:
                return int(payload)
            except ValueError:
                raise InvalidResponse(f"Некорректное целое число: {payload}")
        elif prefix == b"$":  # Bulk String
            try:
                length = int(payload)
            except ValueError:
                raise InvalidResponse(f"Некорректная длина строки: {payload}")

            if length == -1:
                return None

            # Читаем данные указанной длины + CRLF
            data = self.receive(length + 2)
            if len(data) < length + 2:
                raise InvalidResponse("Неполные данные от сервера")

            return data[:-2].decode(errors="replace")
        elif prefix == b"-":  # Error
            raise ResponseError(payload)
        else:
            raise InvalidResponse(
                f"Неизвестный префикс: {prefix.decode(errors='replace')}"
            )

    def __enter__(self):
        """Поддержка контекстного менеджера."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие соединения."""
        self.disconnect()
        return False
