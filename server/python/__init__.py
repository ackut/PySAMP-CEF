import samp
from pysamp import *
from pysamp.player import Player
from python.cef import *
from python.res.test import cef_to_server


@on_gamemode_init
def on_init():
    set_game_mode_text('PySAMP-CEF')
    add_player_class(0, -65.791076660156, -10.221571922302, 3.1171875, 80.406448364258, -1, -1, -1, -1, -1, -1)
    enable_stunt_bonus_for_all(False)
    disable_interior_enter_exits()
    set_weather(0)


@Player.on_connect
def on_player_connect(player: Player):
    cef_on_player_connect(player.get_id(), player.get_ip())
