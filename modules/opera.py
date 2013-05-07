#!/usr/bin/env python

def opera(shana, event): 
	shana.say("http://www.opera.com/")

opera.name = 'opera'
opera.commands = (['opera'])

def gentoo(shana, event): 
	shana.say("http://wiki.archlinux.org/index.php/Arch_Compared_to_Other_Distributions#Gentoo_Linux")

gentoo.name = 'gentoo'
gentoo.commands = (['gentoo'])