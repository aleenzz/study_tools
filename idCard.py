# -*- coding: utf-8 -*- 
#根据阿里云市场的接口通过api返回身份证头像---仅供验证，切勿用于非法 
import base64
import os
import json
import urllib, urllib2, sys
import ssl

def getData():
	host = 'https://faceimg.market.alicloudapi.com'
	path = '/getCardFaceImg'
	method = 'POST'
	appcode = '148f17f8xxxxx9b6e24ae323ba998c'
	querys = ''
	bodys = {}
	url = host + path
	bodys['idCardNum'] = '''513xxxxxx'''
	bodys['realName'] = '''小白'''
	post_data = urllib.urlencode(bodys)
	request = urllib2.Request(url, post_data)
	request.add_header('Authorization', 'APPCODE ' + appcode)
	request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	response = urllib2.urlopen(request, context=ctx)
	content = response.read()
  	contentjson = json.loads(content)
  	return contentjson

def getimg(contentjson):
	conjosn =  contentjson["Code"]
	idCarimg = contentjson["Data"]
	print conjosn
	if (conjosn == 0):
		img = base64.b64decode(idCarimg)
		file=open('idCar.jpg','wb')
		file.write(img)
		file.close()
		print contentjson
	else:
		print contentjson
if __name__ == '__main__':
	getdata = getData()
	getimg(getdata)
