import json

from loguru import logger

from pysamp import call_native_function


def cef_create_browser(
        player_id: int,
        browser_id: int,
        url: str,
        is_hidden: bool,
        is_focused: bool
) -> bool:
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
) -> bool:
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


def cef_emit_event(player_id: int, event_name: str, data: dict):
    if not isinstance(data, dict):
        logger.error(f'data must be a dict, not {type(data)}')
        return None

    return call_native_function(
        'cef_emit_event',
        player_id,
        event_name,
        (0, json.dumps(data or {}))
    )


def cef_subscribe(
        event_name: str,
        callback_name: str,
):
    return call_native_function(
        'cef_subscribe',
        event_name,
        callback_name,
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
        scale: float  # Not exactly.
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
