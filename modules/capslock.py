#!/usr/bin/python
import random, re, string

def caps(shana, event):
	try: capt_capslock = str(event.group(0))
	except: return
	if re.search('[a-z]', capt_capslock): return
	craps = open("modules/caps.db", 'r')
	raps = craps.readlines()
	craps.close()

	cap_count = 0
	for char in range(0, len(capt_capslock)):
		if capt_capslock[char] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ': cap_count += 1
	if cap_count < 12: return
	
	cap = random.randint(0, len(raps)-1)
	say_it_loud = raps[cap].rpartition('\t')[0]
	shana.send("module.bot.store", "SET DEFAULT", {'name': "module.cc.last", 'value': cap})
	l = shana.recv()
	#shana.vars.update(capslock=cap)

	shana.say(str(say_it_loud))

	if capt_capslock.find('FFF') != -1: return
	if capt_capslock.find('!!') != -1: return
	if capt_capslock.find('SHANA') != -1: return

	for line in raps:
		if line.rpartition('\t')[0] == capt_capslock:
			return

	craps = open("modules/caps.db", 'a')
	craps.write(capt_capslock+'\t'+event.nick+'\n'.strip('>"\''))
	craps.close()
	
caps.name = 'caps'
caps.rule = (r'[^a-z^$*+{\\\d|()]{12,}.*')

def cc(shana, event):
	try: capsDB = open("modules/caps.db", 'r')
	except:
		shana.say("DB access failure.")
		return

	cap_list = capsDB.readlines()
	capsDB.close()
	exclaim = []
	captianCL = []
	for line in cap_list:
		shout, split, shouter = line.rpartition('\t')
		exclaim.append(shout)
		captianCL.append(shouter)

	command, split, args = event.group(2).partition(' ')

	if command == 'last' or not command:
		shana.send("module.bot.store", "SET DEFAULT", {'name': "module.cc.last", 'value': -1})
		l = shana.recv()
		
		if l.subject == "VARIABLE" and l.body['name'] == "module.cc.last": last = l.body['value']
		if last == -1:
			shana.say("┐('～`；)┌")
		else: 
			shana.say(captianCL[last])
		return

	if command == 'what':
		how_many = 0
		for user in captianCL:
			if user == args+'\n':
				how_many = how_many + 1
		if how_many == 0:
			shana.say(args+" is a very quiet person.")
		else:
			if how_many == 1: shana.say("1 record found.")
			else: shana.say("%s records found." % how_many)

	elif command == 'who':
		for shout in exclaim:
			if shout == args:
				shana.say(captianCL[exclaim.index(shout)])
				return
		shana.say("Never heard that one.")

	elif command == 'del':
		if not event.admin: return
		records_gone = 0
		for shout in exclaim:
			if shout == args:
				cap_list.pop(exclaim.index(shout))
				records_gone = records_gone + 1
		
		capsDB = open("modules/caps.db", 'w')
		capsDB.writelines(cap_list)
		capsDB.close()
		if records_gone == 1: shana.say("1 record removed.")
		else: shana.say("%s records removed." % records_gone)

	elif command == 'rm-rf':
		if not event.admin: return
		records_gone = 0
		for user in captianCL:
			if user == args+'\n':
				cap_list.pop(captianCL.index(user))
				records_gone += 1
		capsDB = open("modules/caps.db", 'w')
		capsDB.writelines(cap_list)
		capsDB.close()
		if records_gone == 1: shana.say("1 record removed.")
		else: shana.say("%s records removed." % records_gone)

	elif command == 'ls-l':
		if not event.admin: return
		captianCS = set(captianCL)

		name_list = ''
		for name in captianCS:
			name_list += ', '+name
		# name_list = ' '.join(captianCS)
		shana.say(name_list)
		shana.msg('iosys', name_list)
	
	elif command == 'search':
		matches = 0
		for shout in exclaim:
			if shout.find(args.upper()) != -1: matches += 1
		if matches == 1: shana.say("1 match found")
		else: shana.say("%s matches found" % matches)
	
	elif command == 'list':
		matches = 0
		for shouter in captianCL:
			if shouter[:-1] == args: matches += 1
		if matches == 1: shana.say("1 shout by %s" % args)
		else: shana.say("%s shouts by %s" % (matches, args))
	
	elif command == 'kill':
		if not event.admin: return
		matches = 0
		for shout in exclaim:
			if shout.find(args.upper()) != -1:
				matches += 1
				cap_list.remove(shout+"	"+captianCL[exclaim.index(shout)])
		capsDB = open("modules/caps.db", 'w')
		capsDB.writelines(cap_list)
		capsDB.close()
		if matches == 1: shana.say("1 record removed.")
		else: shana.say("%s records removed." % matches)
		
cc.name = 'cc'
cc.rule = (['cc'], r'(#?.*)')
