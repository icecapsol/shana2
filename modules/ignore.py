#!/usr/bin/python

def ignore(phenny, input):
	phenny.send("module.bot.store", "SET DEFAULT", {'name': "module.ignore.list", 'value': []})
	l = phenny.recv()
	if l.subject == "VARIABLE" and l.body['name'] == "module.ignore.list": ilist = l.body['value']
	
	command, sep, nick = input.group(2).partition(" ")
	
	if command == "add":
		if nick in ilist:
			phenny.reply("%s already on ignore list" % nick)
			return
		ilist.append(nick)
		phenny.reply("%s added to ignore list" % nick)
		phenny.send("module.bot.store", "STORE", {'name': "module.ignore.list", 'value': ilist})

	elif command in ["remove", "del"]:
		if nick not in ilist:
			phenny.reply("%s not in ignore list" % nick)
			return
		ilist.remove(nick)
		phenny.reply("%s no longer being ignored" % nick)
		phenny.send("module.bot.store", "STORE", {'name': "module.ignore.list", 'value': ilist})

	elif command == "list":
		if len(ilist) > 0:
			phenny.reply(', '.join(ilist))
		else:
			phenny.reply("No one being ignored")

ignore.commands = ['ignore', 'i']
ignore.group = 'admin'
ignore.mode = (True, True, False)
