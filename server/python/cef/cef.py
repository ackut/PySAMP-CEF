from pysamp import register_callback
from pysamp.event import event

from .browser import Browser
from .natives import cef_on_player_connect
from .registry import BrowserRegistry


class CEF:
    @staticmethod
    def init(player_id: int, player_ip: str) -> None:
        return cef_on_player_connect(player_id, player_ip)

    @staticmethod
    def register_callbacks() -> None:
        register_callback('OnCefInitialize', 'ii')
        register_callback('OnCefBrowserCreated', 'iii')

    @event('OnCefInitialize')
    def on_init(cls, player_id: int, success: int) -> tuple[int, bool]:
        return player_id, bool(success)

    @event('OnCefBrowserCreated')
    def on_browser_created(cls, player_id: int, browser_id: int, status_code: int) -> tuple[Browser, int]:
        return BrowserRegistry.get(player_id), status_code
