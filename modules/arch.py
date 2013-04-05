#!/usr/bin/python
from bs4 import BeautifulSoup as BS
import matplotlib.pyplot as plt
from urllib.request import urlopen

def arch(phenny, input): 
	args = input.group(2).split()
	package = args[0]
	repos = {'community': 'repo=Community&', 'community-testing': 'repo=Community-Testing&', 'core': 'repo=Core&', 'extra': 'repo=Extra&',
		    'multilib': 'repo=Multilib&', 'multilib-testing': 'repo=Multilib-Testing&', 'testing': 'repo=Testing&'}
	arches = {'any': 'arch=any&', 'i686': 'arch=i686&', 'x86_64': 'arch=x86_64&'}
	parch = ''
	prepo = ''
	for arg in args:
		if arg.lower() in arches.keys():
			parch = arches[arg]
		elif arg.lower() in repos.keys():
			prepo = repos[arg]
	
	url = "https://www.archlinux.org/packages/?sort=%s&arch=%s&q=%s&maintainer=&flagged=" % (prepo, parch, package)
	soup = BS(urlopen(url).read())
	
	try: results = int(soup.find_all('p')[1].get_text().split()[0])
	except:
		phenny.say("No packages found.")
		return
	plist = soup.find('tbody')
	
	psample = {}
	for pack in plist.find_all('tr'):
		if len(psample.keys()) > 5: break
		fields = pack.find_all('td')
		if fields[2].get_text() in psample.keys(): continue
		psample[fields[2].get_text()] = {'arch': fields[0].get_text(),
								   'repo': fields[1].get_text(),
								   'link': fields[2].find('a').get('href'),
								   'version': fields[3].get_text(),
								   'desc': fields[4].get_text(),
								   'date': fields[5].get_text()}
	
	if results == 1:
		p = list(psample.values())[0]
		phenny.say("%s %s - %s (%s) %s https://www.archlinux.org%s" % (list(psample.keys())[0], p['version'], p['desc'], p['date'], p['repo'].upper(), p['link']))
	else:
		phenny.say("%s (%d results)" % (', '.join(psample.keys()), results))
arch.commands = ['arch']

def aur(phenny, input): 
	package = input.group(2).split()[0]
	
	url = "https://aur.archlinux.org/packages/?O=0&K=%s" % package
	soup = BS(urlopen(url).read())
	
	try: results = int(soup.find_all('p')[1].get_text().split()[0])
	except:
		phenny.say("No packages found.")
		return
	plist = soup.find('tbody')
	
	psample = {}
	for pack in plist.find_all('tr'):
		if len(psample.keys()) > 5: break
		fields = pack.find_all('td')
		if fields[1].get_text() in psample.keys(): continue
		psample[fields[1].get_text()] = {'category': fields[0].get_text(),
								   'link': fields[1].find('a').get('href'),
								   'version': fields[2].get_text(),
								   'votes': fields[3].get_text(),
								   'desc': fields[4].get_text()}
	
	if results == 1:
		p = list(psample.values())[0]
		phenny.say("%s - %s (%s votes) %s https://aur.archlinux.org%s" % (list(psample.keys())[0], p['desc'], p['votes'], p['category'].upper(), p['link']))
	else:
		phenny.say("%s (%d results)" % (', '.join(psample.keys()), results))

aur.commands = ['aur']