#!/usr/bin/env python2
#Author: P. Beukema February 2016
import math
import random
import pandas as pd
import numpy as np

import time
import os
import csv
import seaborn as sns
import matplotlib.pyplot as plt

from psychopy import visual, core, event, gui, data
from sklearn import linear_model

# Grab user info and set up output files for analysis
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'FlashLagPilot'
expInfo = {u'User': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
outputfn =  _thisDir + os.sep +'data/%s_%s_%s.csv' %(expInfo['User'], \
            expName, expInfo['date'])
dataOut = pd.DataFrame(columns = ('rot','trials'))
grabMeans = pd.DataFrame()
deg_sign= u'\N{DEGREE SIGN}'

'''
Initalize stimuli parameters
all units are in pixels to show correctly on any sized screen
user may wish to modify for optimality on small or larger screens
tested on 1920x1080 (widescreen) display
'''

dotRad = (45,45)
flashRad = (45,45)
circleRadius = 125
flashRadius = circleRadius+35 # displacement from target in pixels

# Set up Window
win = visual.Window([500,500], monitor = 'testMonitor', color = [-1,-1,-1], \
       colorSpace = 'rgb', blendMode = 'avg', useFBO = True, allowGUI = \
       False,fullscr=False,waitBlanking=False)

# Initalize Instructions Text
instructions = '====================================================== \n In this task, you will see two dots appear on the screen. The first dot is white and will appear at the top center of your screen and move in a clockwise circle. The second dot is yellow and will flash in the bottom half of your screen. \n \n Your objective is to move the yellow flashing dot at the bottom of the screen to be vertically aligned with the white dot at the 6 o-clock position. Use the left and right arrow keys to move the yellow dot in your desired direction. Pressing the left arrow key will rotate the flash clockwise (leftwards), pressing the right arrow key will rotate the flash anti-clockwise (rightwards).  \n \n The dot only moves slightly after each press, so you may have to hit the arrow keys multiple times before you notice any large movement. When you believe that the yellow and white dots are vertically aligned (at the 6 o-clock position), press the spacebar and the experiment will end.  ======================================================'
completedText = 'End of Testing. Thank you.'

instrText = visual.TextStim(win = win, ori = 0, name = 'instrText', text=instructions, font = u'Arial',  pos = [0, 0], height = 0.05, wrapWidth = None, color = u'white', colorSpace = 'rgb', opacity = 1, depth = 0.0)

expCompletedText = visual.TextStim(win = win, ori = 0, name = 'instrText', text=completedText, font = u'Arial',  pos = [0, 0], height = 0.05, wrapWidth = None, color = u'white', colorSpace = 'rgb', opacity = 1, depth = 0.0)


fixSpot = visual.GratingStim(win, tex = None, mask = 'gauss', size = (20,20), \
          units='pix', color = 'cyan', autoDraw = False)
clockDot = visual.GratingStim(win = win, mask = 'gauss', size = dotRad, \
           color = 'white', units='pix', opacity = '1', autoDraw=False)
flashDot = visual.GratingStim(win = win, mask = 'gauss', units='pix', \
           size = flashRad,color = 'yellow')


#-------Set Up Routine "Instructions"-------
notStarted = 0
started = 1
instructions_response = event.BuilderKeyResponse()
instructions_response.status = notStarted
InstructionsComponents = []
InstructionsComponents.append(instrText)
InstructionsComponents.append(instructions_response)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = notStarted

#-------Start Routine "Instructions"-------
continueRoutine = True
endExpNow = False
while continueRoutine:
    instrText.setAutoDraw(True)
    theseKeys = event.getKeys()
    if 'escape' in theseKeys:
        endExpNow = True
    if len(theseKeys) > 0:
        continueRoutine = False
    if endExpNow or event.getKeys(keyList=['escape']):
        core.quit()
    if continueRoutine:
        win.flip()

for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'setAutoDraw'):
        thisComponent.setAutoDraw(False)

#-------End Routine "Instructions"-------
win.flip()
core.wait(.5)
fixSpot.setAutoDraw(False)


