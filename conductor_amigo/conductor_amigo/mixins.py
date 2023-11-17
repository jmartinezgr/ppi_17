from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
import json
import datetime
from humanfriendly import format_timespan
from django.http import JsonResponse
from django.conf import settings
# import Google Maps API key from settings.py
GOOGLE_MAPS_API_KEY = settings.GOOGLE_MAPS_API_KEY


def Directions(*args, **kwargs):
	'''
	Handles directions from Google
	'''

	lat_a = kwargs.get("lat_a")
	long_a = kwargs.get("long_a")
	lat_b = kwargs.get("lat_b")
	long_b = kwargs.get("long_b")


	origin = f'{lat_a},{long_a}'
	destination = f'{lat_b},{long_b}'

	result = requests.get(
		'https://maps.googleapis.com/maps/api/directions/json?',
		 params={
		 'origin': origin,
		 'destination': destination,
		 'mode': 'driving',
		 "key": GOOGLE_MAPS_API_KEY
		 })

	directions = result.json()

	if directions["status"] == "OK":

		routes = directions["routes"][0]["legs"]

		distance = 0
		duration = 0
		route_list = []

		for route in range(len(routes)):

			distance += int(routes[route]["distance"]["value"])
			duration += int(routes[route]["duration"]["value"])

			route_step = {
				'origin': routes[route]["start_address"],
				'destination': routes[route]["end_address"],
				'distance': routes[route]["distance"]["text"],
				'duration': routes[route]["duration"]["text"],

				'steps': [
					[
						s["distance"]["text"],
						s["duration"]["text"],
						s["html_instructions"],

					]
					for s in routes[route]["steps"]]
				}
				
			route_list.append(route_step)

	return {
		"origin": origin,
		"destination": destination,
		"distance": f"{round(distance/1000, 2)} Km",
		"duration": format_timespan(duration),
		"route": route_list
		}