#!/usr/bin/env python
import codecs

def rot13(shana, event):
	enc = codecs.getencoder( "rot-13" )
	try: shana.say(enc(event.group(2))[0])
	except: shana.say("non ASCII character found")
	
rot13.name = 'rot13'
rot13.commands = ['rot13']

def rot47(shana, event):
	new = ""
	for loop in range(len(event.group(2))):
		if event.group(2)[loop] == " ": new += " "
		else: new += chr(((ord(event.group(2)[loop]) - 33 + 47) % 94) + 33)
	shana.say(new)
	
rot47.name = 'rot47'
rot47.commands = ['rot47']