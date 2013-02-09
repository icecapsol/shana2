#!/usr/bin/env python
import re, crypt, sys, io

def f_trip(phenny, input):
    pw = input.group(2) \
        .replace('"', '&quot;')      \
        .replace("'", '')           \
        .replace('<', '&lt;')        \
        .replace('>', '&gt;')        \
        .replace(',', ',')    \
	   .encode('shift_jis', 'ignore')
    salt = (pw + b'...')[1:3]
    salt = re.compile(b'[^\.-z]').sub(b'.', salt)
    salt = salt.translate(bytes.maketrans(b':;<=>?@[\\]^_`', b'ABCDEFGabcdef'))
    trip = crypt.crypt(pw.decode("utf-8"), salt.decode("utf-8"))[-10:]
    phenny.say("%s => %s" % (input.group(2), trip))

f_trip.name = 'trip'
f_trip.commands = ['trip']
f_trip.priority = 'low'