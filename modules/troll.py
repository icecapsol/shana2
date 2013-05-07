#!/usr/bin/python
import random

def troll(shana, event):
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
	shana.say(trolls[troll_rating])

troll.name = 'troll'
troll.commands = (['troll'])
troll.priority = 'low'