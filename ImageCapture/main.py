import pyautogui
import time
import sys
sys.path.insert(0, 'ImageCapture/modules')
from constructSettingsUI import constructSettingsUI

def readFromFileSystem():
    with open('data.txt', 'r') as f:
        data = f.read()

def scanScreen():
    try:
        queuePop = pyautogui.locateOnScreen(
            'ImageCapture/assets/okayPopTest.png', grayscale=False, confidence=0.9)
        print(queuePop)
        # pyautogui.screenshot('ImageCapture/assets/my_screenshot.png')
    except pyautogui.ImageNotFoundException:
        print("Image not found...")

def main():
    constructSettingsUI()
    while True:
        print("Beginning scan...")
        scanScreen()
        print("waiting for 1 seconds...")
        time.sleep(1)
    
main()


# use me for help
#btn = ttk.Button(frm, ...)
# print(btn.configure().keys())
