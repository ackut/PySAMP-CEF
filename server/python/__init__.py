import samp  # type: ignore

from pysamp import on_gamemode_init, set_game_mode_text
from pysamp.player import Player

from python.cef.browser import Browser

samp.config(encoding='cp1251')


@on_gamemode_init
def on_init():
    set_game_mode_text('PySAMP-CEF')


@Player.on_connect
def on_player_connect(player: Player) -> None:
    player.toggle_controllable(False)
    player.toggle_spectating(True)

    Browser.init_cef(player.id, player.get_ip())


@Player.on_disconnect
def on_player_disconnect(player: Player, reason: int) -> None:
    Browser.remove_from_pool(player.id)


@Browser.on_cef_init
def on_browser_cef_init(player_id: int, success: bool) -> None:
    player = Player(player_id)

    if not success:
        print(f'[CEF] Failed init for {player.get_name()}')
        player.kick()

    Browser.create(
        player_id=player_id,
        url='http://localhost:5173/',
        is_hidden=False,
        is_focused=True,
    )


@Browser.on_created
def on_browser_created(browser: Browser, status_code: int) -> None:
    player = Player(browser.id)

    if status_code != 200:
        print(f'[Browser] Creation failed with {status_code=}')
        player.kick()
        return

    browser.set_dev_tools(True)


@Browser.on('cef:test')
def test_cef_handler(browser: Browser, data: dict) -> None:
    print(f'test_cef_handler: {browser.id=}, {data=}')
    browser.emit('cef:test', data)
