import urllib,json

url = "http://www.google.com/dictionary/json?callback=a&sl=en&tl=en&q=armchair"
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

