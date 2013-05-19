#!/usr/bin/env python

def ctcp(shana, event):
	responses = dict([s.split(" ", 1) for s in open("modules/ctcp.txt", 'r').readlines()
				if not s.startswith('#') and len(s.strip()) > 0])

	query = event.group(0)[1:-1].upper()
	if query in responses.keys(): shana.write(['NOTICE', event.nick], "%s" % (responses[query]))
	elif query == "VERSION": shana.write(['NOTICE', event.nick], "%s" % shana.conf['version'])
	elif query == "SOURCE": shana.write(['NOTICE', event.nick], "https://github.com/icecapsol/shana2.git")

ctcp.name = 'ctcp'
ctcp.rule = r'(^.+)'