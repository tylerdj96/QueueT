from requests import post
from json import dumps
from qt_fs import writeLogToFileSystem

API_URL = 'https://queuet.azurewebsites.net/QueuePop'

def notifyQueuePop(phoneNumber):
    todo = {"phoneNumber": phoneNumber}
    headers =  {"Content-Type":"application/json"}
    response = post(API_URL, data=dumps(todo), headers=headers)
    logMessage = f"SUCCESS: Sent text to {phoneNumber}"
    if response.status_code != 204:
        logMessage = f"ERROR when sending text: HTTP Status Code {response.status_code}"
    writeLogToFileSystem(logMessage)

    