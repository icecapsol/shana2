#!/usr/bin/env python
import time
def startup(shana, event):
	if 'nickserv' in shana.conf.keys():
		shana.write(('PRIVMSG', 'NickServ'), 'identify %s' % shana.conf['nickserv'])
		time.sleep(2)

	for channel in shana.conf['channels']:
		shana.write(('JOIN', channel))

startup.name = "startup"
startup.event = '251'