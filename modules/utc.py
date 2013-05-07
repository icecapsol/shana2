#!/usr/bin/python
import time

def convert(shana, event):
	args = event.group(2)
	if not args:
		shana.reply("%s UTC %d UNIX" % (time.asctime(time.gmtime()), int(time.time())))
		return
	try:
		seconds = int(args)
		utc = time.gmtime(seconds)
		shana.reply(time.asctime(utc)+" UTC")
	except:
		shana.say(".time [UNIX Timestamp]")

convert.name = 'time'
convert.commands = ['time']