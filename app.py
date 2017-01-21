import googlemaps
import math
from JSONExtractor import *
from flask import Flask, jsonify, json, request
from flask import render_template


app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyDI18CtSf0Zhay82k2YuGkGcrOyX5n1Qc0')


@app.route("/")
def main():
	return render_template('main.html')


def calc_latlng_dist(lat1, lng1, lat2, lng2):
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
def processor():
	origin = request.form["origin"]
	destination = request.form["destination"]
	o_geocode = gmaps.geocode(origin)[0]["geometry"]["location"]
	d_geocode = gmaps.geocode(destination)[0]["geometry"]["location"]
	o_lat = o_geocode["lat"]
	o_lng = o_geocode["lng"]
	d_lat = d_geocode["lat"]
	d_lng = d_geocode["lng"]

	lat = (o_lat + d_lat) / 2
	lng = (o_lng + d_lng) / 2

	radius = calc_latlng_dist(o_lat, o_lng, lat, lng)

	extractor = JSONExtractor()

	score = extractor.generateWalkScore(lat, lng, radius)

	return result(origin, destination, o_geocode, d_geocode, radius, score)


def result(origin, dest, o_geocode, d_geocode, radius, score):
	return render_template('result.html', origin=origin, d_geocode=d_geocode,
						   destination=dest, o_geocode=o_geocode,
						   radius=radius, score=score)


if __name__ == "__main__":
    app.run()