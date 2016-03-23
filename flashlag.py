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
dataOut = pd.DataFrame(columns = ('response','correct','rotation'))
grabMeans = pd.DataFrame()
deg_sign= u'\N{DEGREE SIGN}'

'''
Initalize stimuli parameters
all units are in pixels to show correctly on any sized screen
user may wish to modify for optimality on small or larger screens
tested on 1920x1080 (widescreen) display
'''

dotRad = (55,55)
flashRad = (55,55)
circleRadius = 125
flashRadius = circleRadius+35 # displacement from target in pixels

# Set up Window
win = visual.Window([1000,1000], monitor = 'testMonitor', color = [-1,-1,-1], \
       colorSpace = 'rgb', blendMode = 'avg', useFBO = True, allowGUI = \
       False,fullscr=True)

# Initalize Instructions Text
instructions = '====================================================== \n This is a test of how well you can see movement and track relative motion. For each trial you will see a blinking white light moving along a circular path. As the white light moves around in a circle, there will also be a single yellow flash. The yellow flash will appear at different points around the path of the white light. \n \n Your task is to determine if the yellow flash appears ahead of the blinking white light, or behind it. \n \n Some trials will be easier than others. Don\'t worry if you find some of these trials very difficult, just do your best. Try to track the white blinking light as it moves around, and look for the yellow flash. If the yellow flash appears ahead of the blinking white light, press the \'up\' arrow. If the yellow flash appears behind the blinking white light, press the \'down\' arrow.\n \n  If you are unsure about your response, make your best guess. The entire test takes 3 minutes. \n \n The first trials will be a practice session to acquaint you with the requirements, followed by a window signalling the actual test.  Get ready, and press any key to begin. ====================================================== '

instructions_Practice = 'End of practice session. Press any key to continue.'
completedText = 'End of Testing. Thank you.'
instrText = visual.TextStim(win = win, ori = 0, name = 'instrText', text=instructions, font = u'Arial',  pos = [0, 0], height = 0.05, wrapWidth = None, color = u'white', colorSpace = 'rgb', opacity = 1, depth = 0.0)

instrPracticeText = visual.TextStim(win = win, ori = 0, name = 'instrText', text=instructions_Practice, font = u'Arial',  pos = [0, 0], height = 0.05, wrapWidth = None, color = u'white', colorSpace = 'rgb', opacity = 1, depth = 0.0)

expCompletedText = visual.TextStim(win = win, ori = 0, name = 'instrText', text=completedText, font = u'Arial',  pos = [0, 0], height = 0.05, wrapWidth = None, color = u'white', colorSpace = 'rgb', opacity = 1, depth = 0.0)


fixSpot = visual.GratingStim(win, tex = None, mask = 'gauss', size = (20,20), \
          units='pix', color = 'white', autoDraw = False)
clockDot = visual.GratingStim(win = win, mask = 'gauss', size = dotRad, \
           color = 'white', units='pix', opacity = '0.9', autoDraw=False)
flashDot = visual.GratingStim(win = win, mask = 'gauss', units='pix', \
           size = flashRad,color = 'yellow')

# Build vector of trials, dynamically generated for each new user


trialType = np.repeat([-32,-16,-8,0,8,16,32],20) # 20 trials for each of 5
myDict = {'-32': 'down', '-16': 'down', '-8': 'down', '0': 'down', '8': 'up', '16': 'up', '32': 'up'}
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
core.wait(2)
fixSpot.setAutoDraw(False)


practiceTrials = np.repeat([-32,-16,-8,0,8,16,32],1) # 20 trials for each of 5
anglePres = np.arange(88,264,8) # yellow flash
values = [random.choice(anglePres) for _ in xrange(100)]

#-------Start Routine "Practice Experiment"-------
for rot, angleDev, prac_response in zip(practiceTrials, values, response):
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
    theseKeys = event.waitKeys(float('inf'), keyList=('up', 'down', 'escape'), timeStamped = False)

    # Check if user wants to quit
    if 'escape' in theseKeys:
        core.quit()
    core.wait(.5)

