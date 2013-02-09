#!/usr/bin/env python
import random
def f_pokeball(phenny, input): 
	q = input.group(2)
	q = q.upper()
	balls = ["POKe BALL", "GREAT BALL", "ULTRA BALL", "SAFARI BALL", "MASTER BALL"]
	res = ["Awww! It appeared to be caught!", q+" fled!", "Aww, darn! It missed!", "Shoot! It was so close too!", "All right! "+q+" was caught!"]
	ball = random.randint(1, 5)
	result = random.randint(1, 5)
	phenny.say("A wild "+q+" appeared!")
	phenny.say(input.nick.upper()+" used "+balls[ball-1]+"!")
	if ball == 5:
		phenny.say(res[4])
	else:
		phenny.say(res[result-1])

f_pokeball.name = 'pokeball'
f_pokeball.rule = (['pokeball'], r'([\S ]+)?')
f_pokeball.priority = 'low'