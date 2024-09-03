import time
from pysamp.player import Player
from python.cef import Browser, cef_subscribe, register_callback


def server_to_cef(player: Player, *args):
    browser = Browser(player.id)
    browser.emit('in:cef:event:name', f'Hello from server! Timestamp: {args[0]}')


@Browser.using_pool
def cef_to_server(browser: Browser, arg_1: str, arg_2: int):
    player = Player(browser.id)
    player.send_client_message(-1, f'Hello from cef: {arg_1}, {arg_2}')
    print(f'Hello from cef: {arg_1}, {arg_2}')
    server_to_cef(player, time.time())


register_callback('cef_to_server', 'is')
cef_subscribe('in:server:callback:name', 'cef_to_server')
