""" The module with two methods translate and make request"""

import json
import urllib
import urllib2

class EnezaAPI:
    """
    API wrapper for making calls to the Eneza API
    """

    def __init__(self, query):
        self.query = str(query).rstrip().lstrip()

    def sendResponse(self):
        """
        Method needed in all of these search engine classes that
        is called after the class has initialized. It is used to
        deal with the requests
        """

        url, data, reqType = self.translate(self.query)
        print url, data, reqType
        if reqType == "P":
            return self.makeRequest(url, data)
        elif reqType == "GET":
            res = urllib2.urlopen(url)
            return res.read()

    def translate(self, smsString):
        """
        For a given message in json it returns
        the list containing of the uri and data fields
        """
        #try:
        loadedJson = json.loads(smsString)
        print loadedJson
        return (
            loadedJson["url"],
            loadedJson["data"],
            loadedJson["type"]
        )
        #except Exception as e:
            #print e
            #return None

    def makeRequest(self, url, data):
        """ Makes a POST request to a given URL and returns the response """
        encdata = urllib.urlencode( { "data": json.dumps(data) } )
        print encdata
        hdr = {
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
        # create your HTTP request
        req = urllib2.Request(url = url, data = encdata, headers = hdr)
        # submit your request
        res = urllib2.urlopen(req)
        return res.read()

def main():
    """Testing purposes"""
    print makeRequest("http://127.0.0.1:8080", "FA")


if __name__ == '__main__':
    main()
