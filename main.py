import csv, json, googlemaps
import pandas as pd

# Environmental variables
API = json.load(open('secret.json','r'))['API']
URL ='https://maps.googleapis.com/maps/api/distancematrix/json?'
GMAPS = googlemaps.Client(key=API)


def getDistance(source:list[str], destination:list[str], travel_mode:str) -> dict:
    '''
    Query distances through Googles Distance Matrix API. Given 2 lists of strings including the 2-2 coordinates for query. The function returns the infromation from the query.
    ---------------------------------------------------------
    Input: The cam coordinates to query and the travelling method to be queried in.
    Output: A dictionary of query informations.
    '''
    distance = GMAPS.distance_matrix(
        [source[0]+ ' ' +source[1]],
        [destination[0]+ ' ' +destination[1]],
        mode=travel_mode)
    return distance

def distanceQueryWrapper(coordinates_file:str, source_col:str, destination_col:str) -> list:
    '''
    This is a wrapper funciton to iterate over and query all the distances from the Google Distance Matrix API. The coordinates of both source and destionation locations should be comma separated strings such as "47.3, 16.5".
    ---------------------------------------------------
    Input: A CSV including the cam coordinates and the column names including the koordinates of cameras.
    Output: A list of the query informations
    '''
    with open(coordinates_file, 'r') as cam_csv:
        reader = csv.DictReader(cam_csv, delimiter=';')
        distance_array = []
        duration_array = []
        for line in reader:
            source = [coordinate for coordinate in line[source_col].split(',')]
            destination = [coordinate for coordinate in line[destination_col].split(',')]
            distanceData = getDistance(source, destination, 'driving')
            distance_array.append(distanceData['rows'][0]['elements'][0]['distance']['value'])
            duration_array.append(distanceData['rows'][0]['elements'][0]['duration']['value'])
    
    return distance_array, duration_array


def writeToCSV(orig_file, output_file, distance_array, duration_array):
    '''
    Extends the original file with the queried distances.
    ------------------------------------------
    Input: Original file, output file, array of distances in meteres and array of travel durations in seconds.
    Output: Extended version of original CSV with distance and duration data.
    '''
    original = pd.read_csv(orig_file, encoding='UTF-8', sep=';')
    original['distance'] = distance_array
    original['duration'] = duration_array
    original.to_csv(output_file, sep=';')

def main():
    distance_array, duration_array = distanceQueryWrapper('input/kamera_koordinatak.csv', 'kamera1_koord', 'kamera2_koord')
    writeToCSV('input/kamera_koordinatak.csv', 'output/kamera_ext.csv', distance_array, duration_array)


if __name__=='__main__':
    main()