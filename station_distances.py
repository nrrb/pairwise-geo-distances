from time import sleep
import json
import csv
import re
import requests
from omgsecrets import MAPQUEST_APP_KEY

DIVVY_STATIONS_URL = 'http://divvybikes.com/stations/json'
MAPQUEST_URL = 'http://open.mapquestapi.com/directions/v2/routematrix?key={appkey}'

def distance(latlong1, latlong2):
    """
    The parameters should each be a dictionary with keys 'latitude'
    and 'longitude' and values are floats. For example, 
    {'latitude': 41.9325, 'longitude': -87.652681}
    """
    request_body = {
            'locations': [
                {'latLng': {'lat': latlong1['latitude'], 'lng': latlong1['longitude']}},
                {'latLng': {'lat': latlong2['latitude'], 'lng': latlong2['longitude']}}
                ]
            }
    r = requests.post(MAPQUEST_URL.format(appkey=MAPQUEST_APP_KEY),
                data=json.dumps(request_body)
            )
    if r.status_code != 200:
        # We didn't get a response from Mapquest
        return -1
    result = json.loads(r.content)
    try:
        distance = result['distance'][1]
    except IndexError, KeyError:
        # We didn't get the response we expected from MapQuest
        return -1
    return distance

if __name__ == "__main__":
    r = requests.get(DIVVY_STATIONS_URL)
    if r.status_code != 200:
        print("ERROR: Couldn't get the station list from Divvy Bikes.")
        exit(1)

    station_data = json.loads(r.content)
    stations = station_data['stationBeanList']

    f = open('station_distances.csv', 'wb')
    csvwriter = csv.writer(f)
    csvwriter.writerow(['stationName1', 'stationName2', 'distance (miles)'])
    for station1 in stations:
        for station2 in stations:
            # Skip this iteration if the stations are the same
            if station1['stationName'] == station2['stationName']:
                continue
            # If the pair (station1, station2) has already been checked,
            # we want to skip checking (station2, station1). We need to 
            # split the input in exactly half, so any given pair is only
            # checked once. One way to do this is by the natural string
            # ordering. In Python, 'a' < 'b' because 'a' comes before 
            # 'b' alphabetically. For any two strings A and B, it's true
            # that either A < B or A > B (unless A is B, but we already
            # check for that). If we check for ordering, we can quickly
            # split our input space in half.
            if station1['stationName'] > station2['stationName']:
                continue
            d = distance(station1, station2)
            csvwriter.writerow([station1['stationName'], station2['stationName'], d])
            print('Distance between {station1} and {station2} is {d}.'.format(
                    station1=station1['stationName'], station2=station2['stationName'], d=d
                ))
            # Let's be nice to Open MapQuest and wait a second in between requests
            sleep(1.0)
    f.close()