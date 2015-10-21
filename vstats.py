#!/usr/bin/python

import requests
import json
import pprint

# https://api.jcdecaux.com/vls/v1/stations?contract=Lyon&apiKey=7c425537bc03a2620296456ff99d391e5ce167ed
JCD_APIKEY      = ""
JCD_APIURL      = "https://api.jcdecaux.com/vls/v1/"
JCD_CONTRACT    = "Lyon"
JCD_STATIONS    = [6035,6036,6037,6041,6042,6043]

def get_stations_data():
    stations_data = {}
    for station in JCD_STATIONS:
        station_json = get_station_data(station)
        stations_data[str(station)] = {}
        stations_data[str(station)]['total'] = station_json['bike_stands']
        stations_data[str(station)]['bikes'] = station_json['available_bike_stands']
        stations_data[str(station)]['free'] = station_json['available_bikes']

    return stations_data

def get_station_data(station_id):
    result = get_api_call("stations/"+str(station_id))
    return result

def get_api_call(api_func):
    api_url = JCD_APIURL + api_func + "?apiKey=" + JCD_APIKEY + "&contract=" + JCD_CONTRACT
    data = requests.get(api_url)
    if data.status_code == 200:
        return data.json()
    else:
        return "{}"

if __name__ == '__main__':
    pprint.pprint(get_stations_data())
