from django.http import HttpResponse
from django.template.loader import render_to_string

from services import SoldDataService


def index(request):
	"""
	Displays the homepage containing the history graphs.

	:param request: HTTP Request
	:return: Rendered homepage
	"""
	return HttpResponse(render_to_string('history.jinja'))

def indexImproved(request):
	return HttpResponse(render_to_string('history-improved.jinja'))

def jinja(request):
	return HttpResponse(render_to_string('jinja.jinja'))

def averagePrices(request):
	"""
	Gets average price history TSV for use within the graphs.

	Supports start and end timestamps to get snapshots of data.

	:param request: HTTP Request.
	:return: Average sold prices TSV.
	"""
	# Remove empty get keys
	request.GET = dict((k, v) for k, v in request.GET.iteritems() if v)

	if request.method == 'GET' and len(request.GET) > 0:
		start = request.GET.get("start", "01-01-1970")
		end = request.GET.get("end", "19-01-2038")
		postCode = request.GET.get("postCode", None)
		response = SoldDataService.getAveragePriceData(start, end, postCode)
	else:
		response = SoldDataService.getAllAveragePriceData()

	return HttpResponse(response, content_type = 'text/plain')
