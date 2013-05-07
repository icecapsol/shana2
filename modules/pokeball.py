#!/usr/bin/env python
import random
def pokeball(shana, event): 
	q = event.group(2)
	q = q.upper()
	balls = ["POKe BALL", "GREAT BALL", "ULTRA BALL", "SAFARI BALL", "MASTER BALL"]
	res = ["Awww! It appeared to be caught!", q+" fled!", "Aww, darn! It missed!", "Shoot! It was so close too!", "All right! "+q+" was caught!"]
	ball = random.randint(1, 5)
	result = random.randint(1, 5)
	shana.say("A wild "+q+" appeared!")
	shana.say(event.nick.upper()+" used "+balls[ball-1]+"!")
	if ball == 5:
		shana.say(res[4])
	else:
		shana.say(res[result-1])

pokeball.name = 'pokeball'
pokeball.rule = (['pokeball'], r'([\S ]+)?')
pokeball.priority = 'low'