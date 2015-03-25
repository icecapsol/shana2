# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
import re

def isbn(shana, event):
	url = "http://www.lookupbyisbn.com/Search/Book/%s/1"
	numbers = re.compile('[0-9]')
	raw = event.group(2)
	isbnno = ''.join(numbers.findall(raw))

	if len(isbnno) not in [9, 10, 13]:
		shana.reply("invalid ISBN")
		return
	if len(isbnno) == 9:
		isbnno = "0"+isbnno

	try:
		page = urlopen(url % isbnno)
	except:
		shana.say("ISBN not found")
		return
	soup = BS(page)

	for item in soup.find_all("li", style="margin-bottom:1em;"):
		title = item.a.string
		author = item.u.string
		publisher = item.i.string
		break

	shana.say("ISBN: %s => %s, %s, %s" % (isbnno, title, author, publisher))

isbn.name = "isbn"
isbn.commands = ['isbn']