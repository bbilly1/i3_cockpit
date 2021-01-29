#!/usr/bin/env python3
"""
Main file to handle mpd controll.
Will read argument passed to script to figure
out what to do with it.
docs:
- https://python-mpd2.readthedocs.io/en/latest
- https://dunst-project.org/documentation/
"""

import sys
import subprocess
from mpd import MPDClient

import mpd_playback
import mpd_state


def get_conf():
    """ setting up variables """
    arguments = sys.argv
    signal_id = 11
    cover_art_path = '/tmp/mpd_cover_art_temp.jpg'
    if len(arguments) == 1:
        mpc_command = 'state'
    elif len(arguments) == 2:
        mpc_command = arguments[1]
    return mpc_command, cover_art_path, signal_id


def main():
    """
    establish connection to daemon
    then process the command and disconnect at end
    """
    mpc_command, cover_art_path, signal_id = get_conf()
    client = MPDClient()
    # try to connect, if error try to start daemon
    try:
        client.connect("localhost", 6600)
    except ConnectionRefusedError:
        # mpd is not connecting, try to start
        if mpc_command == 'toggle':
            output = subprocess.run(["mpd"], capture_output=True, check=False)
            if output.returncode == 0:
                # connect
                client.connect("localhost", 6600)
            else:
                # that failed, all is lost
                return
    # follow mpc_command
    if mpc_command == 'toggle':
        mpd_playback.toggle(client, signal_id)
    elif mpc_command == 'next':
        mpd_playback.play_next(client)
    elif mpc_command == 'prev':
        mpd_playback.play_prev(client)
    elif mpc_command == 'state':
        mpd_state.get_state(client, cover_art_path)
    # disconnect connection
    client.disconnect()


# lunch from here
if __name__ == '__main__':
    main()
