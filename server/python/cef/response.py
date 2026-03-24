from pydantic import BaseModel


class BrowserResponse:
    def __init__(
        self,
        success: bool,
        data: dict | None = None,
        error: str | None = None,
    ) -> None:
        self._success = success
        self._data = data
        self._error = error

    @classmethod
    def ok(cls, data: dict | None = None) -> 'BrowserResponse':
        return cls(success=True, data=data)

    @classmethod
    def error(cls, message: str) -> 'BrowserResponse':
        return cls(success=False, error=message)

    def to_dict(self) -> dict:
        result = {'success': self._success}

        if self._data is not None:
            if isinstance(self._data, BaseModel):
                result['data'] = self._data.model_dump(mode='json')
            else:
                result['data'] = self._data

        if self._error is not None:
            result['error'] = self._error

        return result
