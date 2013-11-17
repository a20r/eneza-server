
import android

class SMSPoolMember:

    def __init__(self, query):
        self.droid = android.Android()
        self.query = str(query).lstrip().rstrip()

    def wifiConnected(self):
        none = "<unknown ssid>"
        return not self.droid.wifiGetConnectionInfo().result["ssid"] == none

    def dataConnected(self):
        return self.droid.getCellLocation().result["cid"] > -1

    def sendResponse(self):
        if self.query == "connection":
            return "pool:" + str(self.wifiConnected() or self.dataConnected())
        else:
            return "pool: None"
