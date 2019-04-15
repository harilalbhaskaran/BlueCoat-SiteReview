#!/usr/bin/env python
import json
import requests
import xml.etree.ElementTree as ET

f = open('site-list', 'r')
for line in f:
	sitedomain = line.strip()
	baseurl = "https://sitereview.bluecoat.com/resource/lookup"
	headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
	payload = {"url":sitedomain, "captcha":""}
	req = requests.post(baseurl,headers=headers,data=json.dumps(payload)) 
	req.content.decode("UTF-8")
	if req.status_code != 200:
	    print(sitedomain+"- HTTP {} returned".format(req.status_code))
	else:
	    root = ET.fromstring(req.content)
	    url = root.find('.//url').text
	    category = root.find('.//translatedCategories/en/name').text
	    if root.find('.//ratingDts').text == "OLDER":
	        date = ">"
	    else:
	        date = "<"
	    maxdate = root.find('.//ratingDtsCutoff').text
	    print("URL: {} | Last Time Rated/Reviewed: {} {} days ago | Category: {}".format(url,date,maxdate,category))
f.close()
