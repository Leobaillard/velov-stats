#!/usr/bin/python

from __future__ import print_function
import sys
import requests
import socket
import json
import time
import pprint

from statsd import StatsClient

try:
    with open('./config.json') as config_file:
        config = json.load(config_file)
except:
    print("Can't load config file.")
    raise

def get_stations_data():
    stations_data = {}
    for station in config['jcd_stations']:
        print("Getting station #"+str(station))
        station_json = get_station_data(station)
        stations_data[station] = {}
        stations_data[station]['bike_stands'] = station_json.get('bike_stands', 0)
        stations_data[station]['available_bike_stands'] = station_json.get('available_bike_stands', 0)
        stations_data[station]['available_bikes'] = station_json.get('available_bikes', 0)

    return stations_data

def get_station_data(station_id):
    result = get_api_call("stations/"+str(station_id))
    return result

def get_api_call(api_func):
    api_url = config['jcd_apiurl'] + api_func + "?apiKey=" + config['jcd_apikey'] + "&contract=" + config['jcd_contract']
    try:
        data = requests.get(api_url)
        if data.status_code == 200:
            return data.json()
        else:
            print("Error fetching data, creating graphite event")
            create_graphite_event("Error fetching API data (" + api_func +")", ["error"])
            return json.loads("{}")
    except:
        print("Error fetching data, creating graphite event")
        create_graphite_event("Error fetching API data (" + api_func +")", ["error"])
        return json.loads("{}")

def openstatsd():
    return StatsClient(host=socket.gethostbyname(config['statsd_host']),
                     port=config['statsd_port'],
                     prefix=config['graphite_node'])

def create_graphite_event(event_description, tags):
    required_data = "Event from velov stats"
    tags_string = " ".join(str(x) for x in tags)  # Since you will pass an array but graphite expects multi tags like "a,b,c" or "a b c"
    event = {"what": event_description, "tags": tags_string, "data": required_data}
    try:
        requests.post("http://"+config['graphite_host']+"/events/", data=json.dumps(event), timeout=15, verify=False)
    except Exception as exc:
        print('Error while creating graphite event:', exc, file=sys.stderr)

def main():
    statsd = openstatsd()

    while True:
        stations_data = get_stations_data()
        for station_id, station_data in stations_data.items():
            pprint.pprint(str(station_id) + ": "+str(station_data))
            statsd.gauge(str(station_id) + '.bike_stands', station_data['bike_stands'])
            statsd.gauge(str(station_id) + '.available_bike_stands', station_data['available_bike_stands'])
            statsd.gauge(str(station_id) + '.available_bikes', station_data['available_bikes'])

        # Sleep until next iteration
        print("Waiting "+ str(config['measure_interval']) + "s until next iteration...")
        time.sleep(config['measure_interval'])

if __name__ == '__main__':
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
