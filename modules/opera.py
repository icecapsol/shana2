#!/usr/bin/env python

def f_opera(phenny, input): 
	phenny.say("http://www.opera.com/")

f_opera.name = 'opera'
f_opera.commands = (['opera'])
f_opera.priority = 'low'

def f_gentoo(phenny, input): 
	phenny.say("http://wiki.archlinux.org/index.php/Arch_Compared_to_Other_Distributions#Gentoo_Linux")

f_gentoo.name = 'gentoo'
f_gentoo.commands = (['gentoo'])
f_gentoo.priority = 'low'