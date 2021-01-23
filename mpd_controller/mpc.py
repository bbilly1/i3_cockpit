#!/usr/bin/env python3
# https://python-mpd2.readthedocs.io/en/latest

import sys
from mpd import MPDClient
from time import sleep


def fade(way, current_vol, client):
    """ gracefull fading """
    if way == 'out':
        steps = int(current_vol / 2)
        amount = -2
    elif way == 'in':
        steps = 50
        amount = +2
    for i in range(steps):
        client.volume(amount)
        sleep(0.03)


def mpc_toggle():
    """ toggles play status """
    client = MPDClient()
    client.connect("localhost", 6600)
    client_status = client.status()
    # switch
    current_vol = int(client_status['volume'])
    if client_status['state'] == 'play':
        fade('out', current_vol, client)
        client.pause()
    elif client_status['state'] == 'pause':
        client.setvol(0)
        client.play()
        fade('in', current_vol, client)


def main():
    """ main parser for args """
    mpc_command = sys.argv[1]
    if mpc_command == 'toggle':
        mpc_toggle()


if __name__ == '__main__':
    main()