#Instructions for Practice Epxeriment
#-------Set Up Routine "Practice"-------
notStarted = 0
started = 1
instructions2_response = event.BuilderKeyResponse()
instructions2_response.status = notStarted
InstructionsComponents2 = []
InstructionsComponents2.append(instrPracticeText)
InstructionsComponents2.append(instructions_response)
for thisComponent in InstructionsComponents2:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = notStarted

#-------Start Routine "Instructions"-------
continueRoutine = True
endExpNow = False
while continueRoutine:
    instrPracticeText.setAutoDraw(True)
    theseKeys = event.getKeys()
    if 'escape' in theseKeys:
        endExpNow = True
    if len(theseKeys) > 0:
        continueRoutine = False
    if endExpNow or event.getKeys(keyList=['escape']):
        core.quit()
    if continueRoutine:
        win.flip()

for thisComponent in InstructionsComponents2:
    if hasattr(thisComponent, 'setAutoDraw'):
        thisComponent.setAutoDraw(False)

#-------End Routine "Practice"-------
win.flip()
core.wait(2)

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
expCompletedText.setAutoDraw(True)
win.flip()

#-------Summarize data and fit logistic regression----

#grabMeans = dataOut.groupby(['rotation'], as_index=False).mean()
grabMeans = pd.DataFrame(columns=('rotation', 'accuracy'))
i=0
for rot in np.unique(dataOut[['rotation']]):
    block_df = dataOut.loc[dataOut['rotation']==rot]
    mean_acc = block_df[['correct']].mean()
    grabMeans.loc[i] = [rot, mean_acc.correct]
    i=i+1

dataOut.loc[dataOut.response == 'down', ['response']] = 0
dataOut.loc[dataOut.response == 'up', ['response']] = 1
dataOut[['response']] = dataOut[['response']].astype(float)
X = np.array(dataOut['rotation'])
X = X[:,np.newaxis]
#X = X/np.linalg.norm(X)
Y = np.array(dataOut['response'])
clf = linear_model.LogisticRegression()
clf.fit(X, Y)

PSE = (clf.intercept_/-clf.coef_)[0][0] #Point of Subjective Equality
A = clf.intercept_
B = clf.coef_
x=PSE
precision =  -(B/(1 + np.exp(A + B*x))**2) + B/(1 + np.exp(A + B*x))

#Generate figure summary, and output summary annotated graph
plt.figure(figsize=(6,6))
g = sns.lmplot(x="rotation", y="response", data=dataOut,logistic=True, y_jitter=.02);
rots = np.unique(dataOut[['rotation']])
maxx = max(rots) + 5
minx = min(rots) - 5
xaxlabel = "Rotation(%s)"% (deg_sign)
yaxlabel = "Reported Flash Appearance"
ytics = ['Before', ' ','Ahead']
g = g.set_axis_labels(xaxlabel, yaxlabel).set(xlim=(minx, maxx), ylim=(-.25, 1.25),xticks=rots, yticks=[0, .5, 1], yticklabels = ytics)
h = plt.scatter(PSE,.5,s=50, facecolor='black')
PSE = (clf.intercept_/-clf.coef_)[0][0]
precision =  -(B/(1 + np.exp(A + B*x))**2) + B/(1 + np.exp(A + B*x))
PSE_trunc = "%.2f" % PSE
precision_trunc = "%.3f" % precision
annotation = "P.S.E. = %s%s\nSlope = %s" % (PSE_trunc,deg_sign, precision_trunc)
plt.annotate(annotation, xy = (PSE,.5),xytext = (-5, 5), textcoords = 'offset \
             points', ha = 'right', va = 'bottom')
plotfn =  _thisDir + os.sep +'data/%saccuracy_%s_.png' %(expInfo['User'], \
          expName)
plt.savefig(plotfn)

#generate summary data files
summary_analysis = pd.DataFrame(columns=('PSE', 'Precision'))
summary_analysis.loc[0] = [PSE, precision[0][0]]

#save datafiles to csv, note raw data saved above after each keystroke, here is summary data
meansfn =  _thisDir + os.sep +'data/%smeans_%s_.csv' %(expInfo['User'], expName)
summaryfn =  _thisDir + os.sep +'data/%ssummary_%s_.csv' %(expInfo['User'], expName)
grabMeans.to_csv(meansfn, index = False)
summary_analysis.to_csv(summaryfn, index = False)


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
