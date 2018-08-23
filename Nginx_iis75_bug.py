import requests
import re

url = "http://www.sousou8.com/"
requrlrobots = requests.get(url+"/robots.txt"+"/1.php")
requrlrobots1 = requests.get(url+"/robots.txt"+"%00.php")
if requrlrobots.status_code == 200  or requrlrobots1.status_code !=400:
	if requrlrobots.headers["Content-Type"] == 'text/html' or requrlrobots1.headers["Content-Type"] == 'text/html':
		print "test robots have bug "
	else:
		print "no"
else:
	requrl = requests.get(url)
	text_url =requrl.text
	css_re = re.compile(r'type="text/css" href="(.*?).css')
	csss = css_re.findall(text_url)
	testurls = []
	if len(csss) != 0:
		for css in csss:
			if "http://" in css or "https://" not in css:
				testurls.append(url+css+".css")
			else:
				print "css in other web"
				break
		for testurl in testurls:
			bugurl = requests.get(testurl+"/1.php")
			bugurl1 = requests.get(testurl+"%00.php")
			if bugurl.status_code == 200 or bugurl1.status_code != 400:
				if bugurl.headers["Content-Type"] == 'text/html' or bugurl1.headers["Content-Type"] == 'text/html':
					print "test css have bug"
					break
	else:
		print "dont re[css]"







