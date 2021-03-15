# -*- coding: utf-8 -*-
"""
@author: kevinhhl

This module creates an instance of PyCast, takes input from screenshots captured by user, 
and displays standard outputs through terminal.

Source code is publicly available on https://github.com/kevinhhl
"""
from PyCast import PyCast
import TextsForUI
import pyperclip
#from pytesseract import TesseractNotFoundError
import threading
import time
from PIL import ImageGrab
from PIL import ImageChops


DEBUG_MODE = False
ZOOM = 8            # num. of times to zoom per image input

VERSION_NUMBER = "1.1.1b"
REVISION_NUMBER = "20200926"
# TODOv.1.1.2
# TODO: set tesseract library to folder relative to root

# v.1.1.1b - refactored & added documentations

pc = PyCast(DEBUG_MODE)
resultsTable = {}   # index: listof results, where index = the number of times user has given valid input

def _printSummary(count) -> None:
    '''
    Prints results from OCR at all ZOOM levels, then takes a majority-vote to display the 
    most-likely-amount.
    '''
    # TODO: print results in sorted order (either by zoom levels, or most-likely-amounts as first priority)
    
    freqTable = {}
    for e in resultsTable[count]:
        if not e[1] in freqTable.keys():
            freqTable[e[1]] = 0
        freqTable[e[1]] += 1
    
    mxSum = 0
    mxFreq = 0
    for key in freqTable:
        value = freqTable[key]
        if value > mxFreq:
            mxSum = key
            mxFreq = value
    print("Highest frequency [{0} times] = {1}".format(mxFreq, f"{mxSum:,.2f}"))


def _worker1(c, zoom) -> None:
    ''' For multi-threadding.
    '''
    if not c in resultsTable.keys():
        resultsTable[c] = []
    results = pc.cast(zoom)
    resultsTable[c].append(results)
    print(results[2])


def waitForNewData(pc, sleep_time=0.1) -> None:
    ''' Sleeps thread until new image is copied to clipboard
    '''
    # print("Waiting for new image...")  
    if DEBUG_MODE:
        sleep_time = 1

    crnt_image = ImageGrab.grabclipboard()
    recent_image = crnt_image
    
    # Sleep until user has valid image input in clipboard 
    # {
    while crnt_image is None \
            or recent_image is not None and (pc._count > 0 and not ImageChops.difference(recent_image,crnt_image).getbbox()) \
            or type(recent_image) is list:
        time.sleep(sleep_time)
        if DEBUG_MODE:
            print("[waitForNewData] recent_img="+str(crnt_image))
        crnt_image = ImageGrab.grabclipboard()
    # }




if __name__ == "__main__":

    print(TextsForUI.HEADER.format(VERSION_NUMBER, REVISION_NUMBER))
    print(TextsForUI.INSTRUCTIONS)        
   
    # Need to clear clipboard if it contians an image copied prior to user running program; don't want to program to treat such as input
    # The expected result when there is a copied image in clipboard is a Null string
    if pyperclip.paste() == "":
        pyperclip.copy("")
    
    # Main Loop begins
    # {
    print("\nPyCast is now running...")
    count = 1
    while True:
        try:
            waitForNewData(pc)
        except Exception as e:
            if DEBUG_MODE:
                print("Caught error during waitForNewData(pc): " + str(e))
        
        # Calculating at all ZOOM levels in concurrent threads
        for i in range(ZOOM):
            zoomLvl = i + 1
            threading.Thread(target=_worker1,args=(count, zoomLvl,)).start()
        
        # Thread safety - wait until all processes in above threads are done
        while count not in resultsTable.keys() or len(resultsTable[count]) < ZOOM:
            time.sleep(0.1)

        _printSummary(count)    
        count += 1
    # } End of Main Loop
