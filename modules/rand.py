#!/usr/bin/env python
#coding=utf-8
import random
from ftplib import FTP

def eight_ball(shana, event):
	magicResponses = ["As I see it, yes", "It is certain", "It is decidedly so", "Most likely", "Outlook good", "Signs point to yes", "Without a doubt", "Yes", "Yes - definitely", "You may rely on it", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful "]

	shana.reply(magicResponses[random.randint(0, len(magicResponses)-1)])

eight_ball.name = "8ball"
eight_ball.commands = ['8ball']

def fortune(shana, event):
	fortunes = ["Good Luck", "Bad Luck", "You will meet a dark handsome stranger", "Godly Luck", "ｷﾀ━━━━━━(ﾟ∀ﾟ)━━━━━━!!!!!"]

	shana.reply(fortunes[random.randint(0, len(fortunes)-1)])
fortune.name = "fortune"
fortune.commands = ['fortune']

def rand(shana, event):
	if not event.group(2):
		shana.reply(str(random.randint(1, 100)))
		return
	args = event.group(2).split()
	if len(args) == 1:
		try:
			shana.reply(str(random.randint(1, int(args[0]))))
		except:
			shana.reply("Need an integer greater than 1")
	elif len(args) == 2:
		try:
			shana.reply(str(random.randint(int(args[0]), int(args[1]))))
		except:
			shana.reply("A and B need to be integers such that A < B")
rand.name = "rand"
rand.commands = ['rand', 'random']

def redtube(shana, event):
	shana.reply("http://www.redtube.com/%s" % str(random.randint(1, 10000)))
redtube.name = "redtube"
redtube.commands = ['redtube']

def kick(shana, event):
	victims = event.group(2).split()
	shana.write(['KICK', event.sender, victims[random.randint(0, len(victims)-1)]])
kick.name = "kick"
kick.commands = ['randkick']
kick.group = 'admin'

def choice(shana, event):
	choices = event.group(2).split(" or ")
	shana.reply(choices[random.randint(0, len(choices)-1)])
choice.name = "choice"
choice.commands = ['choose', 'choice']
