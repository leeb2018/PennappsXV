from bs4 import BeautifulSoup
from datetime import datetime
import requests

class JSONExtractor:

    data = {}

    def __init__(self):
        self.data = {}


    def generateURL_circle(self, lat_coord, long_coord, radius):
        '''
        Generates the url for the GET operation
        @param: lat_coord - the latitude of the desired position
                long_coord - the longtitude of the desired position
                radius - the radius of the circle (in meters, I think)
        '''
    	
        base_url = 'https://data.phila.gov/resource/sspu-uyfa.json?$where='
        url = base_url + ('within_circle(shape, %f, %f, %d)' %(lat_coord, long_coord, radius))

        return url

    def generateWalkScore(self, lat_coord, long_coord, radius):
        '''
        Generates the walk score for the given lat_coord, long_coord, radius
        @param: lat_coord - the latitude of the desired position
                long_coord - the longtitude of the desired position
                radius - the radius of the circle (in meters, I think)
        '''
        my_url = generateURL_circle(lat_coord, long_coord, radius)
        r = requests.get(my_url)
        json_list = r.json()

        summaryByDate, summaryByCrime, walkScore = summarizeCrimeActivity(json_list)

        return walkScore


    def summarizeCrimeActivity(self, json_list):
        '''
        Parses through the JSON files and does three things:
        1) Save the data structure with primary key as yyyymmm
        2) Save the data structure with primary key as crime type
        3) Generate the walkscore based on a predetermined weighting scheme

        @param: json_list - list of json-formatted objects
        '''

        summaryByDate = {}
        summaryByCrime = {}
        walkScore = 100.0

        for json_item in json_list:

            # Extract relevant information
            long_coord = json_item['shape']['coordinates'][0]
            lat_coord = json_item['shape']['coordinates'][1]
            coords = json_item['shape']['coordinates']
            crime = json_item['text_general_code']
            yyyymmdd = json_item['dispatch_date'].replace('-', '')
            time = json_item['dispatch_time']

            # Add to the summaryByDate dictionary
            yyyymm = yyyymmdd[0:6] # extract out yyyymm
            if yyyymm not in summaryByDate.keys():
                summaryByDate[yyyymm] = {}
            if lat_coord not in summaryByDate[yyyymm].keys():
                summaryByDate[yyyymm][lat_coord] = {}
            summaryByDate[yyyymm][lat_coord][long_coord] = crime

            # Compute the WalkScore
            now = datetime.now()
            diff_days = (now - datetime.strptime(yyyymm, '%Y%m')).days

            if 'HOMICIDE' in crime.upper():

                walkScore = walkScore - (100.0 / diff_days)

            elif 'VANDALISM' in crime.upper():

                walkScore = walkScore - (17.5 / diff_days)

            elif 'UNDER THE INFLUENCE' in crime.upper():

                walkScore = walkScore - (6.5 / diff_days)

            elif 'NARCOTIC' in crime.upper():

                walkScore = walkScore - (3.0 / diff_days)

            elif 'DISORDERLY' in crime.upper():

                walkScore = walkScore - (20.0 / diff_days)

            elif 'BURGLARY' in crime.upper():

                walkScore = walkScore - (9.0 / diff_days)

            elif 'THEFT' in crime.upper():

                walkScore = walkScore - (4.0 / diff_days)

            elif 'FIREARM' in crime.upper():

                walkScore = walkScore - (100.0 / diff_days)

            elif 'NO FIREARM' in crime.upper():

                walkScore = walkScore - (50.0 / diff_days)

            else:

                walkScore = walkScore - (3.0 / diff_days)

            # Add to the summaryByCrime dictionary
            if crime not in summaryByCrime.keys():
                summaryByCrime[crime] = {}
            if lat_coord not in summaryByCrime[crime].keys():
                summaryByCrime[crime][lat_coord] = {}
            summaryByCrime[crime][lat_coord][long_coord] = yyyymmdd

        return summaryByDate, summaryByCrime, walkScore


## -----------------   MAIN FUNCTION   -----------------##
if __name__ == '__main__':
    
    extractor = JSONExtractor()
    score = extractor.generateWalkScore(lat_coord = 39.96112, long_coord = -75.195521, radius = 100)