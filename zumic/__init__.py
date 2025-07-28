from zumic.connection import Connection

from zumic.exceptions import (
    AuthenticationError,
    ConnectionError,
    InvalidResponse,
    DataError,
    PubSubError,
    ResponseError,
    WatchError,
    ZumicError,
)

# Эта версия используется при создании пакета для публикации
__version__ = "0.1.0"
VERSION = tuple(map(int, __version__.split(".")))

__all__ = [
    "AuthenticationError",
    "ConnectionError",
    "Connection",
    "DataError",
    "InvalidResponse",
    "PubSubError",
    "ResponseError",
    "WatchError",
    "ZumicError",
]
