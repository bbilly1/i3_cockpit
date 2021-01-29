#!/usr/bin/env python3
""" queries openweathermap to get weather data """

import os
import sys
import configparser
from time import sleep

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
    if config_parser.options('api') == ['openweathermap_api_key', 'lat', 'lon']:
        api_key = config_parser.get('api', 'openweathermap_api_key')
        lat = config_parser.get('api', 'lat')
        lon = config_parser.get('api', 'lon')
    else:
        print('config parse error')
        return False
    return api_key, lat, lon


def get_data(api_key, lat, lon):
    """ get celsius and icon_id based on lat and lon """
    url = "https://api.openweathermap.org/data/2.5/weather?&units=metric&appid=" \
        + api_key + "&lat=" + lat + "&lon=" + lon
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


def main():
    """ main function to run """
    # get config file path relative to script file
    config_path = os.path.dirname(sys.argv[0]) + '/config'
    api_key, lat, lon = get_config(config_path)
    # make the call
    celsius_pretty, icon = get_data(api_key, lat, lon)
    # print three lines for i3blocks
    print(icon, celsius_pretty)
    print(icon, celsius_pretty)
    print()


# start from here
if __name__ == '__main__':
    main()
