#!/usr/bin/env python3
""" parses /proc/loadavg for i3blocks """

import sys

load_field_arg = sys.argv[1]
THREADS = 8

def get_load():
    """ returns list of load avg fields """
    with open('/proc/loadavg', 'r') as load_avg:
        load = load_avg.readline().strip()
    load_line = load.split()[:3]
    load_line_float = [float(i) for i in load_line]
    return load_line_float


def main(load_field):
    """ main to run """
    print_main = ""
    print_small = ""
    print_color = ""
    # read proc
    load_line_float = get_load()
    load_1, load_5, load_15 = load_line_float
    # load avg
    if load_field == str(1):
        load = load_1
        load_string = format(load, '.2f')
        print_small = f'{load_field}: {load_string}'
        print_color = "#ffffff"
    elif load_field == str(5):
        load = load_5
    elif load_field == str(15):
        load = load_15
    # colors
    if 6 < load <= 10:
        print_color = "#ffff00"
    elif load > 10:
        print_color = "#ff0000"
    load_string = format(load, '.2f')
    print_main = f'{load_field}: {load_string}'
    print(print_main)
    print(print_small)
    print(print_color)


if __name__ == '__main__':
    main(load_field_arg)
