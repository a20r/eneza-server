import urllib,json,re

#global variables
DEBUG = False
URL = "http://www.google.com/dictionary/json?callback=json&sl=en&tl=en&"

def reRemoveHex(string):
	"function to remove all hex code from a string"

	#remove hex codes and string between hex codes
	pattern = r"\\x..([^\\]{1,3})\\x.."
	string = re.sub(pattern,"",string)

	#remove remaining hex codes
	pattern = r"\\x.."
	string = re.sub(pattern,"",string)

	return string


class Google():

	def __init__(self,searchQuery):

		self.searchQuery = searchQuery
		self.url = None
		self.conent = None
		self.definitions = None

		self.setURL()
		self.setContent()
		self.setDefinitions()
		self.sendResponse()

	def setURL(self):
		"method to set the url for request"

		searchQuery = self.searchQuery

		#define the get parameters for the query
		query = urllib.urlencode({"q":searchQuery})
		url = URL+query

		if DEBUG:
			print(url)

		self.url = url

	def setContent(self):
		"method to set the content of the class"

		url = self.url

		#open the given url
		openURL = urllib.urlopen(url)
		#read the contents
		htmlString = openURL.read()
		#remove all hex caracter codes
		defineString = reRemoveHex(htmlString)

		#remove all characters outside parenthesese in preperation for json
		firstIndex = defineString.find("{")
		lastIndex = defineString.rfind("}")+1
		jsonString = defineString[firstIndex:lastIndex]

		#return json object from string
		content = json.loads(jsonString)

		if DEBUG:
			print content

		self.content = content

	def setDefinitions(self):
		"method to set the responce to send"

		content = self.content

		def getEntries(content):
			"returns the entry assoicated with the definition object"

			if ("primaries" in content.keys()):
				for item in content["primaries"]:
					for key,value in item.items():
						if key == "entries":
							return value

		def getAllMeaningTerms(entries):
			"returns all meaning terms from the entries"

			if not entries:
				return None

			for entry in entries:
				for key,value in entry.items():
					if key == "type":
						if value == "meaning":
							if ("terms" in entry.keys()):
								return entry["terms"]

		def getAllDefinitions(terms):
			"returns all definitions from the terms"

			#if not terms return None
			if not terms:
				return None

			return [term["text"] for term in terms if ((term["type"] == "text") and ("text" in term.keys()))]

		#run the functions to get definitions
		entries = getEntries(content)
		terms = getAllMeaningTerms(entries)
		definitions = getAllDefinitions(terms)

		if DEBUG:
			print entries
			print terms
			print definitions

		self.definitions = definitions


	def sendResponse(self,maxCharacters=160):
		"method to send the response with limited characters"

		searchQuery = self.searchQuery
		definitions = self.definitions
		response = ""

		# if definitions is None state ne definitions
		if (not definitions):
			definitions = ["No definition could be found"]

		#for each definition in set
		characterCount = 0
		for definition in definitions:
			#check there are enough characters reamining
			if (characterCount < maxCharacters):
				#prefix the search query to definition and postfix newline
				response += searchQuery+": "+definition+"\n"

			characterCount == len(response)

		#if the overall string is too long shorten
		toBeContinued = "..."
		if len(response) > maxCharacters:
			response = response[:maxCharacters-len(toBeContinued)]+toBeContinued

		if DEBUG == True:
			print response

		print response


if (__name__ == "__main__"):
	Google("drum and bass")
	Google("house")
	Google("love")
	Google("not in define")