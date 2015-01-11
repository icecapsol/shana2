#!/usr/bin/python
import time

def login(shana, event):
	shana.write(("USER", shana.conf['user'], '+iw', shana.conf['nick']), shana.conf['name'])
	shana.write(["NICK"], shana.conf['nick'])

login.name = 'login'
login.wake_on_letter = True

def pong(shana, event):
	shana.write(['PONG'], event.group(0))

pong.name = 'pong'
pong.rule = (r'(.*)')
pong.event = ['PING']

def echo(shana, event):
	shana.say(event.group(2))

echo.name = 'echo'
echo.commands = ['echo']

def topic(shana, event):
	shana.send("module.bot.store", "PUT", {'name': "%s topic" % event.args[1], 'value': event.group(0)})
	l = shana.recv(subject=["PUT",])

topic.name = 'topic'
topic.rule = (r'(.*)')
topic.event = ['332']

def change_topic(shana, event):
	channel, section, text = event.group(2).split(' ', 2)

	if not event.admin and channel == "#general" and int(section) not in [1, 4]:
		shana.say("Denied: Check your privilege")
		return

	shana.send("module.bot.store", "GET", {'name': "%s topic" % channel})
	shana.log("%s topic" % channel, "NOTICE")
	l = shana.recv(subject=["GET",])

	topic = l.body['value']
	sections = topic.split(" | ")
	if int(section) >= len(sections):
		shana.say("No such slot")
		return
	sections[int(section)] = text

	shana.write(["TOPIC", channel], " | ".join(sections))

change_topic.name = 'change_topic'
change_topic.commands = ['topic']