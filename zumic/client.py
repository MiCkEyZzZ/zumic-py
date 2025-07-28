from typing import Any, Optional, Union, List

from zumic.connection import Connection
from zumic.connection_protocol import ConnectionProtocol


class Client:
    """Клиент для работы с Zumic БД."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 6174,
        timeout: Optional[float] = None,
        connection: Optional[ConnectionProtocol] = None,
        decode_responses: bool = True,
    ) -> None:
        """
        Инициализирует клиент Zumic.

        Args:
            host: Адрес сервера
            port: Порт сервера
            timeout: Таймаут соединения
            connection: Кастомное соединение
            decode_responses: Декодировать ответы в строки
        """
        self.connection: ConnectionProtocol = connection or Connection(
            host=host, port=port, timeout=timeout
        )
        self.decode_responses = decode_responses

    def execute(self, *args: Union[str, bytes]) -> Any:
        """
        Выполняет команду на сервере.

        Args:
            *args: Аргументы команды

        Returns:
            Ответ сервера

        Raises:
            ResponseError: Ошибка от сервера
            InvalidResponse: Некорректный ответ
            ConnectionError: Ошибка соединения
        """
        if not args:
            raise ValueError("Команда не может быть пустой")

        # Отправляем и читаем ответ напрямую:
        self.connection.send_command(*args)
        response = self.connection.read_response()

        # Декодируем байты в строки, если включено декодирование
        if self.decode_responses and isinstance(response, bytes):
            response = response.decode("utf-8", errors="replace")  # type: ignore[unreachable]

        return response

    def ping(self, message: Optional[str] = None) -> Union[str, bool]:
        """
        Проверяет соединение с сервером.

        Args:
            message: Опциональное сообщение

        Returns:
            "PONG" или переданное сообщение
        """
        if message is not None:
            return self.execute("PING", message) == message
        return self.execute("PING") == "PONG"

    def set(self, key: str, value: Union[str, bytes], **kwargs) -> bool:
        """
        Устанавливает значение ключа.

        Args:
            key: Ключ
            value: Значение
            **kwargs: Дополнительные параметры (EX, PX, NX, XX)

        Returns:
            True если операция успешна
        """
        args: List[Union[str, bytes]] = ["SET", key, value]
        if "ex" in kwargs:
            args += ["EX", str(kwargs["ex"])]
        if "px" in kwargs:
            args += ["PX", str(kwargs["px"])]
        if kwargs.get("nx"):
            args.append("NX")
        if kwargs.get("xx"):
            args.append("XX")
        return self.execute(*args) == "OK"

    def get(self, key: str) -> Optional[str]:
        """
        Получает значение ключа.

        Args:
            key: Ключ

        Returns:
            Значение ключа или None если ключ не найден
        """
        return self.execute("GET", key)

    def delete(self, *keys: str) -> bool:
        """
        Удаляет один или несколько ключей.

        Args:
            *keys: Ключи для удаления

        Returns:
            True если хотя бы один ключ удалён, иначе False
        """
        if not keys:
            return False
        return bool(self.execute("DEL", *keys))

    def exists(self, *keys: str) -> bool:
        """
        Проверяет существование ключей.

        Args:
            *keys: Ключи для проверки

        Returns:
            True если хотя бы один ключ существует
        """
        if not keys:
            return False
        return bool(self.execute("EXISTS", *keys))

    def keys(self, pattern: str = "*") -> List[str]:
        """
        Возвращает список ключей по шаблону.

        Args:
            pattern: Шаблон поиска

        Returns:
            Возвращает список ключей по шаблону.
        """
        result = self.execute("KEYS", pattern)
        return result if isinstance(result, list) else []

    def ttl(self, key: str) -> int:
        """
        Возвращает время жизни ключа в секундах.

        Args:
            key: Ключ

        Returns:
            Время жизни в секундах (-1 если ключ постоянный, -2 если не существует)
        """
        return self.execute("TTL", key)

    def expire(self, key: str, seconds: int) -> bool:
        """
        Устанавливает время жизни ключа.

        Args:
            key: Ключ
            seconds: Время жизни в секундах

        Returns:
            True если операция успешна
        """
        return bool(self.execute("EXPIRE", key, str(seconds)))

    def type(self, key: str) -> str:
        """
        Возвращает тип значения ключа.

        Args:
            key: Ключ

        Returns:
            Тип значения
        """
        return self.execute("TYPE", key)

    # Команды для работы со строками.
    def incr(self, key: str) -> int:
        """
        Увеличивает значение ключа на 1.

        Args:
            key: Ключ

        Returns:
            Новое значение
        """
        return self.execute("INCR", key)

    def decr(self, key: str) -> int:
        """
        Уменьшает значение ключа на 1.

        Args:
            key: Ключ

        Returns:
            Новое значение
        """
        return self.execute("DECR", key)

    def incrby(self, key: str, amount: int) -> int:
        """
        Увеличивает значение ключа на указанное количество.

        Args:
            key: Ключ
            amount: Количество для увеличения

        Returns:
            Новое значение
        """
        return self.execute("INCRBY", key, str(amount))

    def decrby(self, key: str, amount: int) -> int:
        """
        Уменьшает значение ключа на указанное количество.

        Args:
            key: Ключ
            amount: Количество для уменьшения

        Returns:
            Новое значение
        """
        return self.execute("DECRBY", key, str(amount))

    def append(self, key: str, value: str) -> int:
        """
        Добавляет строку к значению ключа.

        Args:
            key: Ключ
            value: Строка для добавления

        Returns:
            Новая длина строки
        """
        return self.execute("APPEND", key, value)

    def strlen(self, key: str) -> int:
        """
        Возвращает длину строки.

        Args:
            key: Ключ

        Returns:
            Длина строки
        """
        return self.execute("STRLEN", key)

    # Служебные методы
    def flushdb(self) -> bool:
        """
        Очищает текущую базу данных.

        Returns:
            True если операция успешна
        """
        return self.execute("FLUSHDB") == "OK"

    def flushall(self) -> bool:
        """
        Очищает все базы данных.

        Returns:
            True если операция успешна
        """
        return self.execute("FLUSHALL") == "OK"

    def dbsize(self) -> int:
        """
        Возвращает количество ключей в базе данных.

        Returns:
            Количество ключей
        """
        return self.execute("DBSIZE")

    def close(self) -> None:
        """Закрывает соединение с сервером."""
        self.connection.disconnect()

    def __enter__(self):
        """Поддержка контекстного менеджера."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие соединения."""
        self.close()
        return False
