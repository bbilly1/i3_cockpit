#!/usr/bin/env python3
# https://python-mpd2.readthedocs.io/en/latest
# https://dunst-project.org/documentation/

import sys
from mpd import MPDClient

import mpd_playback
import mpd_state

signal_id = 11
cover_art_temp = '/tmp/mpd_cover_art_temp.jpg'

arguments = sys.argv

if len(arguments) == 1:
    mpc_command = 'state'
elif len(arguments) == 2:
    mpc_command = arguments[1]


def main():
    # connect
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
    except ConnectionRefusedError:
        # mpd is not running, stop here
        return
    # follow mpc_command
    if mpc_command == 'toggle':
        mpd_playback.toggle(client, signal_id)
    elif mpc_command == 'next':
        mpd_playback.play_next(client)
    elif mpc_command == 'prev':
        mpd_playback.play_prev(client)
    elif mpc_command == 'state':
        mpd_state.get_state(client, cover_art_temp)
    # close connection
    client.close()
    client.disconnect()


# lunch from here
if __name__ == '__main__':
    main()
