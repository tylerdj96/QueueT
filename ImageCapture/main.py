import pyautogui
import time
import sys
import os.path
import json
sys.path.insert(0, 'ImageCapture/modules')
from constructSettingsUI import constructSettingsUI

ROOT_DIR = 'D:\World of Warcraft'
WTF_DIR = '_retail_\WTF'
ACCOUNT_DIR = 'Account'
ACCOUNT_NAME = 'TEXMAX456'
SAVED_VARIABLES_DIR = 'SavedVariables'
ADDON_FILENAME = 'QueueT.lua'
JSON_FILENAME = 'QueueT.json'

FULLPATH = os.path.join(ROOT_DIR, WTF_DIR, ACCOUNT_DIR,
                        ACCOUNT_NAME, SAVED_VARIABLES_DIR)
ADDON_FULLPATH = os.path.join(FULLPATH, ADDON_FILENAME)
JSON_FULLPATH = os.path.join(FULLPATH, JSON_FILENAME)

POLLING_INTERVAL = 5
CONFIDENCE = 0.8
SCREENSHOT_PATH = 'D:\Fun\QueueT\ImageCapture\images\okayPopTest.png'
WOW_ROOT_DIR = 'D:\World of Warcraft'

print(FULLPATH)

settings = {}


def readFromFileSystem():
    global settings
    defaults = {
        "pollingInterval": POLLING_INTERVAL,
        "confidence": CONFIDENCE,
        "screenshotPath": SCREENSHOT_PATH,
        "wowRootDir": WOW_ROOT_DIR,
        "accountName": ACCOUNT_NAME
    }
    try:
        jsonFile = open(JSON_FULLPATH)
        data = json.load(jsonFile)
        settings = {
            "pollingInterval": data['pollingInterval'],
            "confidence": data['confidence'],
            "screenshotPath": data['screenshotPath'],
            "wowRootDir": data['wowRootDir'],
            "accountName": data['accountName']
        }
        jsonFile.close()
    except OSError or json.JSONDecodeError:
        print("Could not read/open file. Creating with defaults")
        newJsonFile = open(JSON_FULLPATH, 'w')
        json.dump(defaults, newJsonFile)
        settings = defaults
        newJsonFile.close()

# this is called after init so we know ADDON.json exists


def writeToFileSystem(
    pollingInterval,
    confidence,
    screenshotPath,
    wowRootDir,
    accountName):
    global settings
    newSettings = {
        "pollingInterval": pollingInterval,
        "confidence": confidence,
        "screenshotPath": screenshotPath,
        "wowRootDir": wowRootDir,
        "accountName": accountName
    }
    newJsonFile = open(JSON_FULLPATH, 'w')
    json.dump(newSettings, newJsonFile)
    settings = newSettings
    newJsonFile.close()


def scanScreen(settings):
    try:
        queuePop = pyautogui.locateOnScreen(
            settings['screenshotPath'], 
            grayscale=False, 
            confidence=settings['confidence'])
        print(queuePop)
        # pyautogui.screenshot('ImageCapture/assets/my_screenshot.png')
    except pyautogui.ImageNotFoundException:
        print("Image not found...")

def main():
    readFromFileSystem()
    print(settings)
    constructSettingsUI(
        settings['pollingInterval'],
        settings['confidence'],
        settings['screenshotPath'],
        settings['wowRootDir'],
        settings['accountName'],
        writeToFileSystem
    )
    while True:
        print("Beginning scan...")
        scanScreen()
        print(f"waiting for {settings['pollingInterval']} seconds...")
        time.sleep(settings['pollingInterval'])


main()


# use me for help
#btn = ttk.Button(frm, ...)
# print(btn.configure().keys())
