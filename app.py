import googlemaps
from flask import Flask, jsonify, json, request
from flask import render_template


app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyDI18CtSf0Zhay82k2YuGkGcrOyX5n1Qc0')


@app.route("/")
def main():
	return render_template('main.html')


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

	return result(origin, destination, o_geocode, d_geocode)


def result(origin, dest, o_geocode, d_geocode):
	return render_template('result.html', origin=origin, d_geocode=d_geocode,
						   destination=dest, o_geocode=o_geocode)


if __name__ == "__main__":
    app.run()