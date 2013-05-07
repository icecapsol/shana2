#!/usr/bin/env python
import random, time

def macfagstatus(shana, event):
	if not event.group(0).startswith("."): return
	shana.send("module.bot.store", "SET DEFAULT", {'name': "module.store.last", 'value': 0})
	shana.send("module.bot.store", "SET DEFAULT", {'name': "module.store.rank", 'value': 0})
	shana.send("module.bot.store", "SET DEFAULT", {'name': "module.store.said", 'value': ''})
	shana.send("module.bot.store", "SET DEFAULT", {'name': "module.store.cooldown", 'value': 0})
	
	for i in range(4):
		l = shana.recv(subject=["VARIABLE",])
		if l.body['name'] == "module.store.last": last = l.body['value']
		elif l.body['name'] == "module.store.rank": rank = l.body['value']
		elif l.body['name'] == "module.store.said": said = l.body['value']
		elif l.body['name'] == "module.store.cooldown": cooldown = l.body['value']
	
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
	'4ONE WORD: FORCED INDICATION OF TOLD THREAD OVER']
	not_told = ['.iosysfagstatus', '.udongefagstatus', '.elifagstatus', '.eyeohsysfagstatus', '.iodongfagstatus']
	if event.group(0).strip() in not_told:
		if status == 5:
			shana.msg(event.sender, "PENDING...")
			time.sleep(5)
			shana.msg(event.sender, "3NOT TOLD")
		else:
			shana.say('NOT TOLD')
	else:
		if time.time() - last < 30 and event.group(0).strip() == said and cooldown < time.time():
			shana.say(ut_told[rank])
			shana.send("module.bot.store", "STORE", {'name': "module.store.last", 'value': time.time()})
			shana.send("module.bot.store", "STORE", {'name': "module.store.rank", 'value': rank+1})
			if rank+1 == len(ut_told):
				shana.send("module.bot.store", "STORE", {'name': "module.store.cooldown", 'value': time.time()+240})
				shana.send("module.bot.store", "STORE", {'name': "module.store.rank", 'value': 0})
			return
		elif not cooldown < time.time():
			shana.say("Told-o-meter cooling down")
			return
		else:
			shana.send("module.bot.store", "STORE", {'name': "module.store.last", 'value': time.time()})
			shana.send("module.bot.store", "STORE", {'name': "module.store.rank", 'value': 0})
			shana.send("module.bot.store", "STORE", {'name': "module.store.said", 'value': event.group(0).strip()})
		
		if status == 5:
			shana.msg(event.sender, "PENDING...")
			time.sleep(5)
			shana.msg(event.sender, "4TOLD")
		elif status == 6 and event.group(0) == '.macfagstatus':
			shana.msg(event.sender, "PENDING...")
			time.sleep(5)
			shana.msg(event.sender, "SIGNAL LOST")
		else:
			shana.say('4TOLD')

macfagstatus.name = 'macfagstatus'
macfagstatus.commands = ['\S*fagstatus']
