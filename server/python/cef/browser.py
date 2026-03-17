import json
from functools import wraps
from typing import Callable, Optional

from loguru import logger

from pysamp import register_callback
from pysamp.event import event

from .natives import *


class Browser:
    _pool: dict[int, 'Browser'] = {}  # player_id: Browser

    def __init__(self, player_id: int) -> None:
        self.id: int = player_id
        self.url: str | None = None
        self.is_hidden: bool = False
        self.is_focused: bool = False

    @classmethod
    def is_in_pool(cls, browser_id: int) -> bool:
        return browser_id in cls._pool

    @classmethod
    def from_pool(cls, player_id: int) -> Optional['Browser']:
        return cls._pool.get(player_id)

    @classmethod
    def remove_from_pool(cls, player_id: int) -> None:
        if player_id in cls._pool:
            del cls._pool[player_id]

    @classmethod
    def with_pool(cls, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(browser_id: int, json_string: str):
            browser = cls.from_pool(browser_id)
            if not browser:
                logger.warning(f'[Browser] {browser_id=} not found in pool')
                return None

            try:
                data = json.loads(json_string)
            except json.JSONDecodeError:
                logger.error(f'[Browser] Invalid JSON: {json_string}')
                return None

            if not isinstance(data, dict):
                logger.error(
                    f'[Browser] Event data is not dict. data={data}, type={type(data)}'
                )
                return None

            return func(browser, data)
        return wrapper

    @classmethod
    def create(
        cls,
        player_id: int,
        url: str,
        is_hidden: bool = False,
        is_focused: bool = False,
    ) -> Optional['Browser']:
        if cls.is_in_pool(player_id):
            return None

        result = cef_create_browser(
            player_id=player_id,
            browser_id=player_id,
            url=url,
            is_hidden=is_hidden,
            is_focused=is_focused,
        )

        # NOTE: Creating a browser does not mean that the URL has opened.
        if result == 0:
            logger.error(f'[Browser]: Failed to create for {player_id=}')
            return None

        browser = cls(player_id)
        browser.url = url
        browser.is_hidden = is_hidden
        browser.is_focused = is_focused

        cls._pool[player_id] = browser

        logger.debug(f'[Browser] Created for {player_id=}')
        return browser

    @classmethod
    def init_cef(cls, player_id: int, player_ip: str) -> None:
        return cef_on_player_connect(player_id, player_ip)

    @classmethod
    def on(cls, event: str) -> Callable:
        def decorator(func):
            register_callback(func.__name__, 'is')
            cef_subscribe(event, func.__name__)

            logger.debug(
                f'[Browser] Event "{event}" -> "{func.__name__}"'
            )

            return cls.with_pool(func)
        return decorator

    def destroy(self) -> bool:
        if not self.is_in_pool(self.id):
            return False

        cef_destroy_browser(self.id, self.id)
        self.remove_from_pool(self.id)
        return True

    def emit(self, event: str, data: dict | None = None) -> bool:
        return cef_emit_event(self.id, event, data)

    def set_visibility(self, visible: bool = True) -> bool:
        return cef_hide_browser(self.id, self.id, not visible)

    def set_focus(self, focus: bool = True) -> bool:
        return cef_focus_browser(self.id, self.id, focus)

    def load_url(self, url: str) -> bool:
        return cef_load_url(self.id, self.id, url)

    def set_always_listen_keys(self, always: bool = True) -> bool:
        return cef_always_listen_keys(self.id, self.id, always)

    def set_dev_tools(self, status: bool) -> bool:
        return cef_toggle_dev_tools(self.id, self.id, status)

    @event('OnCefInitialize')
    def on_cef_init(cls, player_id: int, success: int):
        return player_id, bool(success)

    @event('OnCefBrowserCreated')
    def on_created(cls, player_id: int, browser_id: int, status_code: int) -> None:
        return cls.from_pool(player_id), status_code


register_callback('OnCefInitialize', 'ii')
register_callback('OnCefBrowserCreated', 'iii')
