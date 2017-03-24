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
  print "ERROR: environment variable \'INVESTIGATE_TOKEN\' not set. Invoke script with \'INVESTIGATE_TOKEN=%YourToken% python scripts.py\'"
  sys.exit(1)

#Reading and validating commnad line argument
try:
    domainName=sys.argv[1]
except IndexError:
    print "Please enter a domain name\nUsage: domainSecurityInfo.py <Domain Name> (Eg: file.py example.com.com)"
    sys.exit(1)


# domains/categorization
headers = {
  'Authorization': 'Bearer ' + token
}

#Security Information For A Domain
request = Request('https://investigate.api.umbrella.com/security/name/'+domainName+'.json', headers=headers)

response_body = urlopen(request).read()
print response_body


