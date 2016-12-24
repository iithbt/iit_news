from bs4 import BeautifulSoup
from time import mktime
from datetime import datetime
from django.utils import timezone
from .models import NewsArticle
from feedparser import parse
import requests

import sys

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	count = 0
	url = 'https://news.google.co.in/news?q=iit&hl=en&gl=in&output=rss'
	feed = loadfeed(url)
	for item in feed.entries:
		if processFeedItem(item):
			count += 1
	print ("count",count)
	return count

def loadfeed(url):
	return parse(url)

def processFeedItem(item):
	query = NewsArticle.objects.filter(post_id=item.id) #fine tune this later
	if len(query) > 0:
		return False
	summaryText, img_src, source = parseSummary(item.summary)
	url = parseFeedUrl(item.link)
	title = item.title
	if title.endswith(source):
		title = title[:-(len(source) + 3)]
	n = NewsArticle ( post_id = item.id,
		title = title,
		pub_date = getPubDate(item.published_parsed),
		summary = summaryText,
		img_src = img_src,
		url = url,
		source = source)
	n.save()
	sendNotification(title, summaryText, url, img_src)
	return True

def sendNotification(title, body, url, icon_url):
	fcm_url = "https://fcm.googleapis.com/fcm/send"
	headers = {
		'Authorization': 'key=AIzaSyDNCsH4twaJc5JT5dZrq77JYkB0MhoIE2E',
		'Content-Type':'application/json',
		}
	payload = { 
		"notification": {
    		"title": title,
    		"body": body,
    		"icon" : icon_url,
    		"click_action" : url,
  		},
  		"to" : "/topics/iitnews"
	}
	r = requests.post(fcm_url, headers=headers, data=payload)

def getPubDate(time_struct):
	return datetime.fromtimestamp(mktime(time_struct),timezone.utc)

def parseSummary(summary):
	soup = BeautifulSoup(summary, 'html.parser')
	s = soup.find("div", "lh").find_all("font")
	source = s[0].text
	summaryText = s[2].text
	img_src = soup.find("img").get("src")
	return summaryText, img_src, source 

def parseFeedUrl(link):
	i = link.index('&url=') + 5
	return link[i:]