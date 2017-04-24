"""
Umbrella Investigate API
Author: Abhijith R, Renjana Pillai
Date  Apr 3, 2017
Latest_domains endpoint shows whether the IP address entered as input has any known malicious domains associated with it

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
    print "Please enter an IP address\nUsage: latestDomains.py <Domain Name> (Eg: file.py 0.0.0.0)"
    sys.exit(1)
# latest_domains

headers = {
  'Authorization': 'Bearer ' + token
}
request = Request('https://investigate.api.opendns.com/ips/'+domainName+'.json', headers=headers)
response_body = urlopen(request).read()
print "latest_domains: " + response_body
