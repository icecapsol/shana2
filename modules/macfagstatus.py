#!/usr/bin/env python
import random, time

def f_macfagstatus(phenny, input):
	if not input.group(0).startswith("."): return
	phenny.send("module.bot.store", "SET DEFAULT", {'name': "module.store.last", 'value': 0})
	l = phenny.recv()
	if l.subject == "VARIABLE" and l.body['name'] == "module.store.last": last = l.body['value']
	phenny.send("module.bot.store", "SET DEFAULT", {'name': "module.store.rank", 'value': 0})
	l = phenny.recv()
	if l.subject == "VARIABLE" and l.body['name'] == "module.store.rank": rank = l.body['value']
	phenny.send("module.bot.store", "SET DEFAULT", {'name': "module.store.said", 'value': ''})
	l = phenny.recv()
	if l.subject == "VARIABLE" and l.body['name'] == "module.store.said": said = l.body['value']
	phenny.send("module.bot.store", "SET DEFAULT", {'name': "module.store.cooldown", 'value': 0})
	l = phenny.recv()
	if l.subject == "VARIABLE" and l.body['name'] == "module.store.cooldown": cooldown = l.body['value']
	"""phenny.vars['macfagstatus'].setdefault('last', 0)
	phenny.vars['macfagstatus'].setdefault('rank', 0)
	phenny.vars['macfagstatus'].setdefault('said', '')
	phenny.vars['macfagstatus'].setdefault('cooldown', 0)"""
	
	status = random.randint(0, 11)
	ut_told = ['4DOUBLE TOLD', 
	'4TRIPLE TOLD', 
	'4ICE TOLD', 
	'4MULTI TOLD', 
	'4TOLD SPICE', 
	'0415% OFF AT TOLD NAVY',
	'4TOLDS NEW ROMAN', 
	'4BILLY MAYS TOLD', 
	'4TEXAS TOLD\'EM', 
	'4ENNIO MORRICONE\'s ECSTASY OF TOLD',
	'4TOLDSTONE CREAMERY',
	'4MEGA TOLD', 
	'4USER WAS TOLD FOR THIS BOAST', 
	'4TOLD SPICE', 
	'4STONE TOLD STEVE AUSTIN', 
	'4ULTRA TOLD', 
	'4BABY IT\'S TOLD OUTSIDE', 
	'4M-M-M-MONSTER TOLD', 
	'4GREAT CALIFORNIA TOLD RUSH', 
	'4LUDACRIS TOLD', 
	'4ALL GLORY TO THE HYPNOTOLD',
	'4THE WASHINGTOLD MONUMENTALLY', 
	'4H O L Y S H I T F U C K I N G T O L D', 
	'4ALL GLORY TO THE HYPNOTOLD', 
	'4ONE WORD: FORCED INDICATION OF TOLD THREAD OVER']
	not_told = ['.iosysfagstatus', '.udongefagstatus', '.elifagstatus', '.eyeohsysfagstatus', '.iodongfagstatus']
	if input.group(0).strip() in not_told:
		if status == 5:
			phenny.msg(input.sender, "PENDING...")
			time.sleep(5)
			phenny.msg(input.sender, "3NOT TOLD")
		else:
			phenny.say('NOT TOLD')
	else:
		if time.time() - last < 30 and input.group(0).strip() == said and cooldown < time.time():
			phenny.say(ut_told[rank])
			phenny.send("module.bot.store", "STORE", {'name': "module.store.last", 'value': time.time()})
			#phenny.vars['macfagstatus']['last'] = time.time()
			phenny.send("module.bot.store", "STORE", {'name': "module.store.rank", 'value': rank+1})
			#phenny.vars['macfagstatus']['rank'] += 1
			if rank+1 == len(ut_told):
				phenny.send("module.bot.store", "STORE", {'name': "module.store.cooldown", 'value': time.time()+240})
				#phenny.vars['macfagstatus']['cooldown'] = time.time()+240
				phenny.send("module.bot.store", "STORE", {'name': "module.store.rank", 'value': 0})
				#phenny.vars['macfagstatus']['rank'] = 0
			return
		elif not cooldown < time.time():
			phenny.say("Told-o-meter cooling down")
			return
		else:
			phenny.send("module.bot.store", "STORE", {'name': "module.store.last", 'value': time.time()})
			#phenny.vars['macfagstatus']['last'] = time.time()
			phenny.send("module.bot.store", "STORE", {'name': "module.store.rank", 'value': 0})
			#phenny.vars['macfagstatus']['rank'] = 0
			phenny.send("module.bot.store", "STORE", {'name': "module.store.said", 'value': input.group(0).strip()})
			#phenny.vars['macfagstatus']['said'] = input.group(0)
		
		if status == 5:
			phenny.msg(input.sender, "PENDING...")
			time.sleep(5)
			phenny.msg(input.sender, "4TOLD")
		elif status == 6 and input.group(0) == '.macfagstatus':
			phenny.msg(input.sender, "PENDING...")
			time.sleep(5)
			phenny.msg(input.sender, "SIGNAL LOST")
		else:
			phenny.say('4TOLD')

f_macfagstatus.name = 'macfagstatus'
f_macfagstatus.commands = ['\S*fagstatus']
f_macfagstatus.priority = 'low'