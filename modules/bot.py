#!/usr/bin/python
import threading, sys, datetime

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

class Output:
	def __init__(self, name, output, mask=[], module_mask=[]):
		self.name = name
		self.set_mask(mask)
		self.m_mask = module_mask
		self.colors = {"BLACK": ("\x1b[30m", "\x1b[0m"), "DARK RED": ("\x1b[31m", "\x1b[0m"),
					    "DARK GREEN": ("\x1b[32m", "\x1b[0m"), "DARK YELLOW": ("\x1b[33m", "\x1b[0m"),
					    "DARK BLUE": ("\x1b[34m", "\x1b[0m"), "DARK MAGENTA": ("\x1b[35m", "\x1b[0m"), 
					    "DARK CYAN": ("\x1b[36m", "\x1b[0m"), "LIGHT GREY": ("\x1b[37m", "\x1b[0m"),
					    "DARK GREY": ("\x1b[30m", "\x1b[0m"), "RED": ("\x1b[31;1m", "\x1b[0m"),
					    "GREEN": ("\x1b[32;1m", "\x1b[0m"), "YELLOW": ("\x1b[33;1m", "\x1b[0m"), 
					    "BLUE": ("\x1b[34;1m", "\x1b[0m"), "MAGENTA": ("\x1b[35;1m", "\x1b[0m"),
					    "CYAN": ("\x1b[36;1m", "\x1b[0m"), "WHITE": ("\x1b[37;1m", "\x1b[0m")}
		self.level_profiles = {"FATAL": "MAGENTA", "CRITICAL": "RED", "ERROR": "DARK RED", "WARNING": "YELLOW",
						"CAUTION": "DARK YELLOW", "NOTICE": "CYAN", "STATUS": "LIGHT GREY", "DEBUG": "WHITE"}
		self.set_output(output)
	def set_mask(self, mask):
		self.levels = [level for level in ["FATAL", "CRITICAL", "ERROR", "WARNING", "CAUTION", "NOTICE", "STATUS", "DEBUG"] if not level in mask]
	def set_output(self, output):
		if output == "stdout":
			self.output = sys.stdout
		elif output == "stderr":
			self.output = sys.stderr
		elif output.startswith("file:"):
			self.output = open(output.split(":", 1)[1], "a")
	
	def colorize(self, text, level):
		return "%s%s%s" % (self.colors[self.level_profiles[level]][0], text, self.colors[self.level_profiles[level]][1])
	
	def filter_line(self, message):
		if message['level'] not in self.levels: return
		if message['module'] in self.m_mask: return
		print("%s %s" % (datetime.datetime.fromtimestamp(message['time']).strftime("%b %d %H:%M:%S"),
			self.colorize("[%s] %s: %s" % (message['level'], message['module'], message['text']), message['level'])), file=self.output)

def logger_manager(shana, event):
	command, s, name = event.group(2).partition(" ")
	if name: name, s, args = name.partition(" ")
	
	if command == "new":
		shana.send("module.bot.logger", "NEW", {'name': name, 'output': args})
		l = shana.recv()
		if l.body['error']:
			shana.say("Error: %s" % l.body['error'])
		else:
			shana.say("Output created")
	elif command == "modify":
		try: argdict = dict([arg.split("=") for arg in args.split()])
		except: return
		argdict['name'] = name
		shana.send("module.bot.logger", "OUTPUT", argdict)
		l = shana.recv()
		if l.body['error']:
			shana.say("Error: %s" % l.body['error'])
		else:
			shana.say("Output modified")
	elif command == "list":
		shana.send("module.bot.logger", "LIST", {})
		l = shana.recv(subject="LIST")
		shana.say("Outputs: %s" % l.body['list'])
	elif command == "delete":
		shana.send("module.bot.logger", "NEW", {'name': name})
		l = shana.recv()
		if l.body['error']:
			shana.say("Error: %s" % l.body['error'])
		else:
			shana.say("Output deleted")
logger_manager.name = 'log output manager'
logger_manager.commands = ['logger']

def logger(shana, event):
	lines = []
	outputs = []
	for out in shana.conf['outputs']:
		outputs.append(Output(out['name'], out['output'], out.get('mask', []), out.get('module mask', [])))
	while True:
		l = shana.inbox.recv()
		if l.subject == "OUTPUT":
			out = [out for out in outputs if out.name == l.body['name']]
			if len(out) == 0:
				shana.send(l.sender, "OUTPUT", {"error": "name not found"})
				continue
			if 'output' in l.body.keys():
				out[0].set_output(l.body['output'])
			if 'mask' in l.body.keys():
				out[0].set_mask(l.body['mask'].split(","))
			if 'module_mask' in l.body.keys():
				out[0].m_mask = l.body['module_mask'].split(",")
			shana.send(l.sender, "OUTPUT", {"error": None})
		elif l.subject == "NEW":
			out = [out for out in outputs if out.name == l.body['name']]
			if len(out) > 0:
				shana.send(l.sender, "OUTPUT", {"error": "output already exists"})
				continue
			outputs.append(Output(l.body['name'], l.body['output'], l.body.get('mask', []), l.body.get('module mask', [])))
		elif l.subject == "LIST":
			shana.send(l.sender, "LIST", {'list': ' '.join([out.name for out in outputs])})
		elif l.subject == "DELETE":
			out = [out for out in outputs if out.name == l.body['name']]
			if len(out) == 0:
				shana.send(l.sender, "OUTPUT", {"error": "name not found"})
				continue
			outputs.remove(out)
		elif l.subject == "LOG":
			message = l.body
			if 'level' not in message.keys():
				message['level'] = ["FATAL", "CRITICAL", "ERROR", "WARNING", "CAUTION", "NOTICE", "STATUS", "DEBUG"][message['numeric']]
			lines.append(message)
			if len(lines) > 5000: lines.pop(0)
			
			for out in outputs:
				out.filter_line(message)

logger.name = 'logger'
logger.service = True
logger.wake_on_letter = True

def version(shana, event):
	shana.say("Shana2 Version %s" % shana.conf.get('version', '???'))
version.commands = ['version']

def reload_module(shana, event):
	print(event.sender)
	shana.send("self.launcher", "RELOAD MODULE", {'names': event.group(2).split(', '), 'sender': event.sender, 'nick': event.nick})
	
reload_module.name = 'reload_module'
reload_module.commands = ['reload']
