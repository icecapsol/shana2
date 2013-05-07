#!/usr/bin/python
import random, re

def quote(shana, event):
	if not event.sender.startswith("#"): return
	quote_re = re.compile('([0-9]+) <(.*?)> (.*)')
	
	quote_file = open("modules/quotes.db", 'r')
	full_quotes = quote_file.readlines()
	quote_file.close()
	
	if not event.group(2):
		shana.say("#%s" % full_quotes[random.randint(0, len(full_quotes)-1)].strip())
		return

	command, split, args = event.group(2).partition(' ')
	quotes = [quote_re.match(quote).groups() for quote in full_quotes]

	if command == 'add':
		if event.group(2).find(": ") == -1:
			shana.say("Name or colon needed  '.quote add nerd: quote'")
			return
		nick, new_q = args.split(': ', 1)
		for quote in [q[2] for q in quotes if q[1] == nick]:
			if new_q == quote:
				shana.say("Quote already exists")
				return
		number = int(quotes[-1][0])+1

		quote_file = open("modules/quotes.db", 'a')
		quote_file.write("%d <%s> %s\n" % (number, nick, new_q))
		quote_file.close()

		shana.reply("quote added (#%s)" % number)
	
	elif command == 'latest':
		shana.say('#%s' % full_quotes[-1].strip())
	elif command == 'total':
		matches = len([quote for quote in quotes if quote[1] == args])
		shana.say("I have %d total quotes by %s" % (matches, args))
	else:
		try:
			iarg = int(command)
			for quote in quotes:
				if int(quote[0]) == iarg:
					shana.say("#%d <%s> %s" % (iarg, quote[1], quote[2].strip()))
					return
			shana.say("Quote %d doesn't exist" % iarg)
		except:
			pick_list = [quote for quote in quotes if quote[1] == event.group(2).strip()]
			if len(pick_list) == 0:
				shana.say("No quotes by that name")
				return
			else:
				q = pick_list[random.randint(0, len(pick_list)-1)]

			shana.say("#%s <%s> %s" % (q[0], q[1], q[2].strip()))

quote.name = 'quote'
quote.commands = ['quote']