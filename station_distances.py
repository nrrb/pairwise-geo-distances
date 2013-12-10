from pprint import pprint
import json
import csv
import re
import requests
from mapquest import distance_matrix
from models import divvy_bike_station
from local_settings import DIVVY_STATIONS_URL


def get_station_list():
    """
    get_station_list()

    :Args:
    None!

    :Returns:
    A list of Divvy bike stations with the following information
    per station: 
    {u'altitude': u'',
     u'availableBikes': 9,
     u'availableDocks': 10,
     u'city': u'',
     u'id': 5,
     u'landMark': u'030',
     u'lastCommunicationTime': None,
     u'latitude': 41.8739580629,
     u'location': u'620 S. State St.',
     u'longitude': -87.6277394859,
     u'postalCode': u'',
     u'stAddress1': u'State St & Harrison St',
     u'stAddress2': u'',
     u'stationName': u'State St & Harrison St',
     u'statusKey': 1,
     u'statusValue': u'In Service',
     u'testStation': False,
     u'totalDocks': 19}
    """
    r = requests.get(DIVVY_STATIONS_URL)
    if r.status_code != 200:
        print("We didn't get a response from Divvy Bikes.")
        print("We were trying to access this URL: {0}".format(r.url))
        print("Status code: {0}".format(r.status_code))
        print("Full response headers:")
        pprint(dict(r.headers))
        exit(1)
    station_data = json.loads(r.content)
    try:
        stations = station_data['stationBeanList']
    except KeyError:
        print("We didn't get the response we expected from Divvy.")
        print("There is no 'stationBeanList' in the returned JSON.")
        print("Here's what we got:")
        pprint(station_data)
        exit(1)
    return stations

if __name__ == "__main__":
    # Get latest station list
    stations = get_station_list()
    # Compare latest station list to what's in database
    # If there are any new stations, add them to the database and
    #  calculate new distances between them and the other stations
    # Record current datetime in database as last time checked
