import csv
import numpy as np
import requests, json
import os

API = 'AIzaSyCrw2zzf3fwPrRj6Ck68FBO6cIoBW03snc'
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'


with open('kamera_test.csv', 'r') as kam_csv:
    reader = csv.DictReader(kam_csv, delimiter=';')
    distArray = []
    for line in reader:
        # Take source as input
        source = [coordinate for coordinate in line['kamera1_koord'].split(',')]
        # Take destination as input
        dest = [coordinate for coordinate in line['kamera2_koord'].split(',')]
        # url variable store url
        # Get method of requests module
        # return response object
        r = requests.get(url + 'origins = ' + source[0] + " " + source[1] +
                    '&destinations = ' + dest[0] + " " + dest[1] +
                    '&key = ' + API+
                    '&mode=DRIVING')
        
        distArray.append(r.json)
    
with open('distance.json', 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(distArray, indent=4)
        jsonf.write(jsonString)
