from itty import *
import urllib2,json,six,re,sys,time,ast
from json2html import *
from six import *
sys.path.append('../step 2/')
import readSettings
import umbrellaInvestigate
from umbrellaInvestigate import Wrapper

#Fetching Umbrella Investigate API token
def getToken():
    appSettings = readSettings.loadSettings("../../settings.txt")
    firstSetting = appSettings[0].rstrip()
    return firstSetting

token=getToken()

#Fetching Bot token
def getBotToken():
    appSettings = readSettings.loadSettings("../../settings.txt")
    botToken = appSettings[1].rstrip()
    return botToken

def sendSparkGET(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents
    
def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents

@post('/')
def index(request):

    webhook = json.loads(request.body)
    print (webhook['data']['id'])
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)

    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')
        if 'hi'in in_message or "hello" in in_message:
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "markdown": "<h2>Umbrella Investigate</h2>"})
            msg1 = "Hi there! My name is <h4>Laku<h4>\n Please enter a domain name!!!"
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "markdown": msg1})
        elif '.com' in in_message:
            global domName
            global investigateWrapper
            domName= in_message.split("/")
            investigateWrapper = Wrapper(token, domName[1])
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "What security information about "+domName[1]+" would you like to know?\nDomain Category\nDomain Score\nSecurity Information\nLabels\nLatest Tags\nLinks\nRecommendations\nSecurity Name\nDNS resource record by Name"})
        elif 'category' in in_message or 'categories' in  in_message:
        #Get Domain Categories
            try:
                getDomainCategorizationJson = investigateWrapper.getDomainCategorization();
                # print(getDomainCategorizationJson)
                j= json.loads(getDomainCategorizationJson)
                catValue = ast.literal_eval(json.dumps(j))
                for key,value in catValue.items():
                    secCat=value['security_categories']
                    conCat=value['content_categories']
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Domain Categorization\n Security Categories: "+str(secCat)+"\nContent Category: "+str(conCat)})                        
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
                
        elif 'score' in in_message:
        #Get Domian Score
            try:
                getDomainScoreJson = investigateWrapper.getDomainScore();
                jscore= json.loads(getDomainScoreJson)
                scoreValue = ast.literal_eval(json.dumps(jscore))
                for key,value in scoreValue.items():
                    dom = key
                    domScore = value
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDomain Score\nName: "+str(dom)+"\nScore: "+str(domScore)})
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
                print(sys.exc_info()[0])
        elif 'securityinfo' in in_message:
        #Get Domain Security Information
            try:
                getDomainSecInfoJson = investigateWrapper.getDomainSecInfo();
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDomain Security Info\n"+getDomainSecInfoJson})
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
        elif 'label' in in_message or 'labels' in in_message:
        #Get Domain Lable
            try:
                getDomainLabelsJson = investigateWrapper.getDomainLabels();
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDomain Labels\n"+getDomainLabelsJson})
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
        elif 'tags' in in_message or 'tag' in in_message:
        #Get Domain Tags
            try:
                getLatestTagsJson = investigateWrapper.getLatestTags();
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDomain Latest Tags\n"+getLatestTagsJson})
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
        elif 'link' in in_message or 'links' in in_message:
        #Get Domain Links
            try:
                getLinksNameJson = investigateWrapper.getLinksName();
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDomain Links\n"+getLinksNameJson})
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
        elif 'recommendation' in in_message or 'recommendations' in in_message:
        #Get Recommendations    
            try:
                getRecommendationsJson = investigateWrapper.getRecommendations();
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDomain Recommendations\n"+getRecommendationsJson})
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
        elif 'securityname' in in_message:
        #Get Security Name
            try:
                getSecurityNameJson = investigateWrapper.getSecurityName();
                endSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDomain Security Name\n"+getSecurityNameJson})
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
        elif 'dns' in in_message or 'resource' in in_message:
        #Get DNS Resource Record by Name
            try:
                getDNSByNameJson = investigateWrapper.getDNSByName();
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDNS resource record by Name\n"+getDNSByNameJson})
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
    return "true"

####Spark Bot Information#####
bot_email = "laku@sparkbot.io"
bot_name = "Laku"
bearer = getBotToken()
run_itty(server='wsgiref', host='127.0.0.1', port=8000)