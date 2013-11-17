
import android
import server
import smsreader as reader
import time
import threading

class NumberInfo:
    def __init__(self, connected, freq):
        self.connected = connected
        self.freq = freq

class SMSMaster(reader.SMSReader):

    def __init__(self):
        super(SMSMaster, self).__init__()
        self.numberDict = {
            "+447564213928" : NumberInfo(True, 0)
        }
        self.checkConnectionStr = "pool: connection"

    def broadcastCheck(self):
        while True:
            for number in self.numberDict:
                self.droid.smsSend(number, self.checkConnectionStr)
                time.sleep(60 * 10)

    def funcSendMessage(self, smsString):
        connectedNumbers = filter(
            lambda key: self.numberDict[key].connected == True,
            self.numberDict.keys()
        )

        numberToSend = reduce(
            lambda numP, numN:
                numP if (
                    self.numberDict[numP].freq <
                    self.numberDict[numN].freq
                ) else numN,
            connectedNumbers
        )

        self.numberDict[numberToSend].freq += 1
        def retFunc():
            self.droid.smsSend(numberToSend, smsString)

        return retFunc

    def start(self):
        threading.Thread(
            target = self.broadcastConnection
        ).start()

        while True:
            if self.droid.smsGetMessageCount(True).result > 0:
                messageDict = self.readMessages()
                for numberStr in messageDict:
                    if messageDict[numberStr].split(":")[0] == "pool":
                        connBool = bool(
                            str(
                                messageDict[numberStr].split(":")[1]
                            ).lstrip().rstrip()
                        )

                        messageDict[numberStr].connection = connBool
                        continue

                    threading.Thread(
                        target = self.funcSendMessage(
                            messageDict[numberStr]
                        )
                    ).start()

if __name__ == "__main__":
    master = SMSMaster()
    master.start()


