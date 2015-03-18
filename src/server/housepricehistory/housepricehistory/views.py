from django.http import HttpResponse
from django.template.loader import render_to_string
import datetime
import os

def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def jinja(request):
	return HttpResponse(render_to_string('jinja.jinja'))
