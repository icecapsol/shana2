#!/usr/bin/env python
import time, codecs

def f_rot13(phenny, input):
	import codecs
	enc = codecs.getencoder( "rot-13" )
	try: phenny.say(enc(input.group(2))[0])
	except: phenny.say("non ASCII character found")
	
f_rot13.name = 'rot13'
f_rot13.commands = ['rot13']
f_rot13.priority = 'low'

def f_rot47(phenny, input):
	#try:
	new = ""
	for loop in range(len(input.group(2))):
		if input.group(2)[loop] == " ": new += " "
		else: new += chr(((ord(input.group(2)[loop]) - 33 + 47) % 94) + 33)
	phenny.say(new)
	#except: phenny.say("non ASCII character found")
	
f_rot47.name = 'rot47'
f_rot47.commands = ['rot47']
f_rot47.priority = 'low'