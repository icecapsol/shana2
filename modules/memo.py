#!/usr/bin/python
import time

def memo(shana, event):
	nick, message = event.group(2).split(": ", 1)
	channel = event.sender

	locked = False
	while not locked:
		shana.send("module.bot.store", "ACQUIRE", {"name": "%s.%s" % (nick, channel)})
		l = shana.recv(subject="ACQUIRE")
		if l.body['error']:
			time.sleep(1)
			continue
		locked = True
	value = l.body['value']
	if not value:
		value = []
	value.append((event.nick, message))

	shana.send("module.bot.store", "PUT", {"name": "%s.%s" % (nick, channel), "value": value})
	shana.send("module.bot.store", "RELEASE", {"name": "%s.%s" % (nick, channel)})
	shana.send("self.launcher", "TRIGGER", {"action": "register",
									  "module": "module.memo.tell",
									  "definition": {"name": "%s-%s.%s.%d" % (event.nick, nick, channel, int(time.time())),
												  "event": ("JOIN", "PRIVMSG"),
												  "nick": (nick,),
												  "sender": (channel,),
												  "expire": 1
												  }
									  })
	l = shana.recv(subject="TRIGGER")
	if l.body['reply']:
		shana.say("Message saved for %s" % nick)
	else:
		shana.say("Couldn't save message")

memo.name = "memo"
memo.commands = ["memo", "tell"]

def tell(shana, event):
	nick = event.nick
	channel = event.sender

	locked = False
	while not locked:
		shana.send("module.bot.store", "ACQUIRE", {"name": "%s.%s" % (nick, channel)})
		l = shana.recv(subject="ACQUIRE")
		if l.body['error']:
			time.sleep(1)
			continue
		locked = True
	value = l.body['value']

	shana.send("module.bot.store", "PUT", {"name": "%s.%s" % (nick, channel), "value": []})
	shana.send("module.bot.store", "RELEASE", {"name": "%s.%s" % (nick, channel)})

	for nick, message in value:
		shana.msg(channel, "To %s: %s" % (nick, message))
tell.name = "tell"