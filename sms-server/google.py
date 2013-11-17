import urllib,json

#global variables
DEBUG = True
URL = "http://www.google.com/dictionary/json?callback=json&sl=en&tl=en&"

class Google():

	def __init__(self,searchQuery):

		self.searchQuery = searchQuery

		self.setURL()
		self.setContent()
		self.setResponse()

	def setURL(self):
		"method to set the url for request"

		searchQuery = self.searchQuery

		query = urllib.urlencode({"q":searchQuery})
		url = URL+query

		if DEBUG:
			print(url)

		self.url = url

	def setContent(self):
		"method to set the content of the class"

		url = self.url

		openURL = urllib.urlopen(url)
		defineString = openURL.read()

		#remove all characters outside parenthesese
		firstIndex = defineString.find("{")
		lastIndex = defineString.rfind("}")+1
		jsonString = defineString[firstIndex:lastIndex]

		#escape all backslashes
		jsonString = jsonString.replace("\\","\\\\")

		#return json object from string
		content = json.loads(jsonString)

		if DEBUG:
			print content

		self.content = content

	def setResponse(self):
		"method to set the responce to send"

		content = self.content

		response = None

		for i in range(10):
			try:
				response = content["primaries"][0]["entries"][i]["terms"][0]["text"]
			except:
				pass
			i+=1

		if DEBUG:
			print response

		self.response = response


if __name__ == "__main__":
	#Google("drum and bass")
	Google("house")