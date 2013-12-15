# Standard Library imports
from collections import defaultdict
import json
import time
import csv
# Local imports
import divvy
import googlemaps
import mapquest

# For the googlemaps api, this is limited by the URL length limit
DISTANCE_MATRIX_SIZE = 24


if __name__ == "__main__":
    stations = divvy.get_station_list()
    results = []
    for station1 in stations:
        for station2_index_begin in xrange(0, len(stations), DISTANCE_MATRIX_SIZE):
            station2_index_end = station2_index_begin + DISTANCE_MATRIX_SIZE
            locations = [station1] + stations[station2_index_begin:station2_index_end]
            print("Calling Google.")
            results += googlemaps.distance_matrix(locations, by_bicycle=True)
    distances = defaultdict(lambda: {})
    for result in results:
        distances[result['start_id']][result['end_id']] = result['distance']
    print("Writing to JSON file.")
    with open('station_distances_by_bicycle.json', 'wb') as f:
        f.write(json.dumps(distances))
    stations_by_id = {station['id']: station for station in stations}
    print("Writing to CSV file.")
    with open('station_distances_by_bicycle.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['start_station', 'end_station', 'distance'])
        for start_id in distances:
            start_station = stations_by_id[start_id]
            for end_id in distances[start_id]:
                end_station = stations_by_id[end_id]
                writer.writerow([start_station['stationName'],
                                 end_station['stationName'],
                                 distances[start_id][end_id]])


    

