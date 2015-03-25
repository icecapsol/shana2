# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
import re

def upc(shana, event):
	url = "http://www.upcdatabase.com/item/%s"
	numbers = re.compile('[0-9]')
	raw = event.group(2)
	upcno = ''.join(numbers.findall(raw))

	if len(upcno) not in [8, 12, 13]:
		shana.reply("invalid UPC")
		return

	try:
		page = urlopen(url % upcno)
	except:
		shana.say("UPC not found")
		return
	soup = BS(page)

	upca = "?"
	ucc = "?"
	desc = "?"
	for item in soup.find_all("tr"):
		if item.td.string == "UPC-A":
			upca = item.find_all("td")[2].img['alt']
		elif item.td.string == "EAN/UCC-13":
			ucc = item.find_all("td")[2].img['alt']
		elif item.td.string == "Description":
			desc = item.find_all("td")[2].string

	shana.say("UPC-A: %s, EAN/UCC-13: %s => %s" % (upca, ucc, desc))

upc.name = "upc"
upc.commands = ['upc']