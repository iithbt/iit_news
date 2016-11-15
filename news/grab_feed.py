from bs4 import BeautifulSoup
from time import mktime
from datetime import datetime
from django.utils import timezone
from .models import NewsArticle
from feedparser import parse

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
	return count

def loadfeed(url):
	return parse(url)

def processFeedItem(item):
	query = NewsArticle.objects.filter(post_id=item.id) #fine tune this later
	if len(query) > 0:
		return False
	summaryText, img_src, source = parseSummary(item.summary)
	url = parseFeedUrl(item.link)
	n = NewsArticle ( post_id = item.id,
		title = item.title,
		pub_date = getPubDate(item.published_parsed),
		summary = summaryText,
		img_src = img_src,
		url = url,
		source = source)
	n.save()
	return True


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