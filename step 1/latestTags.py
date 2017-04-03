#!/usr/bin/env python
import readSettings
from urllib2 import Request, urlopen
import os, sys
import json
<<<<<<< Updated upstream

=======
<<<<<<< HEAD
import pprint
=======

>>>>>>> origin/master
>>>>>>> Stashed changes

#Fetch API token from setting.txt
def getToken():
	appSettings = readSettings.loadSettings("../../settings.txt")
	firstSetting = appSettings[0].rstrip()
	return firstSetting
<<<<<<< Updated upstream

=======
<<<<<<< HEAD
	
=======

>>>>>>> origin/master
>>>>>>> Stashed changes
token=getToken()

#Validate token
if not token:
  print "Token not set"
  sys.exit(1)

#Reading and validating commnad line argument
try:
    domainName=sys.argv[1]
except IndexError:
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
    print "Please enter a domain name\nUsage: domainSecurityInfo.py <Domain Name> (Eg: file.py example.com.com)"
sys.exit(1)
=======
>>>>>>> Stashed changes
    print "Please enter a domain name\nUsage: latestTags.py <Domain Name> (Eg: file.py example.com)"
    sys.exit(1)


# latest_tags
<<<<<<< Updated upstream
=======
>>>>>>> origin/master
>>>>>>> Stashed changes

headers = {
  'Authorization': 'Bearer ' + token
}
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
request = Request("https://investigate.api.opendns.com/domains/"+domainName+"/latest_tags", headers=headers)
response_body = urlopen(request).read()
print 
=======
>>>>>>> Stashed changes
request = Request('https://investigate.api.opendns.com/domains/'+domainName+'/latest_tags', headers=headers)

response_body = urlopen(request).read()
print "latest_tags: " + response_body



<<<<<<< Updated upstream
=======
>>>>>>> origin/master
>>>>>>> Stashed changes
