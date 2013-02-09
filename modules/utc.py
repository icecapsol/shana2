#!/usr/bin/python
import time, calendar

def f_convert(phenny, input):
	args = input.group(2)
	if not args:
		phenny.reply(time.asctime(time.gmtime())+" UTC")
		return
	try:
		seconds = int(args)
		utc = time.gmtime(seconds)
		phenny.reply(time.asctime(utc)+" UTC")
	except:	
		phenny.say(".time [UNIX Timestamp]")
		

f_convert.name = 'time'
f_convert.commands = (['time'])
f_convert.priority = 'low'