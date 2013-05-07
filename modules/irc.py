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