"""
Umbrella Investigate API
Author: Abhijith R, Renjana Pillai
Date  Apr 3, 2017
Returns a list of co-occurences for the specified domain

"""

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
    print "Please enter a domain name\nUsage: recommendationsName.py <Domain Name> (Eg: file.py example.com)"
    sys.exit(1)
# recommendations/name

headers = {
  'Authorization': 'Bearer ' + token
}
request = Request('https://investigate.api.opendns.com/recommendations/name/'+domainName+'.json', headers=headers)
response_body = urlopen(request).read()
print "recommendations/name: " + response_body
