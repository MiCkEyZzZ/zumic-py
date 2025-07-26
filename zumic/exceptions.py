class ZumicError(Exception):
    pass
class AuthenticationError(ZumicError):
    pass
class ConnectionError(ZumicError):
    pass
class ResponseError(ZumicError):
    pass
class InvalidResponse(ZumicError):
    pass
