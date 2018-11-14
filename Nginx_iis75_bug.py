import requests
import re

headers ={
	'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
def getrobots(url):
	requrlrobots = requests.get(url+"/robots.txt"+"/1.php",headers=headers)
	requrlrobots1 = requests.get(url+"/robots.txt"+"%00.php",headers=headers)
	if requrlrobots.status_code == 200  or requrlrobots1.status_code !=400:
		if requrlrobots.headers["Content-Type"] == 'text/html' or requrlrobots1.headers["Content-Type"] == 'text/html':
			if "User-agent" in requrlrobots.content or "Disallow:" in requrlrobots1.content:
				print "test robots have bug "
			else:
				print "robots no bug and 404 is Unusual"
	else:
		print "no robots",requrlrobots.status_code,requrlrobots1.status_code
		getcss(url)

def getcss(url):
	requrl = requests.get(url,headers=headers)
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
					if ";}" in bugurl.content:
						print "test css have bug"
						break
					else:
						print "css no bug and 404 is Unusual"
			else:
				print "no bug",bugurl.status_code,bugurl1.status_code
				break

	else:
		print "dont re[css]"
if __name__ == '__main__':
	getrobots("https://www.xd0.com/")



