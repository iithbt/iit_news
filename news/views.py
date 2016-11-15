# from django.shortcuts import render
from django.http import HttpResponse
from . import grab_feed

# Create your views here.
def index(request):
    return HttpResponse("News index page")

def fetch(request):
	count = grab_feed.main()
	return HttpResponse("Fetched " + str(count) + " new feeds")