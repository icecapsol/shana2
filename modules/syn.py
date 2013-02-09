#!/usr/bin/env python
import time

def f_syn(phenny, input):
	phenny.say("SMACK")

f_syn.rule = r'SYN'
f_syn.priority = 'low'