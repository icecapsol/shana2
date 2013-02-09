#!/usr/bin/env python
from urllib.request import urlopen
import re

def f_un404_cache(phenny, input):
	#httppattern = re.compile('(http[s]?:\/\/\S+)', re.M)
	#urls = httppattern.findall(input.group(0))
	
	for url in input.searches:
		if url.find("images.4chan.org/") != -1:
			cache = urlopen("http://gtrack.org/image_cache.php?mode=cache&url=%s" % url)
			cache.close()

f_un404_cache.name = 'un404'
f_un404_cache.rule = (r'http[s]?:\/\/\S+')
f_un404_cache.priority = 'low'


def f_un404(phenny, input):
	phenny.reply("http://gtrack.org/imgcache/%s" % input.group(2))
	pass

f_un404.name = 'un404'
f_un404.commands = ['un404']
f_un404.priority = 'low'