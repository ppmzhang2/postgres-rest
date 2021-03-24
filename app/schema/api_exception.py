from enum import Enum


class ErrorCategory(Enum):
    NOT_FOUND = 'record-not-found'
    DB = 'db-error'
    REQUEST_INVALID = 'invalid-request'
    OTHER = 'unexpected-error'


class ApiException(RuntimeError):
    __slots__ = ('_status_code', '_category', '_message')

    def __init__(
        self,
        status_code: int,
        category: ErrorCategory,
        message: str,
    ):
        self._status_code = status_code
        self._category = category
        self._message = message
        super().__init__(self._message)

    @property
    def status_code(self):
        return self._status_code

    @property
    def category(self):
        return self._category.value

    @property
    def message(self):
        return self._message
