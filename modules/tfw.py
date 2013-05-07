#!usr/bin/env python
from bs4 import BeautifulSoup as BS
import urllib.request
import urllib.parse

def tfw(shana, event):
	q = event.group(2)
	
	if not q:
		shana.reply("Usage: .weather <location>")
		return
	q = urllib.parse.quote(q)
	q = q.replace(" ", "+")

	soup = BS(urllib.request.urlopen("http://thefuckingweather.com/?zipcode="+q))
	try:
		res = "%s?! %s" % (soup.find(class_="temperature").get_text(), soup.find(class_="remark").get_text())
		shana.say(res)
	except:
		shana.reply(soup.find(class_="large").get_text())

tfw.name = 'tfw'
tfw.commands = ['tfw']