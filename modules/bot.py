#!/usr/bin/python
import sys
import asyncore, asynchat, errno, ssl, socket, select, time, traceback, threading, signal
import re
from datetime import datetime as dt

def communicator(shana, event):
	class Listener(asynchat.async_chat):
		def __init__(self, bot):
			asynchat.async_chat.__init__(self)
			self.set_terminator(b'\n')
			self.buffer = b''
			self.bot = bot
			self.reload_config(bot.conf)
		
		def reload_config(self, config):
			self.config = config
			self.host = config['host']
			self.port = config['port']
			self.ssl = False if 'ssl' not in config.keys() else config['ssl']
			
			if self.ssl:
				self.send = self._ssl_send
				self.recv = self._ssl_recv
			else:
				self.send = asynchat.async_chat.send
				self.recv = asynchat.async_chat.recv
				
		def _ssl_send(self, data):
			try:
				result = self.write(data)
				return result
			except ssl.SSLError as why:
				if why[0] in (asyncore.EWOULDBLOCK, errno.ESRCH):
					return 0
				else:
					raise ssl.SSLError(why)
				return 0
		
		def _ssl_recv(self, buffer_size):
			try:
				data = self.read(buffer_size)
				if not data:
					self.handle_close()
					return ''
				return data
			except ssl.SSLError as why:
				if why[0] in (asyncore.ECONNRESET, asyncore.ENOTCONN,
						  asyncore.ESHUTDOWN):
					self.handle_close()
					return ''
				elif why[0] == errno.ENOENT:
					return ''
				else:
					raise

		def initiate_connect(self): 
			self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
			self.bot.log("Connecting to %s %s" % (self.host, self.port), "STATUS")
			try:
				self.connect((self.host, int(self.port)))
				self.reconnect_wait = 10
			except:
				self.bot.log("%s: %s" % sys.exc_info()[:2], "ERROR")
				self.reconnect_wait = (self.reconnect_wait * 2) % 240
				
		def handle_connect(self): 
			if self.ssl:
				self.ssl_sock = ssl.wrap_socket(self.socket, do_handshake_on_connect=False)
				self.set_socket(self.ssl_sock)
				while True:
					try:
						self.socket.do_handshake()
						break
					except ssl.SSLError as err:
						if err.args[0] == ssl.SSL_ERROR_WANT_READ:
							select.select([self.socket], [], [])
						elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
							select.select([], [self.socket], [])
						else:
							raise
			self.bot.send("module.irc.login", "CONNECT", {'message': "new connection"})
		def handle_close(self):
			if self.reconnect_wait == 10:
				self.bot.log("Connection to %s lost. Reconnecting in %d seconds" % (self.host, self.reconnect_wait), "NOTICE")
			else:
				self.bot.log("Connecting to %s failed. Retrying in %d seconds" % (self.host, self.reconnect_wait), "WARNING")
			self.close()
			time.sleep(self.reconnect_wait)
			self.initiate_connect()

		def handle_error(self):
			for line in traceback.format_exc().split('\n'):
				self.bot.log(line, "ERROR")
			self.bot.log("Send buffer: %s" % self.buffer, "ERROR")

		def collect_incoming_data(self, data): 
			self.buffer += data
		def found_terminator(self):
			line = self.buffer
			if line.decode().endswith('\r'): 
				line = line[:-1]
			self.buffer = b''
			self.bot.log("New line: %s" % line.decode(), "DEBUG")
			self.bot.send("module.bot.parser", "NEW LINE", {'line': line.decode()})
		def run(self):
			self.initiate_connect()
			try: asyncore.loop()
			except KeyboardInterrupt: 
				sys.exit(0)
	class Speaker():
		def __init__(self, bot, comm):
			self.bot = bot
			self.comm = comm

		def run(self):
			while True:
				letter = self.bot.recv()
				if letter.subject == "NEW IRC OUTPUT":
					try: self.comm.push(letter.body['message'].encode('utf-8'))
					except:
						try:
							self.comm.push(letter.body['message'].encode('cp1252'))
							self.bot.log("Badly encoded characters in message:", "WARNING")
							self.bot.log(letter.body['message'], "WARNING")
						except:
							for line in traceback.format_exc().split('\n'):
								self.bot.log(line, "ERROR")
							self.bot.log(letter.body['message'], "ERROR")
					time.sleep(0.1)
				elif letter.subject == "RELOAD":
					self.comm.reload_config(letter.body['config'])
					self.bot.log("Reloading Listener's configuration", "NOTICE")
	
	def die(self, sig, frame):
		sys.exit(0)
		
	listener = Listener(shana)
	speaker = Speaker(shana, listener)
	signal.signal(signal.SIGINT, die)
	
	t = threading.Thread(target=listener.run, args=())
	t.start()
	speaker.run()
