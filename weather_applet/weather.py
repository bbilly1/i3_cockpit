#!/usr/bin/env python3
""" queries openweathermap to get weather data """

import os
import sys
import configparser
import subprocess
from time import sleep
from datetime import datetime

import requests


iconlist = {
    '01d': '',
    '02d': '',
    '03d': '',
    '04d': '',
    '09d': '',
    '10d': '',
    '11d': '',
    '13d': '',
    '50d': '🌫',
    '01n': '',
    '02n': '',
    '03n': '',
    '04n': '',
    '09n': '',
    '10n': '',
    '11n': '',
    '13n': '',
    '50n': '🌫'
}


def get_config(config_path):
    """ read out the .env file and return config values """
    # parse
    config_parser = configparser.ConfigParser()
    config_parser.read(config_path)
    # return false on error
    if config_parser.options('api') == ['openweathermap_api_key', 'lat', 'lon', 'unit']:
        api_key = config_parser.get('api', 'openweathermap_api_key')
        lat = config_parser.get('api', 'lat')
        lon = config_parser.get('api', 'lon')
        unit = config_parser.get('api', 'unit')
    else:
        print('config parse error')
        return False
    return api_key, lat, lon, unit


def get_data(api_key, lat, lon, unit):
    """ get celsius and icon_id based on lat and lon """
    url = "https://api.openweathermap.org/data/2.5/weather?&units=" + unit \
        + "&appid=" + api_key + "&lat=" + lat + "&lon=" + lon
    # try up to 3 times
    for i in range(1, 4):
        try:
            response = requests.get(url, timeout=5)
        except:
            sleep(int(i) * 30)
        else:
            break
    # parse response
    json = response.json()
    celsius = round(json['main']['temp'])
    celsius_pretty = str(celsius) + "°"
    icon_id = json['weather'][0]['icon']
    icon = iconlist.get(icon_id)
    # return
    return celsius_pretty, icon


def get_forecast(api_key, lat, lon, unit):
    """ get next three days forecast """
    # get data
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lon \
        + "&units=" + unit + "&exclude=current,minutely,hourly,alerts&appid=" + api_key
    response = requests.get(url, timeout=5)
    json = response.json()
    notify_list = []
    # loop three days
    for i in json['daily'][1:4]:
        timestamp = i['dt']
        date_clean = datetime.fromtimestamp(timestamp).strftime("%a %Y-%m-%d")
        min_temp = i['temp']['min']
        max_temp = i['temp']['max']
        weather = i['weather'][0]['main']
        weather_desc = i['weather'][0]['description']
        icon_id = i['weather'][0]['icon']
        icon = iconlist.get(icon_id)
        first_line = f'{date_clean} {icon} {weather}'
        second_line = f'min: {min_temp} max: {max_temp}, {weather_desc}\n'
        notify_list.append(first_line)
        notify_list.append(second_line)
    # output with notify-send
    message = "\n".join(notify_list)
    subprocess.call(['notify-send', 'Three days forecast:', message])


def main():
    """ main function to run """
    # make the call
    celsius_pretty, icon = get_data(api_key, lat, lon, unit)
    # print three lines for i3blocks
    print(icon, celsius_pretty)
    print(icon, celsius_pretty)
    print()


# start from here
if __name__ == '__main__':
    # get config file path relative to script file
    config_path = os.path.dirname(sys.argv[0]) + '/config'
    api_key, lat, lon, unit = get_config(config_path)
    # check for button clicked
    env = os.environ.copy()
    button = env.get('BLOCK_BUTTON', False)
    if button == '1':
        get_forecast(api_key, lat, lon, unit)
    # regular
    main()
