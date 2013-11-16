
import android
import threading

def makeRequest(url, postData):
    return "{'test': true}"

def translateToComponents(smsString):
    return "www.example.com", "{}"

class SMSServer:

    def __init__(self):
        self.droid = android.Android()

    def readMessages(self):

        # gets the message return objects
        msgObjs = self.droid.smsGetMessages(True).result

        # marks the messages as read
        ids = map(lambda msgDict: msgDict["_id"], msgObjs)
        self.droid.smsMarkMessageRead(ids, True)

        return dict(
            [
                (mObj["address"], mObj["body"]) for mObj in msgObjs
            ]
        )

    def parseAndMakeRequest(self, smsString):
        def retFunc():
            url, postData = translateToComponents(smsString)
            retJson = makeRequest(url, postData)
            self.droid.makeToast(retJson)
        return retFunc

    def start(self):
        while True:
            if self.droid.smsGetMessageCount(True).result > 0:
                messageDict = self.readMessages()
                for numberStr in messageDict:
                    threading.Thread(
                        target = self.parseAndMakeRequest(messageDict[numberStr])
                    ).start()


"""Hacky Test Functions"""

def test_messageReader():
    droid = android.Android()
    unreadOnly = True
    while True:
        if droid.smsGetMessageCount(unreadOnly).result > 0:
            msgObjs = droid.smsGetMessages(unreadOnly)
            ids = map(lambda msgDict: msgDict['_id'], msgObjs.result)
            droid.smsMarkMessageRead(ids, True)
            print msgObjs
            break

if __name__ == "__main__":
    #test_messageReader()
    sServer = SMSServer()
    sServer.start()

