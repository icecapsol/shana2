#!/usr/bin/python

from urllib.request import urlopen
import re
from bs4 import BeautifulSoup as BS

def f_woot(phenny, input):
	soup = BS(urlopen("http://www.woot.com/"))

	title = soup.find("li", "site wootplus woot ").find("div", "title").get_text()
	price_now = soup.find("li", "site wootplus woot ").find("span", "price").get_text()
	price_then = soup.find("li", "site wootplus woot ").find("span", "list-price").get_text()
	price_off = soup.find("li", "site wootplus woot ").find("span", "percentage").get_text()
	
	phenny.say("%s  Was: %s Now: %s (%s)" % (title, price_then, price_now, price_off))
	
f_woot.name = 'woot'
f_woot.commands = ['woot']
f_woot.priority = 'low'