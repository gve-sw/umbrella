from itty import *
import urllib2,json,six,re,sys,time,ast,yaml
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
        -posting a message to the Spark room
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
            msg1 = "Hey there!!! My name is Laku\n I'm here to help you with the security related information of a domain!!!\n Enter a domain name to get started\nUsage: Laku /domainName"
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg1})
        elif '.com' in in_message or '.org' in in_message:
            global domName
            global investigateWrapper
            domName= in_message.split("/")
            investigateWrapper = Wrapper(token, domName[1])
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "What security information about "+domName[1]+" would you like to know?\nDomain Category\nDomain Score\n Security Information\nLabels\nDomain Tagging Date\nLinks\nRecommendations\nDNS resource record by Name"})
        elif 'category' in in_message or 'categories' in  in_message:
        #Get Domain Categories
            try:
                getDomainCategorizationJson = investigateWrapper.getDomainCategorization();
                # print(getDomainCategorizationJson)
                j= json.loads(getDomainCategorizationJson)
                catValue = ast.literal_eval(json.dumps(j))
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Domain Categorization\n"})
                for key,value in catValue.items():
                    secCat=value['security_categories']
                    conCat=value['content_categories']
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Security Categories: "+str(secCat)+"\nContent Category: "+str(conCat)})                        
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
                
        elif 'score' in in_message:
        #Get Domain Score
            try:
                getDomainScoreJson = investigateWrapper.getDomainScore();
                jscore= json.loads(getDomainScoreJson)
                scoreValue = ast.literal_eval(json.dumps(jscore))
                for key,value in scoreValue.items():
                    dom = key
                    domScore = value
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nName: "+str(dom)+"\nScore: "+str(domScore)})
            except:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"})
                print(sys.exc_info()[0])
        elif 'security' in in_message or 'security information' in in_message:
        #Get Domain Security Information
            try:
                getDomainSecInfoJson = investigateWrapper.getDomainSecInfo();
                secInfo = yaml.safe_load(getDomainSecInfoJson)
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDomain Security Info\n"})
                for key,value in secInfo.items():
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\n"+str(key)+" : "+str(value)})
            except Exception, e:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"+str(e)})
        elif 'label' in in_message or 'labels' in in_message:
        #Get Domain Label
            try:
                getDomainLabelsJson = investigateWrapper.getDomainLabels();
                jlabel= json.loads(getDomainLabelsJson)
                scoreValue = ast.literal_eval(json.dumps(jlabel))
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\nDomain Labels\n"})
                for key,value in scoreValue.items():
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Name: "+key})
                    for k,v in value.iteritems():
                        sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": " "+str(k)+": "+str(v)})
            except Exception, e:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Please enter a domain name\n"+str(e)})
        elif 'tags' in in_message or 'tag' in in_message:
        #Get Domain Tags
            try:
                getLatestTagsJson = investigateWrapper.getLatestTags();
                tagInfo = yaml.safe_load(getLatestTagsJson)
                print(tagInfo)
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Domain Tagged Date\n"})
                for k,v in tagInfo[0].items():
                    print(k,v)
                    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "\n"+str(k)+": "+str(v)})
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