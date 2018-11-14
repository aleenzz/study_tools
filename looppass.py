#!/usr/bin/env python
#-*- coding:utf-8 -*-

import difflib


info = {'name':'ma/laoshi',
		'abname':'mls', 
		'DateOfBirth':'19920222', 
		'Birthday':'0824', 
		'ID':'6130299910822191', 
		'phoneNumber':'16683666822',
		'girlname':'xiao/xiaofei',
		'girlabname':'xxf',
		'QQ':'550165942',
		'email':'',

}

definfo =[]

password = []

weakpassF = ['Qq','qq','QQ','yy','Yy','YY','a','ad','A','ab','woaini','QWE','z','zz','Aa','aa','AA','WOAINI','www','']

weakpassE = ['!@#','$%^','ABC','..','.','asdf','qwe','111','777','666','888','999','123','.mm','www','']

lovepass = ['520','ai','1314','5201314','love','Love','']

def getkey():
	for key,value in info.items():
		if len(value) != 0:
			definfo.append(key)
	return definfo
def loopweakFE(infos,number):
	if number =='1':
		for k in weakpassF:
			for j in weakpassE:
				password.append(k+info[infos].replace('/','')+j)
	elif number =='2':
		for k in weakpassF:
			password.append(k+info[infos].replace('/',''))
	elif number =='3':
		for j in weakpassE:
			password.append(info[infos].replace('/','')+j)


def loopweakidpass(infos):
	for k in weakpassF:
		for j in weakpassE:
			password.append(k+info[infos][-6:]+j)
	password.append(info['abname'][-6:]+info[infos][-6:])

def loopnamepass(passdict,infos):
	if type(passdict) == list:
		for i in passdict:
			password.append(i+info[infos].split('/')[1:][0])
			password.append(i+info[infos].split('/')[0:][0])
			password.append(i+info[infos].replace('/',''))
			password.append(i+info[infos].replace('/','')+info['Birthday'])
	else:
		for i in infos:
			password.append(info[passdict].split('/')[1:][0]+i)
			password.append(info[passdict].split('/')[0:][0]+i)
			password.append(info[passdict].replace('/','')+i)

def birthpass(passdict,infos):
	if type(passdict) == list:
		for i in passdict:
			password.append(i+info[infos])
			password.append(i+info[infos]+info['name'].split('/')[1:][0])
			password.append(i+info[infos]+info['name'].split('/')[-1:][0])
			password.append(i+info[infos]+info['abname'])
			password.append(i+info[infos])
	else:
		for i in infos:
			password.append(info[passdict]+i)
			password.append(info[passdict]+info['name'].split('/')[1:][0]+i)

def girlpass():
	for i in lovepass:
		password.append(info['name'].split('/')[-1:][0]+i+info['girlname'].split('/')[-1:][0])
		password.append(info['abname']+i+info['girlabname'])


def biupass():
	key_info = getkey()
	if 'name' in key_info:
		loopnamepass(weakpassF,'name')
		loopnamepass('name',weakpassE)
		loopweakFE('name','1')

	if 'abname' in key_info:
		loopweakFE('abname','1')

	if 'DateOfBirth' in key_info:
		birthpass(weakpassF,'DateOfBirth')
		birthpass('DateOfBirth',weakpassE)
		loopweakFE('DateOfBirth','1')

	if 'ID' in key_info:
		loopweakidpass('ID')

	if 'phoneNumber' in key_info:
		loopweakFE('phoneNumber','1')
		loopweakFE('phoneNumber','2')
		loopweakFE('phoneNumber','3')

	if 'girlname' and 'girlabname' in key_info:
		girlpass()

	if 'QQ' in key_info:
		loopweakFE('QQ','1')
		loopweakFE('QQ','2')
		loopweakFE('QQ','3')

	if 'email' in key_info:
		loopweakFE('email','1')
		loopweakFE('email','2')
		loopweakFE('email','3')




if __name__ == '__main__':
	biupass()
	with open("pass.txt","w") as f:
		for i in password:
			f.write(i+"\n")
