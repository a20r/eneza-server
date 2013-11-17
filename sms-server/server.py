
import android
import threading
import google,wolfram, enezaapi as eneza
import os
import smsreader as reader
import poolmember

class SMSServer(reader.SMSReader):
    """
    SMS Server that receives formatted data and makes the corresponding
    HTTP requests.
    """

    def __init__(self):
        super(SMSServer, self).__init__()

        self.searchEngineDict = {
            "wolfram": wolfram.WolframAlpha,
            "define" : google.Google,
            "api": eneza.EnezaAPI,
            "pool": poolmember.SMSPoolMember
        }

    def parseMessage(self, smsString):
        """
        Parses message and uses the necessary engine

        SMS String formating:
            <Query Type>:<Query>
        """

        if not ":" in smsString:
            return None

        queryType = smsString.split(":")[0].lower()
        #phoneNumber = smsString.split(":")[1]
        query = smsString[smsString.index(':') + 1:].lstrip().rstrip()
        print "QUERY", query

        #try:
        queryResponse = self.searchEngineDict[queryType](
            query
        ).sendResponse()
        print "RESPONSE", queryResponse
        #except KeyError:
            #return None
        return queryResponse

    def parseAndMakeRequest(self, phoneNumber, smsString):
        """
        Used for thread creation. Returns a function that is set
        as the target in a thread
        """

        def retFunc():
            queryResponse = self.parseMessage(smsString)
            if queryResponse:
                self.droid.smsSend(phoneNumber, queryResponse)
        return retFunc

    def start(self):
        """
        Starts the main process
        """
        while True:
            if self.droid.smsGetMessageCount(True).result > 0:
                messageDict = self.readMessages()
                for numberStr in messageDict:
                    threading.Thread(
                        target = self.parseAndMakeRequest(
                            numberStr, messageDict[numberStr]
                        )
                    ).start()

if __name__ == "__main__":
    #test_messageReader()
    try:
        sServer = SMSServer()
        sServer.start()
        os.join()
    except Exception as e:
        print e
