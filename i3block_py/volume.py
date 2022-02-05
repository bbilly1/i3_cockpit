#!/usr/bin/env python3
""" 
handler for media keys 
integrated with pipewire by parsing pactl
"""

import subprocess
import sys
from time import sleep

# signal id to update i3blocks
I3BLOCKS_SIGNAL_ID = 10


def get_status():
    """ returns the activ sink pased in a dict """
    # get list of sinks
    state = subprocess.run(["pactl", "list", "sinks"], capture_output=True)
    state_str = state.stdout.decode()
    sinks = state_str.split('\n\n')
    # loop through sinks
    sinks_dict_list = []
    for sink in sinks:
        sink_lines = sink.split('\n')
        # build sink dict
        sink_dict = {}
        for i in sink_lines:
            if ':' in i:
                key, value = i.split(':', maxsplit=1)
            elif '=' in i:
                key, value = i.split('=')
            else:
                continue
            key = key.strip().lower()
            value = value.strip().strip('"')
            if value:
                sink_dict[key] = value
        # append to list
        sinks_dict_list.append(sink_dict)
    # find active
    if len(sinks_dict_list) == 1:
        activ_sink = sinks_dict_list[0]
    else:
        for sink_dict in sinks_dict_list:
            sink_name = sink_dict['name']
            if 'bluez' in sink_name:
                activ_sink = sink_dict
                break
    # return activ
    return activ_sink


def get_vol(activ_sink):
    """ get the current volume level of activ sink """
    vol_string = activ_sink['volume']
    vol_list = [i for i in vol_string.split(' / ') if '%' in i]
    vol = int(vol_list[0].strip().strip('%'))
    return vol


def print_status(activ_sink):
    """ print status for i3 blocks """
    mute = activ_sink['mute']
    # based on sink
    if 'bluez' in activ_sink['name']:
        # bluetooth
        icon = ''
    elif activ_sink['active port'] == 'analog-output-headphones':
        # headphones
        icon = ''
    elif activ_sink['active port'] == 'analog-output-speaker':
        # speaker
        if mute == 'no':
            icon = ''
        else:
            icon = ''
    # color
    if mute == 'no':
        color = "#ffffff"
        vol = str(get_vol(activ_sink)) + '%'
    else:
        color = "#404040"
        vol = "MUTE"
    # print three lines
    print(f'{icon} {vol}')
    print(f'{icon}')
    print(color)


def mute(activ_sink):
    """ toggle mute of activ sink """
    sink_id = activ_sink['object.serial']
    subprocess.call(['pactl', 'set-sink-mute', sink_id, 'toggle'])


def vol_up(activ_sink):
    """ increase vol in 5% increments """
    sink_id = activ_sink['object.serial']
    vol = get_vol(activ_sink)
    # if uneven vol level
    if vol % 5 == 0:
        target_vol = vol + 5
    else:
        target_vol = vol + 5 - (vol % 5)
    # how many times to loop
    iterations = target_vol - vol
    for _ in range(iterations):
        subprocess.call(['pactl', 'set-sink-volume', sink_id, '+1%'])
        sleep(0.1)


def vol_down(activ_sink):
    """ decrese vol in 5% increments """
    sink_id = activ_sink['object.serial']
    vol = get_vol(activ_sink)
    # if uneven vol level
    if vol % 5 == 0:
        target_vol = vol - 5
    else:
        target_vol = vol - (vol % 5)
    # how many times to loop
    iterations = vol - target_vol
    for _ in range(iterations):
        subprocess.call(['pactl', 'set-sink-volume', sink_id, '-1%'])
        sleep(0.1)


def main():
    """ main to run """
    # parse args
    args = sys.argv
    activ_sink = get_status()
    # if args
    if len(args) > 1:
        arg = args[1]
        if arg == 'vol_up':
            vol_up(activ_sink)        
        elif arg == 'vol_down':
            vol_down(activ_sink)
        elif arg == 'mute':
            mute(activ_sink)
        activ_sink = get_status()
        subprocess.call(['pkill', '-RTMIN+' + str(I3BLOCKS_SIGNAL_ID), 'i3blocks'])
    # status
    print_status(activ_sink)


if __name__ == '__main__':
    main()
