import os.path
from json import load, dump, JSONDecodeError

ROOT_DIR = 'D:\World of Warcraft'
WTF_DIR = '_retail_\WTF'
ACCOUNT_DIR = 'Account'
ACCOUNT_NAME = 'TEXMAX456'
SAVED_VARIABLES_DIR = 'SavedVariables'
ADDON_FILENAME = 'QueueT.lua'
JSON_FILENAME = 'QueueT.json'
LOG_FILENAME = 'QueueT_Log.txt'

FULLPATH = os.path.join(ROOT_DIR, WTF_DIR, ACCOUNT_DIR,
                        ACCOUNT_NAME, SAVED_VARIABLES_DIR)
ADDON_FULLPATH = os.path.join(FULLPATH, ADDON_FILENAME)
JSON_FULLPATH = os.path.join(FULLPATH, JSON_FILENAME)
LOG_FULLPATH = os.path.join(FULLPATH, LOG_FILENAME)

POLLING_INTERVAL = 5
CONFIDENCE = 0.8
SCREENSHOT_PATH = 'D:\Fun\QueueT\ImageCapture\images\okayPopTest.png'
WOW_ROOT_DIR = 'D:\World of Warcraft'

print(FULLPATH)

def readSettingsFromFileSystem():
    defaults = {
        "pollingInterval": POLLING_INTERVAL,
        "confidence": CONFIDENCE,
        "screenshotPath": SCREENSHOT_PATH,
        "wowRootDir": WOW_ROOT_DIR,
        "accountName": ACCOUNT_NAME
    }
    try:
        jsonFile = open(JSON_FULLPATH)
        data = load(jsonFile)
        jsonFile.close()
        settings = {
            "pollingInterval": data['pollingInterval'],
            "confidence": data['confidence'],
            "screenshotPath": data['screenshotPath'],
            "wowRootDir": data['wowRootDir'],
            "accountName": data['accountName']
        }
        return settings
    except OSError or JSONDecodeError:
        print("Could not read/open file. Creating with defaults")
        newJsonFile = open(JSON_FULLPATH, 'w')
        dump(defaults, newJsonFile)
        newJsonFile.close()
        settings = defaults
        return settings
    
def readPhoneNumberFromAddon():
    try:
        addonFile = open(ADDON_FULLPATH)
        data = addonFile.read()
        splitData = data.split()
        phoneNumber = splitData[2]
        addonFile.close()
        return phoneNumber
    except OSError:
        print("Could not read/open file")
        return None

# this is called after init so we know ADDON.json exists
def writeSettingsToFileSystem(
    pollingInterval,
    confidence,
    screenshotPath,
    wowRootDir,
    accountName):
    newSettings = {
        "pollingInterval": pollingInterval,
        "confidence": confidence,
        "screenshotPath": screenshotPath,
        "wowRootDir": wowRootDir,
        "accountName": accountName
    }
    newJsonFile = open(JSON_FULLPATH, 'w')
    dump(newSettings, newJsonFile)
    newJsonFile.close()
    return newSettings


def clearFileSystemLogs():
    logFile = open(LOG_FULLPATH, 'w')
    logFile.close()
    
def writeLogToFileSystem(logEntry):
    with open(LOG_FULLPATH, 'a') as logFile:
     logFile.write(logEntry)
     logFile.write('\n')