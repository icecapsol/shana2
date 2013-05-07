#!/usr/bin/env python
"""
validate.py - Phenny Validation Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import web

def val(phenny, input): 
   """Check a webpage using the W3C Markup Validator."""
   uri = input.group(2)
   if not uri.startswith('http://'): 
      uri = 'http://' + uri

   path = '/check?uri=%s;output=xml' % web.urllib.parse.quote(uri)
   info = web.head('http://validator.w3.org' + path)

   result = uri + ' is '

   if isinstance(info, list): 
      return phenny.say('Got HTTP response %s' % info[1])

   if 'X-W3C-Validator-Status' in info.keys(): 
      result += str(info['X-W3C-Validator-Status'])
      if info['X-W3C-Validator-Status'] != 'Valid': 
         if 'X-W3C-Validator-Errors' in info.keys(): 
            n = int(info['X-W3C-Validator-Errors'].split(' ')[0])
            if n != 1: 
               result += ' (%s errors)' % n
            else: result += ' (%s error)' % n
   else: result += 'Unvalidatable: no X-W3C-Validator-Status'

   phenny.reply(result)
val.commands = ['val']
val.example = '.val http://www.w3.org/'