#!/usr/bin/env python
# coding=utf-8

"""
calc.py - Phenny Calculator Module modified a tiny bit to work with shana2
Copyright 2014, icecapsol@gmail.com

Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import web

r_result = re.compile(r'(?i)<A NAME=results>(.*?)</A>')
r_tag = re.compile(r'<\S+.*?>')

subs = [
   (' in ', ' -> '),
   (' over ', ' / '),
   (u'£', 'GBP '),
   (u'€', 'EUR '),
   ('\$', 'USD '),
   (r'\bKB\b', 'kilobytes'),
   (r'\bMB\b', 'megabytes'),
   (r'\bGB\b', 'kilobytes'),
   ('kbps', '(kilobits / second)'),
   ('mbps', '(megabits / second)')
]

def calc(phenny, input):
   """Use the Frink online calculator."""
   q = input.group(2)
   if not q:
      return phenny.say('0?')

   query = q[:]
   for a, b in subs:
      query = re.sub(a, b, query)
   query = query.rstrip(' \t')

   precision = 5
   if query[-3:] in ('GBP', 'USD', 'EUR', 'NOK'):
      precision = 2
   query = web.urllib.parse.quote(query)

   uri = 'http://futureboy.us/fsp/frink.fsp?fromVal='
   bytes = web.get(uri + query).decode('utf-8')
   m = r_result.search(bytes)
   if m:
      result = m.group(1)
      result = r_tag.sub('', result) # strip span.warning tags
      result = result.replace('&gt;', '>')
      result = result.replace('(undefined symbol)', '(?) ')

      if '.' in result:
         try: result = str(round(float(result), precision))
         except ValueError: pass

      if not result.strip():
         result = '?'
      elif ' in ' in q:
         result += ' ' + q.split(' in ', 1)[1]

      phenny.say(q + ' = ' + result[:350])
   else: phenny.reply("Sorry, can't calculate that.")
calc.name = "calc"
calc.commands = ['calc']
calc.example = '.calc 5 + 3'

def py(phenny, input):
   query = input.group(2).encode('utf-8')
   uri = 'http://tumbolia.appspot.com/py/'
   answer = web.get(uri + web.urllib.parse.quote(query))
   if answer:
      phenny.say(answer)
   else: phenny.reply('Sorry, no result.')
py.name = "py"
py.commands = ['py']

def wa(phenny, input):
   if not input.group(2):
      return phenny.reply("No search term.")
   query = input.group(2).encode('utf-8')
   uri = 'http://tumbolia.appspot.com/wa/'
   answer = web.get(uri + web.urllib.parse.quote(query.replace('+', '%2B')))
   if answer:
      phenny.say(answer)
   else: phenny.reply('Sorry, no result.')
wa.name = "wa"
wa.commands = ['wa']