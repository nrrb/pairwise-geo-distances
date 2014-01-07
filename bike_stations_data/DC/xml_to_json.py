from xml.etree.ElementTree import fromstring
import json


with open('DCBikeStations.xml', 'rb') as f:
    data = fromstring(f.read())

stations = [{child.tag: child.text for child in station.getchildren()}
            for station in data.findall('station')]

with open('DCBikeStations.json', 'wb') as f:
    # We'll output this with a similar structure to the Alt Bikes JSON
    f.write(json.dumps({'stationBeanList': stations}))
