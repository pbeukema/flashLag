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

# Grab user info and set up output files for analysis
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'FlashLagPilot'
expInfo = {u'User': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
outputfn =  _thisDir + os.sep +'data/%s_%s_%s.csv' %(expInfo['User'], expName, expInfo['date'])
dataOut = pd.DataFrame(columns = ('response','correct','rotation'))
grabMeans = pd.DataFrame()

'''
Initalize stimuli parameters
all units are in pixels to show correctly on any sized screen
user may wish to modify for optimality on small or larger screens
tested on 1920x1080 (widescreen) display
'''

dotRad = (55,55)
flashRad = (55,55)
circleRadius = 300
flashRadius = circleRadius+35 # displacement from target in pixels

# Set up Window
win = visual.Window([1000,1000], monitor = 'testMonitor', color = [-1,-1,-1], colorSpace = 'rgb', blendMode = 'avg', useFBO = True, allowGUI = False,fullscr=True)

# Initalize Instructions Text
instrText = visual.TextStim(win = win, ori = 0, name = 'instrText',
    text=u'\n In this experiment you will observe a rotating white sphere and a flashed yellow sphere. \n If the flash appears behind the white sphere, press \u2193. \n If the flash appears ahead of the white sphere, press \u2191. \n \n Press any key continue.', font = u'Arial',  pos = [0, 0], height = 0.05, wrapWidth = None, color = u'white', colorSpace = 'rgb', opacity = 1, depth = 0.0)

fixSpot = visual.GratingStim(win, tex = None, mask = 'gauss', size = (20,20), units='pix', color = 'white', autoDraw = False)
clockDot = visual.GratingStim(win = win, mask = 'gauss', size = dotRad, color = 'white', units='pix', opacity = '0.9', autoDraw=False)
flashDot = visual.GratingStim(win = win, mask = 'gauss', units='pix', size = flashRad,color = 'yellow')

# Build vector of trials, dynamically generated for each new user
trialType = np.repeat([-32,-16,0,16,32,48],20) # 20 trials for each of 5 conditions
myDict = {'-32': 'down', '-16': 'down', '0': 'down', '16': 'up', '32': 'up', '48': 'up'}
randTrials = np.random.permutation(trialType)
response = [myDict[str(i)] for i in randTrials]
anglePres = np.arange(88,264,8) # yellow flash
values = [random.choice(anglePres) for _ in xrange(100)]

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
core.wait(3)
fixSpot.setAutoDraw(False)

#-------Start Routine "Main Experiment"-------
for rot, angleDev, response in zip(randTrials, values, response):
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


    for angle in np.arange(0,361,8):
        angleRad = math.radians(angle)
        x = circleRadius*math.sin(angleRad)
        y = circleRadius*math.cos(angleRad)
        clockDot.setPos([x,y])
        clockDot.draw()
        if angle == angleDev:
            angleMark = angle
            angleRad = math.radians(angleMark+rot)
            x2 = flashRadius*math.sin(angleRad)
            y2 = flashRadius*math.cos(angleRad)
            flash = True
        # set position of flash
        if frameN <= 1 and flash: # show flash for 4 frames
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
    theseKeys = event.waitKeys(float('inf'), keyList=('up', 'down', 'escape'), timeStamped = False)

    # Check if user wants to quit
    if 'escape' in theseKeys:
        core.quit()

    key_response = theseKeys[0]
    # Check if the response was correct
    correct = key_response == response
    dataOut.loc[len(dataOut)+1] = [key_response, correct, rot]
    dataOut.to_csv(outputfn, index = False)

    core.wait(.5)
#-------End Routine "Main Experiment"-------

#-------Analyze Data To do: Fit Logit model----
#grabMeans = dataOut.groupby(['rotation'], as_index=False).mean()
grabMeans = pd.DataFrame(columns=('rotation', 'accuracy'))

for rot in np.unique(dataOut[['rotation']]):
    block_df = dataOut.loc[dataOut['rotation']==rot]
    mean_acc = block_df[['correct']].mean()
    grabMeans.loc[i] = [rot, mean_acc.correct]

plt.figure(figsize=(6,6))
sns.regplot(x='rotation', y='accuracy', data = grabMeans, fit_reg = False)
plotfn =  _thisDir + os.sep +'data/%saccuracy_%s_.png' %(expInfo['User'], expName)
plt.savefig(plotfn)
