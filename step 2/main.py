import sys
import json
import readSettings
import six
from six import *
from umbrellaInvestigate import Wrapper

def main():
    """
    Main method for our initializing our Wrapper API and calling functions
    """

    """
    Retrieve API keys from settings.txt
    """
#Fetch API token from setting.txt
    def getToken():
        appSettings = readSettings.loadSettings("../../settings.txt")
        firstSetting = appSettings[0].rstrip()
        return firstSetting

    token=getToken()
    domainName = raw_input('Enter a Domain name: ')

    """
    Initialise Wrapper
    """
    investigateWrapper = Wrapper(token, domainName)

    getDomainCategorizationJson = investigateWrapper.getDomainCategorization();
    print "\n Domain Categorization\n"+getDomainCategorizationJson

    getDomainScoreJson = investigateWrapper.getDomainScore();
    print "\n Domain Score\n"+getDomainScoreJson

    getDomainSecInfoJson = investigateWrapper.getDomainSecInfo();
    print "\n Domain Securty Information\n"+getDomainSecInfoJson

    getDomainLabelsJson = investigateWrapper.getDomainLabels();
    print "\n Domain Labels \n"+getDomainLabelsJson

    getLatestTagsJson = investigateWrapper.getLatestTags();
    print "\n Domain Latest Tags \n"+str(getLatestTagsJson)

    getLinksNameJson = investigateWrapper.getLinksName();
    print "\n Domain Links Name \n"+str(getLinksNameJson)

    getRecommendationsJson = investigateWrapper.getRecommendations();
    print "\n Domain Recommendation \n"+str(getRecommendationsJson)

    getSecurityNameJson = investigateWrapper.getSecurityName();
    print "\n Domain Security Name \n"+str(getSecurityNameJson)

    getDNSByNameJson = investigateWrapper.getDNSByName();
    print "\n DNS by Name \n"+str(getDNSByNameJson)
    

if __name__ == '__main__':
    sys.exit(main())