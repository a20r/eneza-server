""" The module with two methods translate and make request"""

import json
import urllib
import urllib2

def translate(smsString):
    """
    For a given message in json it returns
    the list containing of the uri and data fields
    """
    try:
        loadedJson = json.loads(smsString)
        return (loadedJson["url"], loadedJson["data"])
    except:
        return None

def makeRequest(url, data):
    """ Makes a POST request to a given URL and returns the response """

    headers = {"Content-type": "text/html",
               "Accept": "text/plain"}

    encdata = urllib.urlencode( { "data": json.dumps(data) } )

    # create your HTTP request
    req = urllib2.Request(url = url, data = encdata, headers = headers)

    # submit your request
    res = urllib2.urlopen(req)

    return res.read()


def main():
    """Testing purposes"""
    print makeRequest("http://127.0.0.1:8080", "FA")


if __name__ == '__main__':
    main()
