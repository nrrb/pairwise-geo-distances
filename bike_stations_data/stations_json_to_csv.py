import json
import csv
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Syntax:")
        print("{script} in_file.json out_file.csv".format(script=__file__))
        sys.exit(1)

    in_file, out_file = sys.argv[1:3]

    with open(in_file, 'rb') as f:
        data = json.load(f)

    stations = data['stationBeanList']

    with open(out_file, 'wb') as f:
        dw = csv.DictWriter(f, fieldnames=stations[0].keys())
        dw.writeheader()
        dw.writerows(stations)