communicator.startup = True
communicator.service = True

def parser(shana, event):
	def new_line(l):
		irc_re = re.compile(r'([^!]*)!?([^@]*)@?(.*)')
		line = l.body['line']
		shana.log("new line '%s'" % line.strip(), "DEBUG")
		
		if line.startswith(':'): 
			source, line = line[1:].split(' ', 1)
		else: source = None

		if ' :' in line: 
			argstr, text = line.split(' :', 1)
		else: argstr, text = line, ''
		args = argstr.split()
		
		match = irc_re.match(source or '')
		nick, user, host = match.groups()

		if len(args) > 1: 
			target = args[1]
		else: target = None
		sender = {shana.conf['nick']: nick, None: None}.get(target, target)
		args = tuple([text] + args)
		
		shana.send("module.bot.generator", "NEW IRC DATA", {'nick': nick, "user": user, "host": host, "sender": sender, "args": args})
	
	shana.register(new_line, "NEW LINE")
	shana.loop()
parser.startup = True
parser.service = True

class Event():
	def __init__(self, text, data, bytes, event, args, config):
		#s = str.__new__(cls, text)
		self.sender = data['sender']
		self.nick = data['nick']
		self.host = data['host']
		self.user = data['user']
		self.event = event
		self.bytes = bytes
		self.match = None
		self.search = None
		self.searches = None
		self.group = None #match.group
		self.groups = None #match.groups
		self.args = args
		self.admin = self.nick in config['groups']['admin']
		self.owner = self.nick == config['groups']['sysop']
		if self.nick.lower() in config['passwd']:
			self.username = self.nick.lower()
		else:
			self.username = 'nobody'
		self.ugroups = config['passwd'].get(self.username, ['nobody'])
		
def generator(shana, event):
	def generate(l):
		args = l.body['args']
		event = Event(args[0], l.body, args[0], args[1], args[2:], shana.conf)
		shana.send("self.launcher", "NEW EVENT", {'event': event})
	shana.register(generate, "NEW IRC DATA")
	
	shana.loop()
generator.startup = True
generator.service = True

def store(shana, event):
	records = {}
	while True:
		l = shana.recv()
		if l.subject == "GET":
			rname = l.body['name']
			record = records.get(rname, {})

			shana.send(l.sender, "GET", {'name': rname, 'value': record.get('value', None), 'error': None})

		elif l.subject == "PUT":
			rname = l.body['name']
			record = records.get(rname, {})
			expire = record.get("lock-expire", 0)
			if expire > int(time.time()):
				owner = record.get("lock-owner", '')
				if l.sender != owner:
					shana.send(l.sender, "PUT", {'name': rname, 'value': record.get('value', None), 'error': "locked"})
					continue
			record['value'] = l.body['value']
			records[rname] = record
			shana.send(l.sender, "PUT", {'name': rname, 'value': record.get('value', None), 'error': None})

		if l.subject == "ACQUIRE":
			rname = l.body['name']
			record = records.get(rname, {})
			owner = record.get("lock-owner", '')
			if owner and owner != l.sender:
				shana.send(l.sender, "ACQUIRE", {'name': rname, 'value': record.get('value', None), 'error': "locked"})
			else:
				record['lock-owner'] = l.sender
				record['lock-expire'] = int(time.time()) + 5 * 60
				records[rname] = record
				shana.send(l.sender, "ACQUIRE", {'name': rname, 'value': record.get('value', None), 'error': None})

		elif l.subject == "RELEASE":
			rname = l.body['name']
			record = records.get(rname, {})
			expire = record.get("lock-expire", 0)
			if expire > int(time.time()):
				owner = record.get("lock-owner", '')
				if l.sender != owner:
					shana.send(l.sender, "RELEASE", {'name': rname, 'value': record.get('value', None), 'error': "locked"})
					continue
			record['value'] = l.body['value']
			record['lock-owner'] = ''
			record['lock-expire'] = 0
			records[rname] = record
			shana.send(l.sender, "RELEASE", {'name': rname, 'value': record.get('value', None), 'error': None})

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
		print("%s %s" % (dt.fromtimestamp(message['time']).strftime("%b %d %H:%M:%S"),
			self.colorize("[%(level)s] %(module)s: %(text)s" % message, message['level'])), file=self.output)

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
	shana.send("module.bot.launcher", "RELOAD MODULE", {'names': event.group(2).split(', '), 'sender': event.sender, 'nick': event.nick})
	
reload_module.name = 'reload_module'
reload_module.commands = ['reload']
