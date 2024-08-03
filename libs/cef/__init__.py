import json
from pysamp import (
    call_native_function,
    register_callback
)
from pysamp.event import event
from python.player import Player


def cef_create_browser(
        player_id: int,
        browser_id: int,
        url: str,
        is_hidden: bool,
        is_focused: bool
):
    return call_native_function(
        'cef_create_browser',
        player_id,
        browser_id,
        url,
        is_hidden,
        is_focused
    )


def cef_destroy_browser(
        player_id: int,
        browser_id: int
):
    return call_native_function(
        'cef_destroy_browser',
        player_id,
        browser_id
    )


def cef_hide_browser(
        player_id: int,
        browser_id: int,
        hide: bool
):
    return call_native_function(
        'cef_hide_browser',
        player_id,
        browser_id,
        hide
    )


def to_cef_type(value):
    for type_value, type_ref in enumerate([str, int, float]):
        if isinstance(value, type_ref):
            return type_value


def cef_emit_event(player_id: int, event_name: str, args: tuple):
    cef_args = []

    for arg in args:
        cef_type = to_cef_type(arg)
        if cef_type is None:
            raise ValueError(f'Invalid CEF type: {type(arg).__name__}')
        cef_args.extend([cef_type, arg])

    return call_native_function(
        'cef_emit_event',
        player_id,
        event_name,
        tuple(cef_args)
    )


def cef_subscribe(
        event_name: str,
        callback
):
    return call_native_function(
        'cef_subscribe',
        event_name,
        callback
    )


def cef_player_has_plugin(
        player_id: int
):
    return call_native_function(
        'cef_player_has_plugin',
        player_id
    )


def cef_create_ext_browser(
        player_id: int,
        browser_id: int,
        texture: str,
        url: str,
        scale: float  # Не точно.
):
    return call_native_function(
        'cef_create_ext_browser',
        player_id,
        browser_id,
        texture,
        url,
        scale
    )


def cef_append_to_object(
        player_id: int,
        browser_id: int,
        object_id: int
):
    return call_native_function(
        'cef_append_to_object',
        player_id,
        browser_id,
        object_id
    )


def cef_remove_from_object(
        player_id: int,
        browser_id: int,
        object_id: int
):
    return call_native_function(
        'cef_remove_from_object',
        player_id,
        browser_id,
        object_id
    )


def cef_toggle_dev_tools(
        player_id: int,
        browser_id: int,
        status: bool
):
    return call_native_function(
        'cef_toggle_dev_tools',
        player_id,
        browser_id,
        status
    )


def cef_set_audio_settings(
        player_id: int,
        browser_id: int,
        max_distance: float,
        reference_distance: float
):
    return call_native_function(
        'cef_set_audio_settings',
        player_id,
        browser_id,
        max_distance,
        reference_distance
    )


def cef_focus_browser(
        player_id: int,
        browser_id: int,
        focused: bool
):
    return call_native_function(
        'cef_focus_browser',
        player_id,
        browser_id,
        focused
    )


def cef_always_listen_keys(
        player_id: int,
        browser_id: int,
        listen: bool
):
    return call_native_function(
        'cef_always_listen_keys',
        player_id,
        browser_id,
        listen
    )


def cef_load_url(
        player_id: int,
        browser_id: int,
        url: str
):
    return call_native_function(
        'cef_load_url',
        player_id,
        browser_id,
        url
    )


def cef_on_player_connect(
    player_id: int,
    player_ip: str
):
    return call_native_function(
        'cef_on_player_connect',
        player_id,
        player_ip
    )


class Browser:
    _pool: dict = {}

    def __init__(self, player_id: int) -> None:
        _cls = self._pool[player_id]
        self.player_id: int = player_id
        self.url: str = _cls[0]
        self.hidden: bool = _cls[1]
        self.focused: bool = _cls[2]

    @classmethod
    def create(cls, player_id: int, url: str, hidden: bool, focused: bool) -> "Browser":
        cls._pool[player_id] = [url, hidden, focused]
        cef_create_browser(player_id, player_id, url, hidden, focused)
        register_callback('on_browser_created', 'is')
        cef_subscribe('cef:browser:created', 'on_browser_created')
        return cls(player_id)

    @event('on_browser_created')
    def on_created(cls, player_id: int, args: str):
        return cls(player_id), args

    def hide(self, hide: bool = True) -> None:
        cef_hide_browser(self.player_id, self.player_id, hide)
    
    def focus(self, focus: bool = True) -> None:
        cef_focus_browser(self.player_id, self.player_id, focus)

    def load_url(self, url: str) -> None:
        cef_load_url(self.player_id, self.player_id, url)

    def emit(self, event: str, *args):
        cef_emit_event(self.player_id, event, (json.dumps(list(args)),))
    

# @Browser.on_response
# def asd(player_id: int, args):
#     print(f'browser response from func: {player_id, args}')


def OnCefInitialize(player_id: int, success: int):
    if not success:
        print(f'[CEF] Failed initialize. (player_id: {player_id})')
        return Player(player_id).kick()

    Browser.create(player_id, 'http://localhost:5173/', False, False)


def OnCefBrowserCreated(player_id: int, browser_id: int, status_code: int):
    if status_code != 200:
        print(f'[CEF] Failed create browser.')
        print(f'[CEF] player_id: {player_id}, browser_id: {browser_id}, status_code: {status_code}')
        return Player(player_id).kick()

    # cef_toggle_dev_tools(player_id, browser_id, True)


register_callback('OnCefInitialize', 'ii')
register_callback('OnCefBrowserCreated', 'iii')
