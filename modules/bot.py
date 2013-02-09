#!/usr/bin/python
import threading

def store(phenny, input):
	store = {}
	while True:
		l = phenny.inbox.recv()
		if l.subject == "STORE":
			store[l.body['name']] = l.body['value']
		elif l.subject == "SET DEFAULT":
			if l.body['name'] in store.keys():
				phenny.send(l.sender, "VARIABLE", {'name': l.body['name'], 'value': store[l.body['name']], 'error': None})
			else:
				store[l.body['name']] = l.body['value']
				phenny.send(l.sender, "VARIABLE", {'name': l.body['name'], 'value': store[l.body['name']], 'error': "Var set"})
		elif l.subject == "LOAD":
			if l.body['name'] in store.keys():
				phenny.send(l.sender, "VARIABLE", {'name': l.body['name'], 'value': store[l.body['name']], 'error': None})
			else:
				phenny.send(l.sender, "VARIABLE", {'name': l.body['name'], 'value': None, 'error': "Not set"})

store.name = 'store'
store.startup = True

def logger(phenny, input):
	levels = {"FATAL": 0, "CRITICAL": 1, "ERROR": 2, "WARNING": 3, "CAUTION": 4, "NOTICE": 5, "STATUS": 6, "DEBUG": 7}
	level = 5
	while True:
		l = phenny.inbox.recv()
		if l.subject == "LOG LEVEL":
			if "level" in l.body:
				level = levels[l.body['level']]
			elif "numeric" in l.body:
				level = l.body['numeric']
		else:
			message = l.body
			if message['numeric'] > 3:
				print(message['text'], file=sys.stderr)
			else:
				print(message['text'], file=sys.stdout)
	
logger.name = 'logger'
logger.daemon = True

def reload_module(phenny, input):
	print(input.sender)
	phenny.send("self.launcher", "RELOAD MODULE", {'names': input.group(2).split(', '), 'sender': input.sender, 'nick': input.nick})
	
reload_module.name = 'reload_module'
reload_module.commands = ['reload']