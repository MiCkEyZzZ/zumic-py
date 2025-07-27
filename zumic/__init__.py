from zumic.exceptions import (
    AuthenticationError, ConnectionError,
    InvalidResponse, DataError, PubSubError,
    ResponseError, WatchError, ZumicError
)

__version__ = "0.1.0"
VERSION = tuple(map(int, __version__.split('.')))

__all__ = [
    "AuthenticationError", "ConnectionError", "DataError",
    "InvalidResponse", "PubSubError", "ResponseError",
    "WatchError", "ZumicError"
]
