"""
Google Maps Distance Matrix module.
Actually using Google Maps interface through generous donation of
Smart Chicago Apps.
"""
# Standard Library imports
from __future__ import unicode_literals
from pprint import pprint
import json
# Third Party imports
import requests
# Local imports
from local_settings import GOOGLE_MAPS_API_KEY

# https://developers.google.com/maps/documentation/distancematrix/#Limits
GOOGLE_API_URL_SIZE_LIMIT = 2000


def format_latlong(location):
    return '{0},{1}'.format(location['latitude'], location['longitude'])

def distance_matrix(locations, by_bicycle=False):
    """
    distance_matrix(locations, by_bicycle=False)

    :Args:
    locations - List of dictionaries. Each dictionary
      must have keys 'id', 'latitude', and 'longitude' with
      float values. For example:

      [
       {'id': 1, 'latitude': 1.0, 'longitude': -5.0},
       {'id': 2, 'latitude': -56.1, 'longitude': 3.1415},
       {'id': 3, 'latitude': 4.0, 'longitude': 16.1}
      ]

    by_bicycle - boolean, default False. By default, this will
     calculate the driving distance. When this is set to True,
     Google Maps will calculate the distance as travelled by
     a bike.

    :Returns:

    A list of the same length as the input locations, in the 
    following format:

    [
     {'start_id': 1, 'end_id': 1, 'distance': 0},
     {'start_id': 1, 'end_id': 2, 'distance': 501},
     {'start_id': 1, 'end_id': 3, 'distance': 102}
    ]

    This list is the pairwise distance in meters between the 
    first location and every location in the list including 
    itself. 
    """
    origin = format_latlong(locations[0])
    destinations = '|'.join([format_latlong(location) 
                             for location in locations]
                            )
    if by_bicycle:
        mode = 'bicycling'
    else:
        mode = 'driving'
    url = 'http://services.smartchicagoapps.org/v1/maps/distancematrix?origins={origins}&destinations={destinations}&sensor=false&mode={mode}&key={api_key}'.format(
            origins=origin,
            destinations=destinations,
            mode=mode,
            api_key=GOOGLE_MAPS_API_KEY,
        )
    if len(url) > GOOGLE_API_URL_SIZE_LIMIT:
        print("The url is too long, try with fewer locations.")
        return
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        print("We didn't get a response from Google.")
        print("We were trying to access this URL: {0}".format(response.url))
        print("Status code: {0}".format(response.status_code))
        print("Full response headers:")
        pprint(dict(response.headers))
        return
    result = json.loads(response.content)
    try:
        distances = []
        for i, element in enumerate(result['rows'][0]['elements']):
            if by_bicycle and element['status'] == 'ZERO_RESULTS':
                # Sometimes bicycle routes are not calculable,
                # get distance using driving flag
                driving_matrix = distance_matrix([locations[0], locations[i]])
                if not driving_matrix:
                    return
                # this is a dirty hack
                distance = driving_matrix[1]['distance']
            else:
                distance = element['distance']['value']
            distances.append(distance)
    except KeyError, IndexError:
        print("We didn't get the response we expected from Google.")
        print("Here's what we got:")
        pprint(result)
        return
    if len(locations) != len(distances):
        print("We didn't get enough distances back for the number of locations.")
        print("Number of locations you supplied: {0}".format(len(locations)))
        print("Number of distances we received: {0}".format(len(distances)))
        return
    return [{'start_id': locations[0]['id'],
                'end_id': locations[loc_index]['id'],
                'distance': distances[loc_index]}
               for loc_index in xrange(len(locations))]
