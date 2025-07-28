from typing import Protocol, Union


class ConnectionProtocol(Protocol):
    def connect(self) -> None:
        """Устанавливает соединение с сервером."""
        ...

    def is_connected(self) -> bool:
        """Возвращает True, если соединение активно."""
        ...

    def send_command(self, *args: Union[str, bytes]) -> None:
        """Упаковывает и отправляет команду на сервер."""
        ...

    def read_response(self) -> Union[str, int, None]:
        """Читает и возвращает распарсенный ответ сервера."""
        ...

    def disconnect(self) -> None:
        """Закрывает соединение."""
        ...
