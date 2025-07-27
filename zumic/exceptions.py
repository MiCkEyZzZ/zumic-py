class ZumicError(Exception):
    """Базовое исключение для клиента Zumic."""

    pass


class AuthenticationError(ZumicError):
    """Ошибка аутентификации при подключении к Zumic."""

    pass


class ConnectionError(ZumicError):
    """Ошибка соединения с сервером Zumic."""

    pass


class ResponseError(ZumicError):
    """Сервер вернул некорректный ответ."""

    pass


class InvalidResponse(ZumicError):
    """Ответ сервера невозможно разобрать или он нарушает протокол."""

    pass


class DataError(ZumicError):
    """Ошибка в переданных/полученных данных (например, тип данных не поддерживается)."""

    pass


class PubSubError(ZumicError):
    """Ошибка, связанная с Pub/Sub."""

    pass


class WatchError(ZumicError):
    """Ошибка при использовании механизма слежения (watch)."""

    pass
