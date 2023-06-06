import csv
import json
import googlemaps


API = json.load(open('secret.json','r'))['API']
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
gmaps = googlemaps.Client(key=API)


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
        distance = gmaps.distance_matrix([source[0]+ ' ' +source[1]],[dest[0]+ ' ' +dest[1]],mode='driving')['rows'][0]['elements'][0]
        
        distArray.append(distance)

        
with open('distance.json', 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(distArray, indent=4)
        jsonf.write(jsonString)

