#import requests
from urllib2 import Request, urlopen
import os, sys
import json

class Wrapper(object) :
    """
    This class is used to interact with the AMP API
    """
    def __init__(self, token, domainName):
        self.token = token
        self.domainName = domainName
    
    def getHeader(self):
        headers = {
          'Authorization': 'Bearer ' + self.token
        }
        return headers

    def getDomainCategorization(self):
        """
        Retrieves domain categories
        """
        headers=self.getHeader()
        request = Request('https://investigate.api.opendns.com/domains/categorization/'+self.domainName, headers=headers)

        response_body = urlopen(request).read()
        return response_body

    def getDomainScore(self):
        """
        Retrieves domain score
        """
        headers=self.getHeader()
        request = Request('https://investigate.api.opendns.com/domains/score/'+self.domainName, headers=headers)

        response_body = urlopen(request).read()
        return response_body

    def getDomainSecInfo(self):
        """
        Retrieves domain score
        """
        headers=self.getHeader()
        request = Request('https://investigate.api.umbrella.com/security/name/'+self.domainName, headers=headers)

        response_body = urlopen(request).read()
        return response_body

    def getDomainLabels(self):
        """
        Retrieves domain score
        """
        headers=self.getHeader()
        request = Request('https://investigate.api.opendns.com/domains/categorization/'+self.domainName+'?showLabels', headers=headers)

        response_body = urlopen(request).read()
        return response_body

    def getLatestTags(self):
        """
        Retrieves domain score
        """
        headers=self.getHeader()
        request = Request('https://investigate.api.opendns.com/domains/'+self.domainName+'/latest_tags', headers=headers)

        response_body = urlopen(request).read()
        return response_body

    def getLinksName(self):
        """
        Retrieves domain score
        """
        headers=self.getHeader()
        request = Request('https://investigate.api.opendns.com/links/name/'+self.domainName+'.json', headers=headers)

        response_body = urlopen(request).read()
        return response_body

    def getRecommendations(self):
        """
        Retrieves domain score
        """
        headers=self.getHeader()
        request = Request('https://investigate.api.opendns.com/recommendations/name/'+self.domainName+'.json', headers=headers)

        response_body = urlopen(request).read()
        return response_body

    def getSecurityName(self):
        """
        Retrieves domain score
        """
        headers=self.getHeader()
        request = Request('https://investigate.api.opendns.com/security/name/'+self.domainName+'.json', headers=headers)

        response_body = urlopen(request).read()
        return response_body

    def getDNSByName(self):
        """
        Retrieves domain score
        """
        headers=self.getHeader()
        request = Request('https://investigate.api.opendns.com/dnsdb/name/a/'+self.domainName+'.json', headers=headers)

        response_body = urlopen(request).read()
        return response_body