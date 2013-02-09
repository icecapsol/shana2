#!/usr/bin/env python
import socket, re, enchant

def f_sp(phenny, input):
	if input.group(2):
		eng = enchant.Dict("en_US")
		if eng.check(input.group(2).strip()):
			phenny.reply("09%s" % input.group(2))
		else:
			phenny.reply(', '.join(eng.suggest(input.group(2))[:3]))

f_sp.name = 'sp'
f_sp.commands = ['sp', 'spell']
f_sp.priority = 'low'

def f_psp(phenny, input):
	#if input.group(0).find('(sp)') != -1:
	eng = enchant.Dict("en_US")
	
	corrections = []
	for check in input.searches:
		try: correct = eng.suggest(re.search(r'\S*\Z', check).group())[0]
		except: correct = "?_?"
		if correct.lower() == re.search(r'\S*\Z', check).group().lower():
			corrections.append("09%s" % correct)
		else:
			corrections.append(correct)
	
	phenny.reply('; '.join(corrections))

f_psp.name = 'psp'
f_psp.rule = (r'\S+\(sp\)')
f_psp.priority = 'low'