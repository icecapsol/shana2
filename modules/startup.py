#!/usr/bin/env python
"""
startup.py - Phenny Startup Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""
import time
def startup(phenny, input): 
	if 'nickserv' in phenny.conf.keys():
		phenny.write(('PRIVMSG', 'NickServ'), 'identify %s' % phenny.conf['nickserv'])
		time.sleep(2)

	for channel in phenny.conf['channels']: 
		phenny.write(('JOIN', channel))

startup.rule = r'(.*)'
startup.event = '251'