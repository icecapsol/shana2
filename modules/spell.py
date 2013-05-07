#!/usr/bin/env python
import re, enchant

def sp(shana, event):
	if event.group(2):
		eng = enchant.Dict("en_US")
		if eng.check(event.group(2).strip()):
			shana.reply("09%s" % event.group(2))
		else:
			shana.reply(', '.join(eng.suggest(event.group(2))[:3]))

sp.name = 'sp'
sp.commands = ['sp', 'spell']

def psp(shana, event):
	eng = enchant.Dict("en_US")
	
	corrections = []
	for check in event.searches:
		try: correct = eng.suggest(re.search(r'\S*\Z', check).group())[0]
		except: correct = "?_?"
		if correct.lower() == re.search(r'\S*\Z', check).group().lower():
			corrections.append("09%s" % correct)
		else:
			corrections.append(correct)
	
	shana.reply('; '.join(corrections))

psp.name = 'psp'
psp.rule = (r'\S+\(sp\)')