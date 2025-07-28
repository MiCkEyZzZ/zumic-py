import pytest

from zumic.exceptions import (
    AuthenticationError, ConnectionError, InvalidResponse,
    ResponseError, DataError, PubSubError, WatchError, ZumicError
)

@pytest.mark.parametrize("exc", [
    AuthenticationError, ConnectionError, InvalidResponse, ResponseError,
    DataError, PubSubError, WatchError, ZumicError
])
def test_exceptions_raises(exc):
    with pytest.raises(exc):
        raise exc("test")
