from django.http import HttpResponse
from django.template.loader import render_to_string

import SoldDataService


def index(request):
	"""
	Displays the homepage containing the history graphs.

	:param request: HTTP Request
	:return: Rendered homepage
	"""
	return HttpResponse(render_to_string('history.jinja'))

def jinja(request):
	return HttpResponse(render_to_string('jinja.jinja'))

def averagePrices(request):
	"""
	Gets sold price history JSON for use within the graphs.

	Supports start and end timestamps to get snapshots of data.

	:param request: HTTP Request
	:return: history JSON
	"""
	if request.method == 'GET' and "start" in request.GET:
		start = request.GET["start"]
		end = request.GET["end"]
		response = SoldDataService.getAveragePriceData(start, end)
	else:
		response = SoldDataService.getAllAveragePriceData()

	return HttpResponse(response, content_type = 'text/plain')
