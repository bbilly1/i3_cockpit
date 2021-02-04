#!/usr/bin/env python3
""" parses output of acpi to monitor battery status """

import subprocess

LOG_FILE_PATH = "/tmp/battery_status.log"


def get_acpi():
    """ get acpi data as a sting """
    acpi_raw = subprocess.run(["acpi"], capture_output=True, check=False)
    acpi_string = acpi_raw.stdout.decode().strip().split('\n')[0]
    return acpi_string


def parse_acpi(acpi):
    """ split acpi string into its parts """
    state_list = acpi.split(': ')[1].split(',')
    battery_state_list = [i.strip() for i in state_list]
    # catch different states
    if len(battery_state_list) == 2:
        # fully charged
        battery_state, battery_level = battery_state_list
        time_remaining = False
    elif len(battery_state_list) == 3:
        # not fully charged
        battery_state, battery_level, time_remaining = battery_state_list
        time_remaining = time_remaining.split()[0]
        time_remaining = parse_time(time_remaining)
    battery_level = battery_level.strip('%')
    return battery_state, battery_level, time_remaining


def parse_time(time_remaining):
    """ returns minutes remaing from 00:00:00 format if a string
    else parses minutes back to hh:mm """
    if isinstance(time_remaining, int):
        if time_remaining > 60:
            hour = int(str(time_remaining / 60).split('.')[0])
            minutes = time_remaining - ( hour * 60 )
            hour_c = str(hour).zfill(2)
            minutes_c = str(minutes).zfill(2)
            left = f'{hour_c}:{minutes_c}'
        else:
            minutes_c = str(time_remaining).zfill(2)
            left = f'00:{minutes_c}'
    else:
        time_list = time_remaining.split(':')
        time_list.reverse()
        # account for different length of str
        total_sec = int()
        for i in enumerate(time_list):
            position, value = [int(j) for j in i]
            sec = value * 60 ** position
            total_sec = total_sec + sec
        # normalize to minutes
        left = int(total_sec / 60)
    return left


def get_last_log(battery_state, time_remaining):
    """ parse log file and return new average min value """
    new_line = f'{battery_state} {time_remaining}'
    try:
        with open(LOG_FILE_PATH, 'r') as last_log_file:
            log_lines = last_log_file.readlines()
    except FileNotFoundError:
        # no log file on first run
        return time_remaining, new_line
    # get lines
    try:
        log_lines_clean = [i.strip() for i in log_lines]
        last_10 = [i.split() for i in log_lines_clean]
        min_list = [int(i[1]) for i in last_10[-2:]]
        min_list.append(time_remaining)
        # calc avg
        avg_min = int(sum(min_list) / len(min_list))
    except ValueError:
        # something went wrong, reset log file
        return time_remaining, new_line
    return avg_min, last_10


def write_log(last_10, battery_state, new_avg_min):
    """ update the log file """
    state_changed = False
    if isinstance(last_10[0], type('str')):
        log_list = [battery_state, str(new_avg_min)]
        log_string = ' '.join(log_list)
    elif last_10[-1][0] == battery_state:
        # last state is same as current state
        last_10.append([battery_state, str(new_avg_min)])
        log_list = last_10[-10:]
        log_string = '\n'.join([' '.join(i) for i in log_list])
    else:
        # state changed replace log file
        if battery_state == 'Full':
            new_avg_min = 0
        log_string = f'{battery_state} {new_avg_min}'
        state_changed = True
    # write to log file
    with open(LOG_FILE_PATH, 'w') as log_file:
        log_file.write(log_string + '\n')
    return state_changed


def print_status(battery_state, battery_level, avg_min, state_changed):
    """ will print three lines for i3blocks """
    print_main = ""
    print_small = ""
    print_color = ""
    battery_level_int = int(battery_level)
    left = parse_time(avg_min)
    if battery_state == 'Discharging':
        if battery_level_int <= 20:
            icon = ""
            print_main = "<span background=\'#E53935\'>  $battery_level_int% $left</span>"
            print_main = f'<span background=\'#E53935\'>{icon}  {battery_level_int}% {left}</span>'
            print_color = "#ffffff"
        elif 20 < battery_level_int <= 25:
            icon = ""
            print_main = f'{icon}  {battery_level_int}% {left}'
            print_color = "#ff0000"
        elif 25 < battery_level_int <= 40:
            icon = ""
            print_main = f'{icon}  {battery_level_int}% {left}'
            print_color = "#ffff00"
        elif 40 < battery_level_int <= 70:
            icon = ""
            print_main = f'{icon}  {battery_level_int}% {left}'
        elif 70 < battery_level_int <= 90:
            icon = ""
            print_main = f'{icon}  {battery_level_int}% {left}'
        else:
            icon = ""
            print_main = f'{icon}  {battery_level_int}% {left}'
    elif battery_state == 'Charging':
        icon = "⚡"
        print_main = f'{icon}  {battery_level_int}% {left}'
        print_small = f'{icon}  {battery_level_int}%'
        if battery_level_int <= 20:
            print_color = "#E53935"
        else:
            print_color = "#ffffff"
    else:
        # full
        icon = "⚡"
        print_main = f'{icon}  {battery_level_int}%'
        print_small = f'{icon}'
    if state_changed:
        subprocess.call(["notify-send", f'{icon} {battery_state}'])
    # print
    print(print_main)
    print(print_small)
    print(print_color)


def main():
    """ main to run """
    acpi = get_acpi()
    battery_state, battery_level, time_remaining = parse_acpi(acpi)
    new_avg_min, last_10 = get_last_log(battery_state, time_remaining)
    state_changed = write_log(last_10, battery_state, new_avg_min)
    print_status(battery_state, battery_level, new_avg_min, state_changed)


if __name__ == '__main__':
    main()
