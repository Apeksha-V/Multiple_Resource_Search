import threading
import urllib
import urllib2
import json

from HTMLParser import HTMLParser
import twitter

from search.models import Result, Response


class CommunicationService:

    def __init__(self,config):
        self.googleUrl = 'https://www.googleapis.com/customsearch/v1?key=' + config.GOOGLE_API_KEY + '&cx=017576662512468239146:omuauf_lfve&q='
        self.duckUrl = 'https://api.duckduckgo.com/?format=json&q='
        self.twitterPath = 'f=tweets&q='
        self.twitterApi = twitter.Api(consumer_key=config.CONSUMER_KEY,
                          consumer_secret=config.CONSUMER_SECRET,
                          access_token_key=config.ACCESS_TOKEN,
                          access_token_secret=config.ACCESS_TOKEN_SECRET)
        self.timeout = config.HTTP_TIMEOUT

    def callApi(self,query,hostUrl):
        threads = []
        result = {}
        query = urllib.quote_plus(query)
        try:
            threads.append(threading.Thread(target=self.googleSearch, args=(query,result,hostUrl)))
            threads.append(threading.Thread(target=self.duckDuckGoSearch, args=(query,result,hostUrl)))
            threads.append(threading.Thread(target=self.twitterSearch, args=(query,result,hostUrl)))

            for t in threads:
                t.daemon = True  # set thread to daemon ('ok' won't be printed in this case)
                t.start()

            for t in threads:
                t.join(self.timeout)

            print result
            return Response(query,result)
        except:
            print("Error: unable to start thread")


    def googleSearch(self,query,result,hostUrl):
        result["google"] ={
            "error" : "operation_timeout"
        }
        try:
            response = urllib2.urlopen(self.googleUrl + query).read()
            data = json.loads(response)
            hits = data['items']
            text = hits[0]['snippet']
            result["google"] = Result(hostUrl,text)
            #print("google-->",text)
        except KeyError:
            result["google"] = {
                "error": "Empty search result"
            }
        except Exception, e:
            print "Failed Google data fetch: ", e
            result["google"] = {
                "error": "Oops! Something went wrong"
            }

    def duckDuckGoSearch(self,query,result,hostUrl):
        result["duckduckgo"] = {
            "error": "operation_timeout"
        }
        try:
            response = urllib2.urlopen(self.duckUrl + query).read()
            data = json.loads(response)
            hits = data['RelatedTopics']
            text = hits[0]['Text']
            result["duckduckgo"] = Result(hostUrl, text)
            #print ("duck-->"+text)
        except IndexError:
            result["google"] = {
                "error": "Empty search result"
            }
        except Exception, e:
            print "Failed DuckDuckGo data fetch: ", e
            result["duckduckgo"] = {
                "error": "Oops! Something went wrong"
            }

    def twitterSearch(self,query,result,hostUrl):

        result["twitter"] = {
            "error": "operation_timeout"
        }
        try:

            hits = self.twitterApi.GetSearch(raw_query=self.twitterPath + query)
            text = hits[0].text
            result["twitter"] = Result(hostUrl, text)
            #print("Twitter-->"+text)
        except IndexError:
            result["google"] = {
                "error": "Empty search result"
            }
        except Exception, e:
            print "Failed Twitter data fetch: ", e
            result["twitter"] = {
                "error": "Oops! Something went wrong"
            }