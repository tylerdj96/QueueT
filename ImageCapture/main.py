import time
import os.path
import qt_fs
from sys import exit
from pyautogui import locateOnScreen, ImageNotFoundException
from infi.systray import SysTrayIcon
from threading import Thread, Event

from constructSettingsUI import constructSettingsUI
from notify import notifyQueuePop

CURRENT_DIR = os.path.dirname(__file__)

scanning = False
stopEvent = Event()
currentlyScanning = Event()
daemon = None

def scanScreen(settings):
    try:
        print("...searching...")
        print(settings)
        queuePop = locateOnScreen(
            settings['screenshotPath'], 
            grayscale=False, 
            confidence=settings['confidence'])
        print(queuePop)
        if (queuePop != None): 
            qt_fs.writeLogToFileSystem("IMAGE FOUND!")
            phoneNumber = qt_fs.readPhoneNumberFromAddon()
            if (phoneNumber != None):
                notifyQueuePop(phoneNumber)
                time.sleep(60)
                qt_fs.writeLogToFileSystem('Sleeping for 60 seconds...')
    except ImageNotFoundException or OSError:
        print("Image not found...")

def scanScreenForQueuePop(settings):
    while not stopEvent.is_set():
        print("Beginning scan...")
        qt_fs.writeLogToFileSystem("Beginning scan...")
        scanScreen(settings)
        print(f"waiting for {settings['pollingInterval']} seconds...")
        qt_fs.writeLogToFileSystem(f"waiting for {settings['pollingInterval']} seconds...")
        time.sleep(settings['pollingInterval'])
        
def startNewBackgroundThread():
    global daemon
    settings = qt_fs.readSettingsFromFileSystem()
    daemon = Thread(target=scanScreenForQueuePop, args=(settings,), daemon=True, name='Background')
    stopEvent.clear()
    currentlyScanning.set()
    daemon.start()
    
def stopOldBackgroundThread():
    print(f"Stopping scan...")
    if (not stopEvent.is_set()):
        stopEvent.set()
    if (currentlyScanning.is_set()):
        currentlyScanning.clear()
    if (daemon is not None):
        daemon.join()

def start_SYSTRAY(_):
    if (currentlyScanning.is_set()): 
        qt_fs.writeLogToFileSystem("Scanning already in progress...")
    else:
        qt_fs.clearFileSystemLogs()
        startNewBackgroundThread()

def changeSettings_SYSTRAY(_):
    settings = qt_fs.readSettingsFromFileSystem()
    constructSettingsUI(
        settings['pollingInterval'],
        settings['confidence'],
        settings['screenshotPath'],
        settings['wowRootDir'],
        settings['accountName'],
    )
    stopOldBackgroundThread()
    startNewBackgroundThread()

    
def quit_SYSTRAY(_):
    qt_fs.writeLogToFileSystem("You killed me! >:(")
    stopOldBackgroundThread()
    exit("Error message")
    
hover_text = "QueueT"

menu_options = (('Start', None, start_SYSTRAY),
                ('Change Settings', None, changeSettings_SYSTRAY)
               )

sysTrayIcon = SysTrayIcon(os.path.join(CURRENT_DIR, "./images/logo/QueueT.ico"), hover_text, menu_options, on_quit=quit_SYSTRAY, default_menu_index=1)
sysTrayIcon.start()

# use me for help
#btn = ttk.Button(frm, ...)
# print(btn.configure().keys())
