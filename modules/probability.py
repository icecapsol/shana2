import random, re

def rps(shana, event):
	if not event.group(2):
		return
	throws = {'r': 'rock', 'rock': 'rock', 'p': 'paper', 'paper': 'paper', 's': 'scissors', 'scissors': 'scissors'}
	values = {1: 'rock', 2: 'paper', 3: 'scissors'}
	results = {'rock': {'rock': 'tie', 'paper': 'lose', 'scissors': 'win'},
		   'paper': {'rock': 'win', 'paper': 'tie', 'scissors': 'lose'},
		   'scissors': {'rock': 'lose', 'paper': 'win', 'scissors': 'tie'}}

	throw = event.group(2).split(' ')[0].lower()
	if throw in throws.keys():
		counter = random.randint(1, 3)
		shana.say('You throw %s, I throw %s. You %s!' % (throws[throw], values[counter], results[throws[throw]][values[counter]]))
	
rps.commands = ['rps', 'janken', 'roshambo']

def flip(shana, event):
	if not event.group(2):
		coins = 1
	elif event.group(2):
		flip_text = re.search('[0-9]+', event.group(2))
		if not flip_text: return
		coins = int(flip_text.group(0))
	else:
		return

	if coins == 0:
		shana.say("Wtf, man.")
		return
	elif coins > 10000:
		shana.say("50 god damn percent. What the hell did you expect?")
		return

	faces = {0: "heads", 1: "tails"}
	flips = []
	for c in range(coins):
		flips.append(random.randint(0, 1))
	if coins == 1:
		shana.say("Flip a coin: %s" % faces[flips[0]])
	elif coins < 20:
		shana.say("Flip %d coins: %s" % (coins, ', '.join([faces[f] for f in flips])))
	else:
		shana.say("Flip %d coins: %d heads, %d tails" % (coins, len([f for f in flips if f == 0]), len([f for f in flips if f == 1])))
flip.commands = ['flip']


def roll(shana, event):
	roll_text = re.search('([0-9]+)d([0-9]+)([-+][0-9]+)?', event.group(2))
	if not roll_text: return
	roll = list(roll_text.groups())
	
	dice = int(roll.pop(0))
	sides = int(roll.pop(0))

	if dice == 0:
		shana.say("0 dice? Here, have 0 dollars.")
	if sides < 4:
		shana.say("%d sided dice? What dimension do you live in?")
		return

	if roll[0]:
		modifier = int(roll.pop(0))
	else:
		modifier = 0
	
	outcome = []
	for d in range(dice):
		outcome.append(random.randint(1, sides))
	subtotal = sum(outcome)
	total = subtotal + modifier
	
	if dice == 1:
		shana.say("Roll %s: %d %s" %
			(event.group(2).strip(), subtotal, {True: '', False: '-> %d' % total}[subtotal == total]) )
	else:
		shana.say("Roll %s: [%s] = %d %s" %
			(event.group(2).strip(), ' ,'.join(map(str, outcome)), subtotal, {True: '', False: '-> %d' % total}[subtotal == total]) )
roll.name = 'roll'
roll.commands = ['roll']
