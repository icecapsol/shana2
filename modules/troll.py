#!/usr/bin/python
import random

def f_troll(phenny, input):
	troll_rating = random.randint(0, 9)
	trolls = ["\\[L........4H]",
	"[L\\.......4H]",
	"[L.\\......4H]",
	"[L..\\.....4H]",
	"[L...|....4H]",
	"[L....|...4H]",
	"[L...../..4H]",
	"[L....../.4H]",
	"[L......./4H]",
	"[L........4H]/  Would rage again"]
	phenny.say(trolls[troll_rating])

f_troll.name = 'troll'
f_troll.commands = (['troll'])
f_troll.priority = 'low'