#-------End Routine "Practice"-------
win.flip()
core.wait(2)

#-------Start Routine "Main Experiment"-------


expComplete = 0
nTrials = 0 #to record how long it took subject to get to answer
keyMapDict = {'left': 1, 'right':-1}
increment = 0 #start at super easy detection threshold
trials = range(0,12) # do 10 trials
devInc = [16,16,8,8,8,8,4,4,4,4,4,4, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2, 2,2,2]
 
increment = 0
expComplete = 0
nFlips = 0
key_prev = '0'
for dev in devInc:
    if nFlips == 15:
        break
    if 'escape' in theseKeys:
        core.quit()
    frameN = 0
    flash = False

    # project sphere for 800 ms so that user directs focus to sphere
    angleRad = math.radians(0)
    x = circleRadius*math.sin(angleRad)
    y = circleRadius*math.cos(angleRad)
    clockDot.setPos([x,y])
    clockDot.setAutoDraw(True)
    clockDot.draw()
    win.flip()
    core.wait(.8)
    #targetSide= random.choice([-1,1])
    #angleDev = random.choice([192]) #randomize where target is set
    angleDev = random.choice([192, 224, 160])
    for angle in np.arange(0,361,2):
        angleRad = math.radians(angle)
        x = circleRadius*math.sin(angleRad)
        y = circleRadius*math.cos(angleRad)
        clockDot.setPos([x,y])
        clockDot.draw()
        if angle == angleDev:
            angleMark = angle
            angleRad = math.radians(angleMark+increment)
            x2 = flashRadius*math.sin(angleRad)
            y2 = flashRadius*math.cos(angleRad)
            flash = True
        # set position of flash
        if frameN <= 1 and flash: # show flash for 1 frames
            flashDot.setPos([x2,y2])
            flashDot.draw()
            frameN = frameN+1
        win.flip()
        if event.getKeys(keyList ='escape'):
            core.quit()
        event.clearEvents('mouse')

    # Turn off stimulus and wait for response
    clockDot.setAutoDraw(False)
    win.update()
    win.flip()
    theseKeys = event.waitKeys(float('inf'), keyList=('left', 'right', 'escape', 'space'), timeStamped = False)

    # Check if user wants to quit
    if 'escape' in theseKeys:
        core.quit()
    key_response = theseKeys[0]

    if key_prev != key_response:
        nFlips = nFlips + 1
        print nFlips
    # Check response
    if key_response == 'left': #user wants to push the flash backwards
        increment = np.multiply(dev, 1)

    elif key_response == 'right': #user wants to push the flash forward
        increment = np.multiply(dev, -1)
    elif key_response == 'space': #user judges stimuli to be aligned.
        expComplete = 1
    key_prev = key_response
    print 'increment', increment
    nTrials += 1
    print 'nTrial', nTrials
dataOut.loc[0] = [increment, nTrials]
dataOut.to_csv(outputfn, index = False)


#-------End Routine "Main Experiment"-------
expCompletedText.setAutoDraw(True)
win.flip()


#-------Set Up Routine "Experiment Complete"-------
notStarted = 0
started = 1
instructions3_response = event.BuilderKeyResponse()
instructions3_response.status = notStarted
InstructionsComponents3 = []
InstructionsComponents3.append(expCompletedText)
InstructionsComponents3.append(instructions_response)
for thisComponent in InstructionsComponents3:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = notStarted

#-------Start Routine "Instructions"-------
continueRoutine = True
endExpNow = False
while continueRoutine:
    expCompletedText.setAutoDraw(True)
    theseKeys = event.getKeys()
    if 'escape' in theseKeys:
        endExpNow = True
    if len(theseKeys) > 0:
        continueRoutine = False
    if endExpNow or event.getKeys(keyList=['escape']):
        core.quit()
    if continueRoutine:
        win.flip()

for thisComponent in InstructionsComponents3:
    if hasattr(thisComponent, 'setAutoDraw'):
        thisComponent.setAutoDraw(False)
