#!/usr/bin/env python

def join(phenny, input): 
	"""Join the specified channel. This is an admin-only command."""
	# Can only be done in privmsg by an admin
	print(input.sender)
	if input.sender.startswith('#'): return
	channel = input.group(2)
	#if not key:
	#	phenny.write(['JOIN'], channel)
	#else: 
	phenny.write(['JOIN', channel])
join.commands = ['join', 'j']
join.mode = (True, True, False)
join.group = 'admin'
join.example = '.join #example or .j #example key'

def part(phenny, input): 
	"""Part the specified channel. This is an admin-only command."""
	# Can only be done in privmsg by an admin
	if input.sender.startswith('#'): return
	phenny.write(['PART', input.group(2)])
part.commands = ['part', 'p']
part.mode = (True, True, False)
part.group = 'admin'
part.example = '.part #example'

def quit(phenny, input): 
	"""Quit from the server. This is an owner-only command."""
	# Can only be done in privmsg by the owner
	if input.sender.startswith('#'): return
	if input.group(2): 
		phenny.write(['QUIT'], input.group(2))
	else:
		phenny.write(['QUIT'])
		__import__('os')._exit(0)
quit.commands = ['quit', 'q']
quit.mode = (True, True, False)
quit.group = 'admin'

def config(shana, event):
	key, param = event.group(2).split(" = ", 1)
	d = {}
	for part in reversed(key.split(".")):
		if not d.keys():
			d[part] = param
		else:
			d = {part: d}
	shana.send("self.launcher", "SET CONF", {'config': d})
config.commands = ['config']
config.mode = (True, True, False)
config.group = 'admin'

def msg(phenny, input): 
	# Can only be done in privmsg by an admin
	if input.sender.startswith('#'): return
	a, b = input.group(2), input.group(3)
	if (not a) or (not b): return
	phenny.msg(a, b)
msg.rule = (['msg'], r'(#?\S+) (.+)')
msg.mode = (True, True, False)
msg.group = 'admin'

def me(phenny, input): 
	# Can only be done in privmsg by an admin
	if input.sender.startswith('#'): return
	msg = '\x01ACTION %s\x01' % input.group(3)
	phenny.msg(input.group(2), msg)
me.rule = (['me'], r'(#?\S+) (.*)')
me.mode = (True, True, False)
me.group = 'admin'

def list_modules(phenny, input):
	if input.sender.startswith('#'): return
	phenny.send("self.launcher", "LIST MODULES", {})
	mods = phenny.inbox.recv()
	for mod in mods.body['list'].keys():
		phenny.say("module.%s" % mod)
		for func in mods.body['list'][mod]:
			phenny.say("   |--- %s" % func)
	
list_modules.commands = ['list']
list_modules.mode = (True, True, False)
list_modules.group = 'admin'

def kill(phenny, input):
	if input.sender.startswith('#'): return
	phenny.reply("Not implemented yet")
	return
	if input.group(2):
		phenny.running[input.group(2)] = False
		phenny.say('%s reset' % input.group(2))
	else:
		phenny.say('No such module')
kill.commands = ['kill']
kill.mode = (True, True, False)
kill.group = 'admin'