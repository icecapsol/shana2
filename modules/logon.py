#!/usr/bin/env python
import time

def f_logon(phenny, input): 
	if not input.admin: 
		phenny.say("Lowly commoners can't tell me what to do! Hmpf!")
		return
	
	ignorefile = open('modules/ignore.ini', 'r')
	ignorelines = ignorefile.readlines()
	ignorefile.close()
	for ignore in ignorelines:
		phenny.ignore.append(ignore.strip())
	
	phenny.write(('PRIVMSG', 'Chanserv'), 'HALFOP')
f_logon.commands = ['logon']
f_logon.priority = 'low'

def f_identify(phenny, input):
	if not input.admin: 
		phenny.say("Lowly commoners can't tell me what to do! Hmpf!")
		return
	phenny.msg('NickServ', "IDENTIFY flamehaze")
	
f_identify.commands = ['identify']
f_identify.priority = 'low'