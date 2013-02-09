#!/usr/bin/python
import time

def login(phenny, input):
	time.sleep(2)
	phenny.write(("USER", phenny.conf['user'], '+iw', phenny.conf['nick']), phenny.conf['name'])
	phenny.write(["NICK"], phenny.conf['nick'])

login.name = 'login'
login.startup = True

def pong(phenny, input):
	phenny.write(['PONG'], input.group(0))

pong.name = 'pong'
pong.rule = (r'(.*)')
pong.event = ['PING']

def echo(phenny, input):
	phenny.say(input.group(2))

echo.name = 'echo'
echo.commands = ['echo']