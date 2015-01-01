#!/usr/bin/python
import urllib.request
from urllib.request import urlopen
import re, time, datetime, subprocess
from bs4 import BeautifulSoup as BS

def http(shana, event):
	def identify(format, chunk):
		pid = subprocess.Popen(['identify', '-format', '"%s"' % format, '-'], executable='identify', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		out, err = pid.communicate(chunk)
		return out.decode('utf-8').replace('"', '')
	def bytes_to_better_bytes(b):
		levels = ['B', 'KB', 'MB', 'GB']
		for l in levels:
			if b < 1024:
				return "%.1f %s" % (b, l)
			b = b / 1024.0
		return "%.1f GB" % b
				
	if event.bytes.startswith(".un404"):
		shana.log("Ignoring un404 command", 7)
		return
	if not event.sender.startswith("#") and not event.admin:
		shana.log("Ignoring link sent in pm", 7)
		return
	
	# get the file we should be appending to
	today = datetime.date.today()
	uri_filename = 'modules/URIs %d-%02d.txt' % (today.year, today.month)
	if not os.path.exists(uri_filename):
		uri_file = open(uri_filename, 'w')
	else:
		uri_file = open(uri_filename, 'r')
	uri_count = len(uri_file.readlines())
	uri_file.close()
	
	def new_uri(args):
		uri_file = open(uri_filename, 'a')
		uri_file.write('%s\t%s\t%s\t%s\n' % (str(uri_count+1), str(int(time.time())), event.nick, '\t'.join(args).replace('\n', '')))
		uri_file.close()

	def fourchan(url):
		if url.find("/b/") != -1:
			shana.write(['KICK', event.sender+' '+event.nick], 'Rule #1, faggot')
			return
		if url.find("/mlp/") != -1:
			shana.say("ponies :/")
			return
		if url.find("boards") != -1:
			page_url = urlopen(url)
			soup = BS(page_url.read(32768))
			title = soup.find("title").get_text().strip()
			try: topic = soup.find(class_="subject").span["title"].strip()
			except: topic = ""
			
			if topic:
				shana.say("[URI %s] 034chan %s | %s" % (uri_count+1, title, topic))
				new_uri([url, "034chan %s | %s\n"  % (title, topic)])
			else:
				shana.say("[URI %s] 034chan %s" % (uri_count+1, title))
				new_uri([url, "034chan %s\n"  % title])
	def fourchan_images(url):
		if url.find("/b/") != -1:
			shana.write(['KICK', event.sender+' '+event.nick], 'Rule #1, faggot')
			return
		if url.find("/mlp/") != -1:
			shana.say("ponies :/")
			return
		if url.rsplit(".", 1)[1].lower() in ['jpg', 'jpeg', 'png', 'gif', 'tif', 'tiff']:
			image_url = urlopen(url)
			image_info = image_url.info()
			image_size = int(image_info["Content-Length"])
			image = image_url.read(32768)
			try: w, h, t = identify("%w %h %m", image).strip().split()
			except Exception as e:
				shana.say("Yep, that's a link")
				shana.log("Exception parsing image: %s" % e, 4)
				return
			
			shana.say("[URI %s] 034chan: %sx%s %s %s" % (uri_count+1, w, h, bytes_to_better_bytes(image_size), t))
			new_uri([url, "034chan %sx%s %s %s\n" % (w, h, bytes_to_better_bytes(image_size), t)])
		if url.rsplit(".", 1)[1].lower() == "webm":
			image_url = urlopen(url)
			image_info = image_url.info()
			image_size = int(image_info["Content-Length"])
			
			shana.say("[URI %s] 034chan: %s WebM" % (uri_count+1, bytes_to_better_bytes(image_size)))
			new_uri([url, "034chan %s WebM\n" % bytes_to_better_bytes(image_size)])

	def newegg(url):
		page_url = urlopen(url)
		soup = BS(page_url)
		if url.find('www.newegg.com/Product'):
			import json
			tag = re.search('/?Item=([A-Z0-9]+)', url)
			price = "$"+json.loads(urlopen("http://content.newegg.com/LandingPage/ItemInfo4ProductDetail.aspx?v2=2012&Item="+tag.group(1)).readlines()[2].decode('utf-8').replace("var rawItemInfo=", '')[:-3])['finalPrice']
		else:
			price = "$"+soup.find(id="singleFinalPrice").get("content")
		title = soup.find("title").get_text()

		shana.say("[URI %s] 3Title: %s %s" % (uri_count+1, title, price))
		new_uri([url, "3Title: %s %s\n" % (title, price)])
	
	def flickr(url):
		picid = url.partition("_")[0].rpartition("/")[2]
		page_url = urlopen("http://flickr.com/photo.gne?id=%s" % picid)
		new_url = page_url.geturl()[:-1]
		page_url.close()
		
		shana.say("[URI %s] 4Flickr: %s's photostream" % (uri_count+1, new_url.rpartition("/")[0].rpartition("/")[2]))
		new_uri([url, "[URI %s] Flickr: %s's photostream" % (uri_count+1, new_url.rpartition("/")[0].rpartition("/")[2])])
		
	def youtube(url):
		if url.find("v=") != -1: page_url = urlopen("http://gdata.youtube.com/feeds/api/videos/"+url.partition("v=")[2].partition("&")[0])
		elif url.find("/v/") != -1: page_url = urlopen("http://gdata.youtube.com/feeds/api/videos/"+url.partition("/v/")[2].partition("&")[0])
		elif url.find("/user/") != -1:
			shana.say("[URI %s] 1,0You0,4tube %s's Channel" % (uri_count+1, url.partition("/user/")[2]))
			new_uri([url, "1,0You0,4tube %s's Channel\n" % url.partition("/user/")[2]])
			return
		else:
			page_url = urlopen(url)
			soup = BS(page_url.read(8196))
			title = soup.find("title").get_text().strip()
			shana.say("[URI %s] 1,0You0,4tube %s" % (uri_count+1, title))
			new_uri([url, "1,0You0,4tube %s\n" % title])
			return

		
		soup = BS(page_url.read())
		title = soup.find("title").get_text().strip()
		views = soup.find("yt:statistics")['viewcount']
		length = int(soup.find("yt:duration")['seconds'])
		seconds = length % 60
		minutes = (length -seconds) / 60
		
		try: rates = int(soup.find("gd:rating")['numraters'])
		except:
			rates = 0
			thumbs_up = 0
		else:
			thumbs_up = int( ((float(soup.find("gd:rating")['average']) - 1.0) / 4.0) * rates )
		
		shana.say("[URI %s] 1,0You0,4tube %s [%d:%02d] - %s views %d 3☺ %d 4☹" % (uri_count+1, title, minutes, seconds, views, thumbs_up, rates - thumbs_up))
		new_uri([url, "1,0You0,4tube %s [%d:%02d]\n" % (title, minutes, seconds)])

	def omploader(url):
		ompid = url.rsplit('/', 1)[1][1:]
		ompinfo_page = urlopen('http://ompldr.org/i%s' % ompid).read().decode("utf-8")
		stuff = ompinfo_page.split('<div class="content">\n', 2)[1].split('\n')
		info = {'name': stuff[2].partition('</a>')[0].rpartition('>')[2],
		'size': stuff[3].rpartition('</div>')[0].rpartition('>')[2],
		'hits': stuff[4].rpartition('</div>')[0].rpartition('>')[2],
		'uploaded': stuff[5].rpartition('</div>')[0].rpartition('>')[2],
		'type': stuff[6].rpartition('</div>')[0].rpartition('>')[2]}
		
		shana.say("[URI %s] 3Ompldr: %s [%s] - %s hits" % (uri_count+1, info['name'], info['size'], info['hits']))
		new_uri([url, "3Ompldr: %s [%s] - %s hits" % (info['name'], info['size'], info['hits'])])

	def gelbooru(url):
		if hasattr(re.search('jpg|png|gif|swf', url), "group"): return
		gelpage = urlopen(url)
		try:
			soup = BS(gelpage)
		except:
			return
		authors = [a.find_all("a")[1].get_text() for a in soup.find_all("li", "tag-type-artist")]
		author_pl = "s" if len(authors) > 1 else ""
		origins = [o.find_all("a")[1].get_text() for o in soup.find_all("li", "tag-type-copyright")]
		origin_pl = "s" if len(origins) > 1 else ""
		chars = [c.find_all("a")[1].get_text() for c in soup.find_all("li", "tag-type-character")]
		char_pl = "s" if len(chars) > 1 else ""
		if soup.find("li", text=re.compile("Rating")).get_text() == "Rating: Safe": warn = ""
		else: warn = "[NSFW]"
		
		title = "%s Author%s: %s Origin%s: %s Character%s: %s" % (warn, author_pl, ', '.join(authors), origin_pl, ', '.join(origins), char_pl, ', '.join(chars))

		shana.say("[URI %s] 3Gelbooru: %s" % (uri_count+1, title))
		new_uri([url, "3Title: %s\n" % title])
		return
	
	def danbooru(url):
		if hasattr(re.search('jpg|png|gif|swf', url), "group"): return
		danpage = urlopen(url)
		soup = BS(danpage)
		
		authors = [a.find_all("a")[1].get_text() for a in soup.find_all("li", "tag-type-artist")]
		author_pl = "s" if len(authors) > 1 else ""
		origins = [o.find_all("a")[1].get_text() for o in soup.find_all("li", "tag-type-copyright")]
		origin_pl = "s" if len(origins) > 1 else ""
		chars = [c.find_all("a")[1].get_text() for c in soup.find_all("li", "tag-type-character")]
		char_pl = "s" if len(chars) > 1 else ""
		if soup.find("li", text=re.compile("Rating")).get_text() == "Rating: Safe": warn = ""
		else: warn = "[NSFW]"
		
		title = "%s Author%s: %s Origin%s: %s Character%s: %s" % (warn, author_pl, ', '.join(authors), origin_pl, ', '.join(origins), char_pl, ', '.join(chars))

		shana.say("[URI %s] 3Danbooru: %s" % (uri_count+1, title))
		new_uri([url, "3Title: %s\n" % title])
		return

	def tor(url):
		# do not log these links
		torpage = urllib.request.build_opener(urllib.request.ProxyHandler({"http": "localhost:8118", "https": "localhost:8118"})).open(url)
		soup = BS(torpage)
		
		try: title = soup.find("title").get_text().strip()
		except: return
		
		if not title: title = "Untitled"
		
		shana.say("[URI NULL] 3Tor: %s" % (title))
		return

	def therest(url):
		page_url = urlopen(urllib.request.Request(url, headers={'User-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0"}))
		try: title = BS(page_url.read(8196)).find("title").get_text().strip()
		except: return
		#page = page_url.read(4096)
		if not title: return

		shana.say("[URI %s] 3Title: %s" % (uri_count+1, title))
		new_uri([url, "3Title: %s\n" % title])
		return

		
	modulelist = [('4chan.org', fourchan), ('4cdn.org', fourchan_images), ('newegg.c', newegg), ('.youtube.com', youtube), ('.static.flickr.com', flickr),
	 ('ompldr.org', omploader), ('omploader.org', omploader), ('gelbooru.com', gelbooru), ('danbooru.donmai.us', danbooru),
	 (".onion.to", tor), (".onion", tor)]
	caught = 0
	for catch in event.searches:
		for module in modulelist:
			if catch.find(module[0]) != -1: 
				try: 
					module[1](catch)
				except urllib.error.HTTPError as e:
					shana.say('HTTP Error %d' % e.code)
				except Exception as e:
					shana.log("Exception retrieving link: %s" % e, 2)
				caught = 1
				uri_count += 1
				break
		if caught == 0:
			try: 
				therest(catch)
			except urllib.error.HTTPError as e:
				shana.say('HTTP Error %d' % e.code)
			except Exception as e:
				shana.log("Exception retrieving link: %s" % e, 2)
			uri_count += 1
		caught = 0

http.name = 'http'
http.rule = (r'http[s]?:\/\/\S+')