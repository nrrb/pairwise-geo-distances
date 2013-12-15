from pprint import pprint
import json
import requests
from local_settings import MAPQUEST_APP_KEY


def distance_matrix(locations, by_bicycle=False):
    """
    distance_matrix(locations, by_bicycle=False)

    :Args:
    locations - List of dictionaries. Each dictionary
      must have keys 'latitude' and 'longitude' with float
      values. For example:

      [{'latitude': 1.0, 'longitude': -5.0},
       {'latitude': -56.1, 'longitude': 3.1415},
       {'latitude': 4.0, 'longitude': 16.1}]

    Max size: 100

    by_bicycle - boolean, default False. By default, this will
     calculate the driving distance. When this is set to True,
     Google Maps will calculate the distance as travelled by
     a bike.

    :Returns:

    A list of floats, the same length as the input list_of_latlongs. 
    This list is the pairwise distance in meters between the first 
    location and every location in the list including itself. 
    """
    request_body = {
            'locations': 
            [{'latLng': {'lat': location['latitude'], 
                         'lng': location['longitude']}}
                for location in locations],
            'unit': 'k'
            }
    if by_bicycle:
        request_body['routeType'] = 'bicycle'
    r = requests.post('http://open.mapquestapi.com/directions/v2/routematrix?key={appkey}'.format(appkey=MAPQUEST_APP_KEY),
            data=json.dumps(request_body)
            )
    if r.status_code != 200:
        print("We didn't get a response from Mapquest.")
        print("We were trying to access this URL: {0}".format(r.url))
        print("Status code: {0}".format(r.status_code))
        print("Full response headers:")
        pprint(dict(r.headers))
        return
    result = json.loads(r.content)
    try:
        distances = result['distance']
    except KeyError:
        print("We didn't get the response we expected from MapQuest.")
        print("Here's what we got:")
        pprint(result)
        return
    if len(locations) != len(distances):
        print("We didn't get enough distances back for the number of locations.")
        print("Number of locations you supplied: {0}".format(len(locations)))
        print("Number of distances we received: {0}".format(len(distances)))
        return
    # distances are in kilometers, need to convert to meters
    distances = [int(1000*d) for d in distances]
    results = [{'start_id': locations[0]['id'],
                'end_id': locations[loc_index]['id'],
                'distance': distances[loc_index]}
               for loc_index in xrange(len(locations))]
    return results
