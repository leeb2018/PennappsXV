from bs4 import BeautifulSoup
import requests

def generateURL_circle(lat_coord, long_coord, radius):
	
	base_url = 'https://data.phila.gov/resource/sspu-uyfa.json?$where='
	url = base_url + ('within_circle(shape, %f, %f, %d)' %(lat_coord, long_coord, radius))

	return url

def summarizeCrimeActivity(json_list):
    '''
    Parses through the JSON files and does three things:
    1) Save the data structure with primary key as yyyymmm
    2) Save the data structure with primary key as crime type
    3) Generate the walkscore based on a predetermined weighting scheme
    '''

    for json_item in json_list:

        long_coord = json_item['shape']['coordinates'][0]
        lat_coord = json_item['shape']['coordinates'][1]
        crime_type = 


	summary = {}


## -----------------   MAIN FUNCTION   -----------------##
if __name__ == '__main__':
    
    lat_coord = 39.96112
    long_coord = -75.195521
    radius = 500

    my_url = generateURL_circle(lat_coord, long_coord, radius)
    r = requests.get(my_url)
    json_list = r.json()