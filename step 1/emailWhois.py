#!/usr/bin/env python
import readSettings
from urllib2 import Request, urlopen
import os, sys
import json


#Fetch API token from setting.txt
def getToken():
	appSettings = readSettings.loadSettings("../../settings.txt")

	firstSetting = appSettings[0].rstrip()
	return firstSetting
token=getToken()

#Validate token
if not token:
  print "Token not set"
  sys.exit(1)

#Reading and validating commnad line argument
try:
    email=sys.argv[1]
except IndexError:
    print "Please enter a email address\nUsage: emailWhois.py <emailID> (Eg: file.py test@example.com)"
    sys.exit(1)

# domains/categorization

headers = {
  'Authorization': 'Bearer ' + token
}
#This API method returns the WHOIS information for the specified email address
request = Request('https://investigate.api.umbrella.com/whois/emails/'+email, headers=headers)

response_body = urlopen(request).read()
print response_body