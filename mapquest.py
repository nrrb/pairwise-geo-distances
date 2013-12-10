from pprint import pprint
import json
import requests
from local_settings import MAPQUEST_APP_KEY


def distance_matrix(locations):
    """
    distance_matrix(locations)

    :Args:
    locations - List of dictionaries. Each dictionary
      must have keys 'latitude' and 'longitude' with float
      values. For example:

      [{'latitude': 1.0, 'longitude': -5.0},
       {'latitude': -56.1, 'longitude': 3.1415},
       {'latitude': 4.0, 'longitude': 16.1}]

    :Returns:

    A list of floats, the same length as the input list_of_latlongs. 
    This list is the pairwise distance between the first location
    and every location in the list including itself. 
    """
    request_body = {
            'locations': 
            [{'latLng': {'lat': location['latitude'], 'lng': location['longitude']}}
                for location in locations]
            }
    r = requests.post('http://open.mapquestapi.com/directions/v2/routematrix?key={appkey}'.format(appkey=MAPQUEST_APP_KEY),
            data=json.dumps(request_body)
            )
    if r.status_code != 200:
        print("We didn't get a response from Mapquest.")
        print("We were trying to access this URL: {0}".format(r.url))
        print("Status code: {0}".format(r.status_code))
        print("Full response headers:")
        pprint(dict(r.headers))
        exit(1)
    result = json.loads(r.content)
    try:
        distances = result['distance']
    except KeyError:
        print("We didn't get the response we expected from MapQuest.")
        print("There is no 'distance' in the returned JSON.")
        print("Here's what we got:")
        pprint(result)
        exit(1)
    return distance
