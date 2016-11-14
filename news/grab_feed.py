from bs4 import BeautifulSoup
from time import mktime
from datetime import datetime
from .models import NewsArticles
from feedparser import parse


def main():
	url = 'https://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&output=rss&q=iit'
	feed = loadfeed(url)
	for item in feed.entries:
		processFeedItem(item)
	return

def loadfeed(url):
	return parse(url)

def processFeedItem(item):
	query = NewsArticles.objects.filter(post_id=item.id) #fine tune this later
	if len(query) > 0:
		return
	summaryText, img_src, source = parseSummary(item.summary)
	url = parseFeedUrl(item.link)
	n = NewsArticles ( post_id = item.id,
		title = item.title,
		pub_date = getPubDate(item.published_parsed),
		summary = summaryText,
		img_src = img_src,
		url = url,
		source = source)
	n.save()
	return


def getPubDate(time_struct):
	return datetime.fromtimestamp(mktime(time_struct))

def parseSummary(summary):
	soup = BeautifulSoup(summary, 'html.parser')
	s = soup.find("div", "lh").find_all("font")
	source = s[0].text.encode("ascii")
	summaryText = s[2].text.encode("ascii")
	img_src = soup.find("img").get("src")
	return summaryText, img_src, source 

def parseFeedUrl(link):
	i = link.index('&url=') + 5
	return link[i:]