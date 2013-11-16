import urllib

#global variables
DEBUG = True
APIKEY = "QH2XXJ-4UJJJ3E489"

class WolframAlpha():
	""" class to deal with returning and sorting data from wolfram alpha """

	def __init__(self,query):

		self.query = query
		self.url = None
		self.responce = None

	def getURL(self):
		"get the url of the wolfram alpha query"

		query = self.query
		url = "http://api.wolframalpha.com/v2/query?input={}&appid={}".format(query,APIKEY)

		if DEBUG:
			print url

		self.url = url

	def setResponce(self):
		"method to set the wolfram alpha responce to a class variable"

		url = self.url

		if url:
			openURL = urllib.urlopen(self.url)
		else:
			raise ValueError("url is not defined")

		responce = openURL.read()

		if DEBUG:
			print responce


if __name__ == "__main__":
	wolframAlpha = WolframAlpha("test")
	wolframAlpha.getURL()
	wolframAlpha.setResponce()