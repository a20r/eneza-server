
import android

class SMSReader(object):

    def __init__(self):
        self.droid = android.Android()

    def readMessages(self):
        """
        Returns a dictionary of phone numbers to messages. Parses the new
        messages on the phone
        """
        # gets the message return objects
        msgObjs = self.droid.smsGetMessages(True).result

        # marks the messages as read
        ids = map(lambda msgDict: msgDict["_id"], msgObjs)
        self.droid.smsMarkMessageRead(ids, True)

        return dict(
            (mObj["address"], mObj["body"]) for mObj in msgObjs
        )
