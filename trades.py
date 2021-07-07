#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, errno
from lbcapi import api
from string import find,replace

hmac_key = ""
hmac_secret = ""

trade = sys.argv[1]
print("Connecting to localbitcoins api...")
conn = api.hmac(hmac_key, hmac_secret)
print("Done!")

if find(trade,'.txt') != -1:
	file = open (trade,'r')
	trades = [replace(t,'\n','') for t in file]
	file.close()
else:
	trades = [trade,]

for code in trades:
	print("Downloading "+code+"...")
	resp = conn.call('GET', '/api/contact_messages/'+code+'/').json()

	try:
		os.mkdir(str(code))
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

	os.chdir("./"+str(code))

	try:
		os.mkdir("attachment")
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

	f = open ('messages.txt','w')

	for i in resp["data"]["message_list"]:
		if i['msg']:
			f.write( i["sender"]["username"].encode('utf-8')+": \n"+i["msg"].encode('utf-8')+"\n"+i["created_at"].encode('utf-8')+"\n\n")
		else:
			os.chdir("attachment")
			with open(i["attachment_name"].encode('utf-8'), 'wb') as handle:
				img = conn.call('GET', replace(i["attachment_url"].encode('utf-8'),"https://localbitcoins.com",""))
				for block in img.iter_content(1024):
					if not block:
						break
					handle.write(block)
			os.chdir("./..")
			f.write( i["sender"]["username"].encode('utf-8')+": \n"+i["attachment_name"].encode('utf-8')+"\n"+i["attachment_url"].encode('utf-8')+"\n"+i["created_at"].encode('utf-8')+"\n\n")

	f.close()
	os.chdir("./..")
	print("Done!")