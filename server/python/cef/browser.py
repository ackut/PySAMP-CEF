from typing import Any, Callable

from .event_handler import EventHandler
from .exceptions import BrowserCreationError
from .natives import (cef_always_listen_keys, cef_create_browser,
                      cef_destroy_browser, cef_emit_event, cef_focus_browser,
                      cef_hide_browser, cef_load_url, cef_toggle_dev_tools)
from .registry import BrowserRegistry


class Browser:
    """browser_id == player_id"""

    def __init__(self, player_id: int):
        self.id = player_id
        self.url: str | None = None
        self.is_hidden: bool = False
        self.is_focused: bool = False

    @classmethod
    def create(
        cls,
        player_id: int,
        url: str,
        is_hidden: bool = False,
        is_focused: bool = False,
    ) -> 'Browser':
        result = cef_create_browser(
            player_id=player_id,
            browser_id=player_id,
            url=url,
            is_hidden=is_hidden,
            is_focused=is_focused,
        )

        if result == 0:
            raise BrowserCreationError(
                f'Failed to create browser for player {player_id}'
            )

        browser = cls(player_id)
        browser.url = url
        browser.is_hidden = is_hidden
        browser.is_focused = is_focused
        BrowserRegistry.add(browser)
        return browser

    @classmethod
    def on(cls, event: str) -> Callable:
        return EventHandler.subscribe(event)

    def destroy(self) -> bool:
        if BrowserRegistry.remove(self):
            cef_destroy_browser(self.id, self.id)
            return True
        return False

    def emit(self, event_name: str, data: dict | None = None) -> Any:
        return cef_emit_event(self.id, event_name, data)

    def set_visibility(self, visible: bool = True) -> Any:
        return cef_hide_browser(self.id, self.id, not visible)

    def set_focus(self, focus: bool = True) -> Any:
        return cef_focus_browser(self.id, self.id, focus)

    def load_url(self, url: str) -> Any:
        return cef_load_url(self.id, self.id, url)

    def set_always_listen_keys(self, listen: bool = True) -> Any:
        return cef_always_listen_keys(self.id, self.id, listen)

    def set_dev_tools(self, status: bool) -> Any:
        return cef_toggle_dev_tools(self.id, self.id, status)
