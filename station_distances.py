# Standard Library imports
from collections import defaultdict
from math import ceil
import argparse
import json
import time
import csv
import sys
import os
# Local imports
import divvy
import googlemaps
import mapquest

# For the googlemaps api, this is limited by the URL length limit
DISTANCE_MATRIX_SIZE = 24

def array_without_element(array, element):
    index = array.index(element)
    return array[:index] + array[index+1:]

def parse_arguments():
    parser = argparse.ArgumentParser(description='Pairwise Distance Calculator for Divvy Bike Stations')
    parser.add_argument('output_filename', help='''The path to the CSV file where the output should go.
            NOTE: This will be used to output the cache JSON file that can be used at a later date with
            the --existing-file option.''')
    parser.add_argument('--stations-file', help='''The path to a JSON file containing the stations data as
        downloaded from Divvy Bikes. Default: the stations data will be downloaded automatically from 
        the Divvy Bikes website.''')
    parser.add_argument('--existing-file', help='''The path to a JSON file generated on a previous run
        of this script, containing distance in meters between stations identified by their Divvy station
        ID number.''')
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    if arguments.stations_file:
        stations = divvy.get_station_list(filename=arguments.stations_file)
    else:
        print('Getting latest list of bike stations from Divvy...')
        stations = divvy.get_station_list()

    if arguments.existing_file:
        with open(arguments.existing_file, 'rb') as f:
            existing_distances = json.load(f)

    results = []
    for station_index, station1 in enumerate(stations):
        print("Working on station \"{name}\" ({i} of {N}).".format(
                name=station1['stationName'],
                i=station_index+1, 
                N=len(stations)
            ))
        other_stations = array_without_element(stations, station1)
        print('Number of stations to calculate distance to: {0}'.format(len(other_stations)))
        if arguments.existing_file:
            other_stations = [station for station in other_stations
                    if str(station['id']) not in existing_distances[str(station1['id'])]]
            print('We have {n} stations left to check.'.format(n=len(other_stations)))
        for call_number, station2_index_begin in enumerate(xrange(0, len(other_stations), DISTANCE_MATRIX_SIZE)):
            station2_index_end = station2_index_begin + DISTANCE_MATRIX_SIZE
            locations = [station1] + other_stations[station2_index_begin:station2_index_end]
            print("Calling Google ({call_number} of {total_calls})".format(
                    call_number=call_number+1,
                    total_calls=int(ceil(len(other_stations)/float(DISTANCE_MATRIX_SIZE)))
                ))
            results += googlemaps.distance_matrix(locations, by_bicycle=True)
    if len(results) == 0:
        print("No distances were calculated, I guess you have everything!")
        sys.exit(1)
    # Got all the distances, now let's remove duplicates
    distances = defaultdict(lambda: {})
    for result in results:
        distances[result['start_id']][result['end_id']] = result['distance']
    # Output this pretty picture to save ourselves time in the future
    print("Writing to cache JSON file.")
    base, _ = os.path.splitext(arguments.output_filename)
    cache_filename = base + '.json'
    with open(cache_filename, 'wb') as f:
        f.write(json.dumps(distances))
    stations_by_id = {station['id']: station for station in stations}
    print("Writing to CSV file.")
    with open(arguments.output_filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['start_station', 'end_station', 'distance'])
        for start_id in distances:
            start_station = stations_by_id[start_id]
            for end_id in distances[start_id]:
                end_station = stations_by_id[end_id]
                writer.writerow([start_station['stationName'],
                                 end_station['stationName'],
                                 distances[start_id][end_id]])


    

