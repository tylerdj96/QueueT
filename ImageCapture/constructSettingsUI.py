import os.path
import tkinter.filedialog as fileDialog
import tkinter as tk
from tkinter import Tk, ttk
from qt_fs import writeSettingsToFileSystem, writeLogToFileSystem
from PIL import ImageTk, Image

CURRENT_DIR = os.path.dirname(__file__)

def constructSettingsUI(
        pollingInterval,
        confidence,
        screenshotPath,
        wowRootDir,
        accountName
        ):
    global screenShotPreviewContainer
    root = tk.Tk()
    
    currentPollingInterval = tk.IntVar(value=pollingInterval)
    currentConfidence = tk.DoubleVar(value=confidence)
    currentScreenShotPath = tk.StringVar(value=screenshotPath)
    screenshotPreview = ImageTk.PhotoImage(Image.open(currentScreenShotPath.get()))

    def selectAddonsFolder():
        addonsDirectory = fileDialog.askdirectory(mustexist=True)
        print(addonsDirectory)

    def selectScreenShot():
        fileName = fileDialog.askopenfilename(title="Select a Screenshot")
        currentScreenShotPath.set(fileName)
        writeLogToFileSystem(f"Screen shot path changed to: {fileName}")
        print(fileName)

    def saveAndQuit():
        # write to filesystem
        writeSettingsToFileSystem(currentPollingInterval.get(),
                     currentConfidence.get(),
                     currentScreenShotPath.get(),
                     wowRootDir,
                     accountName)
        root.destroy()
        print("closing UI")

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

    tk.Label(optionsFrame, text="Screenshot:").grid(
        column=0, row=2)
    tk.Label(optionsFrame, textvariable=currentScreenShotPath).grid(column=1, row=2)
    tk.Button(optionsFrame, text="Upload Screenshot",
              command=selectScreenShot).grid(column=2, row=2)

    tk.Label(optionsFrame, text="WoW Root Dir:").grid(column=0, row=3)
    tk.Label(optionsFrame, text=wowRootDir).grid(column=1, row=3)
    tk.Button(optionsFrame, text="Choose Path",
              command=selectAddonsFolder).grid(column=2, row=3)

    tk.Label(optionsFrame, text="Account Name:").grid(column=0, row=4)
    tk.Label(optionsFrame, text=accountName).grid(column=1, row=4)
    tk.Entry(optionsFrame).grid(column=2, row=4)
    
    screenShotPreviewContainer = tk.Label(optionsFrame, image=screenshotPreview).grid(column=1, row=5)
    
    tk.Button(quitAndSaveFrame, text="Save and Close",
              command=saveAndQuit).grid(column=0, row=1)
    
    root.iconbitmap(os.path.join(CURRENT_DIR, "./images/logo/QueueT.ico"))
    root.mainloop()
