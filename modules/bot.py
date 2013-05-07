#!/usr/bin/python
import threading, sys

def store(shana, event):
	store = {}
	while True:
		l = shana.recv()
		if l.subject == "STORE":
			store[l.body['name']] = l.body['value']
		elif l.subject == "SET DEFAULT":
			if l.body['name'] in store.keys():
				shana.send(l.sender, "VARIABLE", {'name': l.body['name'], 'value': store[l.body['name']], 'error': None})
			else:
				store[l.body['name']] = l.body['value']
				shana.send(l.sender, "VARIABLE", {'name': l.body['name'], 'value': store[l.body['name']], 'error': "Var set"})
		elif l.subject == "LOAD":
			if l.body['name'] in store.keys():
				shana.send(l.sender, "VARIABLE", {'name': l.body['name'], 'value': store[l.body['name']], 'error': None})
			else:
				shana.send(l.sender, "VARIABLE", {'name': l.body['name'], 'value': None, 'error': "Not set"})

store.name = 'store'
store.wake_on_letter = True

def logger(shana, event):
	levels = {"FATAL": 0, "CRITICAL": 1, "ERROR": 2, "WARNING": 3, "CAUTION": 4, "NOTICE": 5, "STATUS": 6, "DEBUG": 7}
	level = 6
	while True:
		l = shana.inbox.recv()
		if l.subject == "LOG LEVEL":
			if "level" in l.body:
				level = levels[l.body['level']]
			elif "numeric" in l.body:
				level = l.body['numeric']
		else:
			message = l.body
			if message['numeric'] <= level:
				print("%s" % message['text'], file=sys.stdout)

logger.name = 'logger'
logger.service = True
logger.wake_on_letter = True

def version(shana, event):
	shana.say("Shana2 Version 0.1 Beta")
version.commands = ['version']

def reload_module(shana, event):
	print(event.sender)
	shana.send("self.launcher", "RELOAD MODULE", {'names': event.group(2).split(', '), 'sender': event.sender, 'nick': event.nick})
	
reload_module.name = 'reload_module'
reload_module.commands = ['reload']
