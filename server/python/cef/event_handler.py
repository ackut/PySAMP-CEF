import json
from functools import wraps
from inspect import signature
from typing import TYPE_CHECKING, Any, Callable, Optional

from loguru import logger
from pydantic import BaseModel, ValidationError

from pysamp import register_callback

from .exceptions import (BrowserNotFoundInRegistry, EventDataTypeMismatch,
                         EventDataValidationError, FailedParseEventData)
from .natives import cef_subscribe
from .registry import BrowserRegistry
from .response import BrowserResponse

if TYPE_CHECKING:
    from .browser import Browser


class EventHandler:
    @classmethod
    def subscribe(cls, event_name: str) -> Callable:
        def decorator(func: Callable):
            register_callback(func.__name__, 'is')
            cef_subscribe(event_name, func.__name__)

            @wraps(func)
            def wrapper(browser_id: int, json_string: str):
                browser = BrowserRegistry.get(browser_id)
                if browser is None:
                    raise BrowserNotFoundInRegistry(f'{browser_id=}')

                data = cls._parse_event_data(json_string)
                if data is None:
                    return None

                request_id: str | None = data.get('_requestId')

                try:
                    result = cls._call_handler(func, browser, data)
                except Exception as e:
                    logger.exception(
                        f'Error in event handler "{func.__name__}": {e}'
                    )

                    if request_id:
                        cls._send_error_response(browser, request_id, str(e))

                    return None

                if request_id:
                    cls._send_response(browser, request_id, result)

                return result
            return wrapper
        return decorator

    @staticmethod
    def _parse_event_data(json_string: str) -> Optional[dict]:
        if not json_string:
            return None

        try:
            data = json.loads(json_string)
        except json.JSONDecodeError:
            raise FailedParseEventData(f'Invalid JSON: {json_string}')

        if not isinstance(data, dict):
            raise EventDataTypeMismatch(f'Expected dict, got {type(data)}')

        return data

    @staticmethod
    def _call_handler(func: Callable, browser: 'Browser', data: dict) -> Any:
        sig = signature(func)
        params = list(sig.parameters.values())
        if len(params) == 1:
            return func(browser)

        if len(params) < 2:
            return func(browser, data)

        param_annotation = params[1].annotation
        if isinstance(param_annotation, type) and issubclass(param_annotation, BaseModel):
            clean_data = {k: v for k, v in data.items() if k != '_requestId'}

            try:
                validated_data = param_annotation.model_validate(clean_data)
            except ValidationError as e:
                raise EventDataValidationError(f'Validation error: {e.json()}')

            return func(browser, validated_data)
        else:
            return func(browser, data)

    @staticmethod
    def _send_response(browser: 'Browser', request_id: str, result: Any) -> None:
        if isinstance(result, BrowserResponse):
            response = result
        elif isinstance(result, BaseModel):
            response = BrowserResponse.ok(result.model_dump())
        else:
            response = BrowserResponse.ok(result)

        payload = response.to_dict()
        payload['_requestId'] = request_id
        ret = browser.emit('cef::response', payload)

    @staticmethod
    def _send_error_response(browser: 'Browser', request_id: str, message: str) -> None:
        payload = BrowserResponse.error(message).to_dict()
        payload['_requestId'] = request_id
        browser.emit('cef::response', payload)
