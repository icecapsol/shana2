#!/usr/bin/env python
from urllib.request import urlopen

def un404_cache(shana, event):
	for url in event.searches:
		if url.find("images.4chan.org/") != -1:
			cache = urlopen("http://gtrack.org/image_cache.php?mode=cache&url=%s" % url)
			cache.close()

un404_cache.name = 'un404_cache'
un404_cache.rule = (r'http[s]?:\/\/\S+')


def un404(shana, event):
	shana.reply("http://gtrack.org/imgcache/%s" % event.group(2))
	pass

un404.name = 'un404'
un404.commands = ['un404']