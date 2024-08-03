import samp
from pysamp import *
from python.player import Player
from python.libs.cef import *


samp.config(encoding='cp1251')


@on_gamemode_init
def on_init():
    set_game_mode_text('Project')
    add_player_class(0, 258.22296142578, 2926.1264648438, 1.78125, 178.83819580078, -1, -1, -1, -1, -1, -1)
    show_player_markers(1)
    show_name_tags(True)
    set_name_tag_draw_distance(40)
    enable_stunt_bonus_for_all(False)
    disable_interior_enter_exits()
    set_weather(0)


@Player.on_connect
@Player.using_pool
def on_player_connect(player: Player):
    cef_on_player_connect(player.get_id(), player.get_ip())
