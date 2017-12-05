from django.shortcuts import render
import requests
from django.http import JsonResponse 


def pts(request):
	key = "AIzaSyCeM7pffJ6naduIgfQGvzbiVA78v6Zrit4"
	query = request.GET.get('query', '')
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&region=kw&key=%s"%(query, key)

	next_page = request.GET.get('nextpage')
	if next_page is not None:
		url += "&pagetoken="+next_page

	response = requests.get(url)

	context = {
		"response":response.json(),
		}

	return render(request, "pts.html", context)

def place_detail(request):
	key = "AIzaSyCeM7pffJ6naduIgfQGvzbiVA78v6Zrit4"
	place_id = request.GET.get('place_id', '')
	url = "https://maps.googleapis.com/maps/api/place/details/json?key=%s&placeid=%s"%(key, place_id)

	response = requests.get(url)
	map_key = "AIzaSyA6IV2xVJuhe9GrvqWji6mJWNmMtwNpnl4"
	context = {
		"response":response.json(),
		"map": map_key,
		}
	return render(request, "place_detail.html", context)