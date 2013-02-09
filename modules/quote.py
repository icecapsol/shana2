#!/usr/bin/python
import random, re, enchant

def f_quote(phenny, input):
	if not input.sender.startswith("#"): return
	if not input.group(2):
		quote_file = open("modules/quotes.db", 'r')
		full_quotes = quote_file.readlines()
		quote_file.close()

		qot = random.randint(0, len(full_quotes)-1)
		say_quote = full_quotes[qot]

		phenny.say("#%s" % say_quote.replace('JxcelDolghmQ', 'jynx'))
		return
	else:
		command, split, args = input.group(2).partition(' ')

		quote_file = open("modules/quotes.db", 'r')
		full_quotes = quote_file.readlines()
		quote_file.close()

	if command == 'add':
		if input.group(2).find(": ") == -1:
			phenny.say("Name or colon needed  '.quote add nerd: quote'")
			return
		for quote in full_quotes:
			if "<"+args.partition(': ')[0].replace('JxcelDolghmQ', 'jynx')+"> "+args.partition(': ')[2]+'\n' in quote.partition(" ")[2]:
				phenny.say("Quote already exists")
				return
		number = int(full_quotes[-1].partition(" ")[0])+1

		quote_file = open("modules/quotes.db", 'a')
		quote_file.write("%s <%s> %s\n" % (number, args.partition(': ')[0].replace('JxcelDolghmQ', 'jynx'), args.partition(": ")[2]))
		quote_file.close()

		phenny.reply("quote added (#%s)" % number)

	elif command == 'del':
		if not input.admin: return
		try:
			iarg = int(args)
			for quote in full_quotes:
				if int(quote.partition(" ")[0]) == iarg:
					full_quotes.pop(full_quotes.index(quote))
					phenny.say("Quote %s removed." % iarg)
					return
			phenny.say("Quote %s doesn't exist" % iarg)
			return
		except:
			phenny.say(".quote del <quote number>")
			return
		
		quote_file = open("modules/quotes.db", 'w')
		quote_file.writelines(quotes)
		quote_file.close()
		phenny.say(str(records_gone)+" quote(s) removed.")
	
	elif command == 'latest':
		phenny.say('#%s' % full_quotes[-1])

	else:
		try:
			iarg = int(command)
			for quote in full_quotes:
				if int(quote.partition(" ")[0]) == iarg:
					phenny.say("#%s" % quote)
					return
			phenny.say("Quote %s doesn't exist" % iarg)
		except:
			pick_list = []
			for line in full_quotes:
				if line.partition('> ')[0].partition('<')[2] == input.group(2).strip():
					pick_list.append(line)
			if len(pick_list) == 0:
				phenny.say("No quotes by that name")
				return
			else:
				qot = random.randint(0, len(pick_list)-1)
				say_quote = pick_list[qot]

			phenny.say("#%s" % say_quote)

f_quote.name = 'quote'
f_quote.commands = (['quote'])
f_quote.priority = 'low'