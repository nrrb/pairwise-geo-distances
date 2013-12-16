# Standard Library imports
from pprint import pprint
import json
# Third Party imports
import requests

DIVVY_STATIONS_URL = 'http://divvybikes.com/stations/json'


def get_station_list(filename=None):
    """
    get_station_list()

    :Args:
    filename (optional) - The path to a file containing previously downloaded
     station information.

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
    if filename:
        with open(filename, 'rb') as f:
            station_data = json.load(f)
    else:
        response = requests.get(DIVVY_STATIONS_URL)
        if response.status_code != requests.codes.ok:
            print("We didn't get a response from Divvy Bikes.")
            print("We were trying to access this URL: {0}".format(response.url))
            print("Status code: {0}".format(response.status_code))
            print("Full response headers:")
            pprint(dict(response.headers))
            return
        station_data = json.loads(response.content)
    try:
        stations = station_data['stationBeanList']
    except KeyError:
        print("We didn't get the response we expected from Divvy.")
        print("There is no 'stationBeanList' in the returned JSON.")
        print("Here's what we got:")
        pprint(station_data)
        return
    return stations
