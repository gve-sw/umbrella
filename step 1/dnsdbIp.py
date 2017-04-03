#!/usr/bin/env python
import readSettings
from urllib2 import Request, urlopen
import os, sys
import json
import pprint

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
    domainName=sys.argv[1]
except IndexError:
    print "Please enter a domain name\nUsage: domainSecurityInfo.py <Domain Name> (Eg: file.py example.com.com)"
    sys.exit(1)
# dnsdb/ip

headers = {
  'Authorization': 'Bearer ' + token
}
request = Request('https://investigate.api.opendns.com/dnsdb/ip/a/'+domainName+'.json', headers=headers)
response_body = urlopen(request).read()
print "dnsdb/ip: " + response_body
