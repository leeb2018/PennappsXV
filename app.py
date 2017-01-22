import googlemaps
import math
import json
from JSONExtractor import *
from flask import Flask, jsonify, json, request, render_template


app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyDI18CtSf0Zhay82k2YuGkGcrOyX5n1Qc0')


@app.route("/")
def main():
	''' 
	render the main page with tex box for users to input origin 
	and destination.
    '''
	return render_template('main.html')


def calc_latlng_dist(lat1, lng1, lat2, lng2):
	''' 
	calculates distance between two given coordinates (lat1, lng1) and
	(lat2, lng2)
    '''
	radlat1 = math.pi * lat1 / 180
	radlat2 = math.pi * lat2 / 180
	theta = lng1 - lng2
	radtheta = math.pi * theta / 180
	dist = math.sin(radlat1) * math.sin(radlat2) + math.cos(radlat1) * math.cos(radlat2) * math.cos(radtheta)
	dist = math.acos(dist)
	dist = dist * 180 / math.pi
	dist = dist * 60 * 1.1515
	dist = dist * 1609.344

	return dist

@app.route('/result', methods=['POST'])
def process_data():
	''' 
	obtain user input and translate origin and destination to geo-coordinates.
	Using extracted information, acquire necessary information such as radius,
	walk score, and filtered crime data. Then, pass acquired informtion to result()
	to render it.
    '''
    # Extract/transform input
	origin = request.form["origin"]
	destination = request.form["destination"]
	o_geocode = gmaps.geocode(origin)[0]["geometry"]["location"]
	d_geocode = gmaps.geocode(destination)[0]["geometry"]["location"]
	o_lat = o_geocode["lat"]
	o_lng = o_geocode["lng"]
	d_lat = d_geocode["lat"]
	d_lng = d_geocode["lng"]

	# find the middle point
	lat = (o_lat + d_lat) / 2
	lng = (o_lng + d_lng) / 2

	radius = calc_latlng_dist(o_lat, o_lng, lat, lng)

	# create JSONExtractor instance and, with it, obtain necessary data.
	extractor = JSONExtractor()

	data = extractor.generateWalkScore(lat, lng, radius)
	score = "{0:.2f}".format(data["walk_score"])
	crime_data_by_date = data["summary_by_date"]
	crime_data_by_crime = data["summary_by_crime"]

	return result(origin, destination, score, o_lat, o_lng, d_lat, d_lng, 
			      crime_data_by_crime, crime_data_by_date)


def result(origin, dest, score, o_lat, o_lng, d_lat, d_lng, 
		   sum_by_crime, sum_by_date):
	''' render result page.'''
	return render_template('result.html', origin=origin, destination=dest, 
						   score=score, o_lat=o_lat, o_lng=o_lng, d_lat=d_lat, 
						   d_lng=d_lng, sum_by_date=json.dumps(sum_by_date),
						   sum_by_crime=json.dumps(sum_by_crime))


if __name__ == "__main__":
    app.run()