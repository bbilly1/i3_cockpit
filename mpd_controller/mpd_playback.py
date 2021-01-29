""" handles the play interactions with mpd """
from time import sleep
import subprocess

def fade(way, current_vol, client):
    """ gracefull fading """
    if way == 'out':
        steps = int(current_vol / 2)
        amount = -2
    elif way == 'in':
        steps = 50
        amount = +2
    for _ in range(steps):
        client.volume(amount)
        sleep(0.03)


def toggle(client, signal_id):
    """ toggles play status """
    # setup
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
    # call pkill to refresh status bar
    subprocess.call(["pkill", "-RTMIN+" + str(signal_id), "i3blocks"])


def play_next(client):
    """ skip to next in playlist """
    client_status = client.status()
    current_vol = int(client_status['volume'])
    fade('out', current_vol, client)
    client.pause()
    client.setvol(current_vol)
    client.next()


def play_prev(client):
    """ skip to previous in playlist """
    client_status = client.status()
    current_vol = int(client_status['volume'])
    fade('out', current_vol, client)
    client.pause()
    client.setvol(current_vol)
    client.previous()
