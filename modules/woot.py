#!/usr/bin/python

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS

def woot(shana, event):
	soup = BS(urlopen("http://www.woot.com/"))

	title = soup.find("li", "site wootplus woot ").find("div", "title").get_text()
	price_now = soup.find("li", "site wootplus woot ").find("span", "price").get_text()
	price_then = soup.find("li", "site wootplus woot ").find("span", "list-price").get_text()
	price_off = soup.find("li", "site wootplus woot ").find("span", "percentage").get_text()
	
	shana.say("%s  Was: %s Now: %s (%s)" % (title, price_then, price_now, price_off))
	
woot.name = 'woot'
woot.commands = ['woot']