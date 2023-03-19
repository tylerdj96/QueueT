import os.path
import tkinter.filedialog as fileDialog
import tkinter as tk
from tkinter import Tk, ttk

CURRENT_DIR = os.path.dirname(__file__)

def constructSettingsUI(
        pollingInterval,
        confidence,
        screenshotPath,
        wowRootDir,
        accountName,
        saveSettings):
    root = tk.Tk()
    
    currentPollingInterval = tk.IntVar(value=pollingInterval)
    currentConfidence = tk.DoubleVar(value=confidence)

    def selectAddonsFolder():
        addonsDirectory = fileDialog.askdirectory(mustexist=True)
        print(addonsDirectory)

    def selectScreenShot():
        fileName = fileDialog.askopenfilename()
        print(fileName)

    def saveAndQuit():
        # write to filesystem
        saveSettings(currentPollingInterval.get(),
                     currentConfidence.get(),
                     screenshotPath,
                     wowRootDir,
                     accountName)
        root.destroy()
        print("save and quit")

    frame = ttk.Frame(root, padding=20)
    frame.grid()

    optionsFrame = ttk.Frame(frame, padding=15)
    optionsFrame.grid()

    quitAndSaveFrame = ttk.Frame(frame, padding=15)
    quitAndSaveFrame.grid()

    tk.Label(optionsFrame, text="Polling Interval:").grid(column=0, row=0)
    # tk.Label(optionsFrame, text=pollingInterval).grid(column=1, row=0)
    tk.Entry(optionsFrame, textvariable=currentPollingInterval).grid(column=1, row=0)
    
    tk.Label(optionsFrame, text="Confidence:").grid(column=0, row=1)
    tk.Entry(optionsFrame, textvariable=currentConfidence).grid(column=1, row=1)

    tk.Label(optionsFrame, text="Queue Pop Visual Indicator:").grid(
        column=0, row=2)
    tk.Label(optionsFrame, text=screenshotPath).grid(column=1, row=2)
    tk.Button(optionsFrame, text="Upload Screenshot",
              command=selectScreenShot).grid(column=2, row=2)

    tk.Label(optionsFrame, text="WoW Root Dir:").grid(column=0, row=3)
    tk.Label(optionsFrame, text=wowRootDir).grid(column=1, row=3)
    tk.Button(optionsFrame, text="Choose Path",
              command=selectAddonsFolder).grid(column=2, row=3)

    tk.Label(optionsFrame, text="Account Name:").grid(column=0, row=4)
    tk.Label(optionsFrame, text=accountName).grid(column=1, row=4)
    tk.Entry(optionsFrame).grid(column=2, row=4)

    tk.Button(quitAndSaveFrame, text="Save & Quit",
              command=saveAndQuit).grid(column=0, row=1)
    
    root.iconbitmap(os.path.join(CURRENT_DIR, "../images/logo/QueueT.ico"))
    root.mainloop()
