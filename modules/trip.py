#!/usr/bin/env python
import re, crypt

def trip(shana, event):
    pw = event.group(2) \
        .replace('"', '&quot;')      \
        .replace("'", '')           \
        .replace('<', '&lt;')        \
        .replace('>', '&gt;')        \
        .replace(',', ',')    \
	   .encode('shift_jis', 'ignore')
    salt = (pw + b'...')[1:3]
    salt = re.compile(b'[^\.-z]').sub(b'.', salt)
    salt = salt.translate(bytes.maketrans(b':;<=>?@[\\]^_`', b'ABCDEFGabcdef'))
    trip = crypt.crypt(pw.decode("shift_jis"), salt.decode("shift_jis"))[-10:]
    shana.say("%s => %s" % (event.group(2), trip))

trip.name = 'trip'
trip.commands = ['trip']