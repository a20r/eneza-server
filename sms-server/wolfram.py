import urllib
import xml.etree.cElementTree as xmlElementTree

#global variables
DEBUG = False
APIKEY = "QH2XXJ-4UJJJ3E489"

class WolframAlpha():
	""" class to deal with returning and sorting data from wolfram alpha """

	def __init__(self,searchQuery):

		self.searchQuery = searchQuery
		self.url = None
		self.elementTree = None
		self.dictionaryResponce = None

		self.getURL()
		self.setContent()
		self.setResponce()
		self.sendResponce()

	def getURL(self):
		"get the url of the wolfram alpha query"

		searchQuery = self.searchQuery
		#define GET parameters
		query = urllib.urlencode({"input":searchQuery,"appid":APIKEY})
		#construct url
		url = "http://api.wolframalpha.com/v2/query?{}".format(query)

		if DEBUG:
			print url

		self.url = url

	def setContent(self):
		"method to set the wolfram alpha element tree as a class variable"

		url = self.url

		if url:
			openURL = urllib.urlopen(self.url)
		else:
			raise ValueError("url is not defined")

		#read the xml content returned
		xmlContent = openURL.read()
		#set the element tree from the xml responce
		self.elementTree = xmlElementTree.fromstring(xmlContent)

	def getPodFromTitle(self,title):
		"method to return all pods with the given title"

		elementTree = self.elementTree

		if elementTree:
			#retrieve all elements from the element tree
			allPods = elementTree.getchildren()
		else:
			raise ValueError("elementTree is not defined")

		#for all pods check if pod name is result
		for pod in allPods:
			#look at the attribute of the xml element tag
			attributes = pod.attrib
			#if the title is an attribute of the xml tag
			if "title" in attributes.keys():
				#if the title is the required title return the pod
				if attributes["title"] == title:
					return pod

		return None

	def getPlaintextFromPod(self,pod):
		"method to return all the elements that are in plaintext"

		#get all subPods of given pod
		subPods = pod.getchildren()

		#for all subPods 
		for subPod in subPods:
			#find all plaintext tags
			plaintext = subPod.findall("plaintext")
			#return the first instance of plaintext
			return plaintext[0].text

	def getPlaintextFromTitle(self,title):
		"""method to return all the plaintext from a pod with the givent title

		if there are no pods with the given title return None
		"""
		#get the pod
		pod = self.getPodFromTitle(title)

		if DEBUG == True:
			print pod

		#if there is a pod with given title return the included plaintext
		if pod:
			return self.getPlaintextFromPod(pod)
		else:
			return None

	def setResponce(self):
		"method to set the full dictionary responce from the query"

		#define title of interest
		titleList = ["Input","Input interpretation","Basic information","Result","Alternate form"]
		dictionaryResponce = {}

		#for all titles populate the dictionar responce
		for title in titleList:
			dictionaryResponce[title] = self.getPlaintextFromTitle(title)

		if DEBUG == True:
			print dictionaryResponce

		self.dictionaryResponce=dictionaryResponce

	def sendResponce(self,maxCharacters=160):
		"method to send the responce of the query"

		dictionaryResponce = self.dictionaryResponce
		responce = ""

		#for all elements in the dictionary add to the responce string
		for key,value in dictionaryResponce.items():
			if value:
				responce += "{}: {} \n".format(key,value)

		#if the responce is longer than the max characters shorten
		if len(responce)>maxCharacters:
			toBeContinued = "...\n"
			responce = responce[:maxCharacters-len(toBeContinued)]+toBeContinued

		print responce

if __name__ == "__main__":
	WolframAlpha("capital of england")
	WolframAlpha("y=12x+23")
	WolframAlpha("shakespear")
	WolframAlpha("differentiate(y=3x+10)")