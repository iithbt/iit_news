# from django.shortcuts import render
from django.http import HttpResponse
from . import grab_feed, notif_reg
from .models import FcmDetails
import threading
from datetime import datetime

# Create your views here.
def index(request):
    return HttpResponse("News index page")

def fetch(request):
	# threading.Thread(target=grab_feed.main()).start()
	count = grab_feed.main()
	return HttpResponse("Fetched " + str(count) + " new feeds")

def reg_notif(request):
	if request.method == 'GET':
		token = request.GET['token']
		if len(token)>0 :
			browser, os, device = notif_reg.getUserDetails(request)
			fcm_user = FcmDetails (
				token = token,
				date = datetime.now(),
				ip = notif_reg.get_client_ip(request),
				browser = browser,
				os = os,
				device = device)
			fcm_user.save()
			notif_reg.regiter_token_for_topic(token)
			return HttpResponse("registered")
		else:
			return HttpResponse("no token sent")


