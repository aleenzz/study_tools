#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:404
#配上临时邮箱 http://24mail.chacuo.net/ 申请ssr

import time
import requests
import json

number = str(int(time.time()))+"404"
emails = raw_input("input_email:")
def register(emails):
	headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Origin': 'https://wikicc.in',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	}
	post_url = "https://wikicc.in/auth/send"
	post_emails = "email="+emails
	req_email =requests.post(post_url,data = post_emails,headers=headers)
	req_email_json = json.loads(req_email.text)
	print req_email_json["msg"]
	print "="*50
	email_verify = raw_input("input_email_verify:")
	register_url = "https://wikicc.in/auth/register"
	post_info = 'email={emails}&name={number}&passwd={number}&repasswd={number}&code=&emailcode={email_verify}'.format(emails=emails,number=number,email_verify=email_verify)
	req_register = requests.post(register_url,data=post_info,headers=headers)
	requests_text = req_register.text
	req_text_json = json.loads(requests_text)
	if ":1" in requests_text:
		print "Success!!!"
		print "="*50
		print "email:"+emails
		print "username:"+number
		print "password:"+number
	else:
		print req_text_json["msg"]


if __name__ == '__main__':
	register(emails)


