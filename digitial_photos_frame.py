# -*- coding: utf-8 -*-
from PIL import ImageTk, Image
from Tkinter import Tk, Label
import os
import time
import threading
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',)


PHOTOS_PATH = './photos'
INTERVAL = 10
IS_STOP = 0
DISPLAY_CONDITION = threading.Condition()
PLAY_OR_STOP_EVENT = threading.Event()
FILES = os.listdir(PHOTOS_PATH)
FILE_INDEX = -1
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0


def initPanel(tkRoot):
    logging.debug('Initializing panel...')
    tkRoot.attributes("-fullscreen", True)
    panel = Label(tkRoot, text="电子相框", bg="black", fg="red", font='size, 40')
    panel.pack(side="bottom", fill="both", expand="yes")
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = tkRoot.winfo_screenwidth()
    SCREEN_HEIGHT = tkRoot.winfo_screenheight()
    return panel


def getPhotoImageByName(fileName):
    image = Image.open(fileName)
    newSize = calculateImageSize(image)
    return getPhotoImage(image, newSize)


def calculateImageSize(image):
    imageWidth, imageHeight = image.size
    if imageWidth > SCREEN_WIDTH or imageHeight > SCREEN_HEIGHT:
        ratio = 0
        if imageWidth >= imageHeight:
            ratio = float(SCREEN_WIDTH)/float(imageWidth)
        else:
            ratio = float(SCREEN_HEIGHT)/float(imageHeight)
        imageWidth = imageWidth*ratio
        imageHeight = imageHeight*ratio
        return (int(imageWidth), int(imageHeight))
    return (SCREEN_WIDTH, SCREEN_HEIGHT)


def getPhotoImage(image, newSize):
    imageAfterResize = image.resize(newSize, Image.ANTIALIAS)
    photoImage = ImageTk.PhotoImage(imageAfterResize)
    return photoImage


def createThread(panel):
    displayProcess = threading.Thread(name='DisplayImageProcess',
                                      target=displayImageProcess,
                                      args=(DISPLAY_CONDITION, panel,))
    controlProcess = threading.Thread(name='ControlDisplayByTime',
                                      target=controlDisplayByTime,
                                      args=(DISPLAY_CONDITION,))
    PLAY_OR_STOP_EVENT.set()
    displayProcess.start()
    time.sleep(1)
    controlProcess.start()


def displayImageProcess(cond, panel):
    logging.debug('Starting displayImageProcess thread')
    while True:
        with cond:
            cond.wait()
            logging.debug('Received notify to display image...')
            oneFile = getNextFileName()
            displayImageByFileName(oneFile, panel)


def getNextFileName():
    fileSize = len(FILES)
    if fileSize > 0:
        global FILE_INDEX
        if FILE_INDEX < (fileSize - 1):
            FILE_INDEX = FILE_INDEX + 1
        else:
            FILE_INDEX = 0
        return FILES[FILE_INDEX]


def getPreviousFileName():
    fileSize = len(FILES)
    if fileSize > 0:
        global FILE_INDEX
        if FILE_INDEX == -1 or FILE_INDEX == 0:
            FILE_INDEX = fileSize - 1
        else:
            FILE_INDEX = FILE_INDEX - 1
        return FILES[FILE_INDEX]


def displayImageByFileName(fileName, panel):
        if not os.path.isfile(PHOTOS_PATH + '/%s' % fileName):
            logging.debut('File donot exist!')
            return
        if not (fileName.endswith('.jpg') or fileName.endswith('.JPG')):
            return
        pictureName = PHOTOS_PATH + '/%s' % fileName
        changeImageOnPanel(pictureName, panel)


def changeImageOnPanel(pictureName, panel):
    photoImage = getPhotoImageByName(pictureName)
    panel.configure(image=photoImage)
    panel.image = photoImage


def controlDisplayByTime(cond):
    logging.debug('Starting controlDisplayByTime thread...')
    while True:
        time.sleep(INTERVAL)
        PLAY_OR_STOP_EVENT.wait()
        with cond:
            logging.debug('Send display image notify...')
            cond.notifyAll()


def manualPageTurning(event):
    x = event.x
    labelCellWidth = SCREEN_WIDTH / 3
    if x > 0 and x < labelCellWidth:
        logging.debug("Clicked at left of image")
        stopDisplayImage()
        oneFile = getPreviousFileName()
        displayImageByFileName(oneFile, event.widget)
    elif x > labelCellWidth and x < labelCellWidth * 2:
        logging.debug("Clicked at mid of image")
        if PLAY_OR_STOP_EVENT.isSet():
            PLAY_OR_STOP_EVENT.clear()
        else:
            logging.debug('Restore display image...')
            PLAY_OR_STOP_EVENT.set()
    elif x > labelCellWidth * 2 and x < labelCellWidth * 3:
        logging.debug("Clicked at right of image")
        stopDisplayImage()
        oneFile = getNextFileName()
        displayImageByFileName(oneFile, event.widget)


def stopDisplayImage():
    if PLAY_OR_STOP_EVENT.isSet():
        logging.debug('Stopping display image...')
        PLAY_OR_STOP_EVENT.clear()


if __name__ == '__main__':
    tkRoot = Tk()
    panel = initPanel(tkRoot)
    panel.bind("<Button-1>", manualPageTurning)
    createThread(panel)
    tkRoot.mainloop()
