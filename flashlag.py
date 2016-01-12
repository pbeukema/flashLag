#!/usr/bin/env python2

from psychopy import visual, core, event, gui, data
import numpy as np
import time
from math import sin, cos, radians
from random import shuffle, randint, uniform
import os, csv
import random
import math
import os
import pandas as pd

#Set up Output file for reading and writing
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'flashLag_Pilot'  # from the Builder filename that created this script
expInfo = {u'Day': u'', u'User': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; # Output summary data and analyzed files
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['User'], expName, expInfo['date'])
outputfn =  _thisDir + os.sep +'data/%s_summary_%s_%s_Day_%s.csv' %(expInfo['User'], expName, expInfo['date'], expInfo['Day'])
data_out = pd.DataFrame(columns=('response','actual','correct'))

#Initalize variables
dotRad = (0.05,0.05)
flashRad = (0.1,0.1)
circleRadius = .15
flashRadius = circleRadius+.1
angle = 0 #start position is vertical
nTrials = 100

win = visual.Window([800,800], monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True)

second = visual.ShapeStim(win, vertices= [[0,0.00], [0,0.8]], lineColor=[1,1,1],fillColor=[1,1,1], interpolate=False, lineWidth=1, autoLog=False, autoDraw=False)

fixSpot = visual.GratingStim(win,tex=None, mask="gauss", size=(0.05,0.05),color='white', autoDraw=True)
clock = core.Clock() # to grab RTs, -- maybe make global?

clockDot = visual.GratingStim(win=win, mask="gauss", size=dotRad, color='white', opacity = '0.5', autoDraw=True)
flashDot = visual.GratingStim(win=win, mask="gauss", size=flashRad,color='yellow')

#Build vector of trialTypes
trialType = np.repeat([-20,-10,0,10,20],20)
myDict = {'-20': 'left', '-10': 'left', '0': 'down', '20': 'right', '10': 'right'}

randTrials = np.random.permutation(trialType)
response = [myDict[str(i)] for i in randTrials]
anglePres = np.arange(30,330,10)
values = [random.choice(anglePres) for _ in xrange(100)]
angle = np.arange(0,370,10)
fixSpot.draw()
#ie forever Hard capped to 60Hz refresh unless have better comp but not likely, therefore accuracy limited to +/- min(~16 ms).
    # add function to randomize the direction of motion to minimize adaptation, or anticipation
    #if angle % 360 == 0 and angle != 0:
    #    trial = trial+1
    #    angle = angle+((-1)**trial)*angleInc
for rot, angleDev, response in zip(randTrials, values, response):
    event.clearEvents(eventType ='keyboard') #can remove, done implicity in event.waitKeys below
    for angle in np.arange(0,370,5):
        angleRad = radians(angle)
        x = circleRadius*sin(angleRad)
        y = circleRadius*cos(angleRad)
        clockDot.setPos([x,y])
        clockDot.draw()

        if angle == angleDev:
            angleRad = radians(angle+rot)
            x = flashRadius*sin(angleRad)
            y = flashRadius*cos(angleRad)
            flashDot.setPos([x,y])
            flashDot.draw()
        win.flip()
        if event.getKeys(keyList="escape"):
            core.quit()
        event.clearEvents('mouse') #only really needed for pygame windows
    win.flip()

    theseKeys = event.waitKeys(float('inf'), keyList=('left', 'right', 'down'), timeStamped = False)
    key_response = theseKeys[0]
    #was the response correct?
    correct = key_response==response
    data_out.loc[len(data_out)+1]=[key_response,response, correct]
    data_out.to_csv(outputfn, index=False)
    core.wait(1)
