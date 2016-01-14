#!/usr/bin/env python2

from psychopy import visual, core, event, gui, data
import time, os, csv
import math, random
import pandas as pd
import numpy as np
#import seaborn as sns
import matplotlib.pyplot as plt

#Set up Output file for reading and writing
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'Flash Lag Pilot'  # from the Builder filename that created this script
expInfo = {u'User': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; # Output summary data and analyzed files
filename = _thisDir + os.sep + 'data/%s_%s' %(expInfo['User'], expName)
outputfn =  _thisDir + os.sep +'data/%s_%s_%s.csv' %(expInfo['User'], expName, expInfo['date'])
data_out = pd.DataFrame(columns=('response','correct','rotation'))

#Initalize variables
dotRad = (0.085,0.085)
flashRad = (0.085,0.085)
circleRadius = .40
flashRadius = circleRadius+.1

#Set up Window
win = visual.Window([1000,1000], monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True)

#Initalize Instructions Text
instrText = visual.TextStim(win=win, ori=0, name='instrText',
    text=u'In this experiment you will observe a rotating white sphere and a flashed yellow sphere. If the flash appears ahead of the white sphere, press \u2190, if it appears behind the white sphere, press \u2192. \n \n Press any key continue.',    font=u'Arial',
    pos=[0, 0], height=0.05, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

fixSpot = visual.GratingStim(win,tex=None, mask="gauss", size=(0.05,0.05),color='white', autoDraw=False)
clockDot = visual.GratingStim(win=win, mask='gauss', size=dotRad, color='white', opacity = '0.9', autoDraw=False)
flashDot = visual.GratingStim(win=win, mask="gauss", size=flashRad,color='yellow')

#Build vector of trialTypes, These will be random for each user.
#May be better to have one version of these and load them rather than build dynamically for each user.
#Also add line to save these automatically for each user.
trialType = np.repeat([-20,0,20,40,60],20)
myDict = {'-20': 'right', '0': 'right', '20': 'left', '40': 'left', '60': 'left'}
randTrials = np.random.permutation(trialType)
response = [myDict[str(i)] for i in randTrials]
anglePres = np.arange(90,210,10) #this is the angle at which the flashed yellow sphere will be drawn.
values = [random.choice(anglePres) for _ in xrange(100)] #random choice with replacement
print values
#-------Set Up "Instructions"-------
NOT_STARTED = 0
STARTED=1
instructions_response = event.BuilderKeyResponse()
instructions_response.status = NOT_STARTED
InstructionsComponents = []
InstructionsComponents.append(instrText)
InstructionsComponents.append(instructions_response)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Instructions"-------
continueRoutine = True
endExpNow=False
while continueRoutine:
    instrText.setAutoDraw(True)
    theseKeys = event.getKeys()
    if "escape" in theseKeys:
        endExpNow = True
    if len(theseKeys) > 0:  # at least one key was pressed
        continueRoutine = False
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
#-------End Routine "Instructions"-------
win.flip()
core.wait(3)
fixSpot.setAutoDraw(False)

#-------Start Routine "Main Experiment"-------
for rot, angleDev, response in zip(randTrials, values, response):
    clockDot = visual.GratingStim(win=win, mask='gauss', size=dotRad, color='white', opacity = '0.9', autoDraw=False)
    core.wait(.5)
    #Check if user wants to quit
    if "escape" in theseKeys:
        core.quit()
    frameN=0
    flash=False
    for angle in np.arange(0,361,10):

        angleRad = math.radians(angle)
        x = circleRadius*math.sin(angleRad)
        y = circleRadius*math.cos(angleRad)
        clockDot.setPos([x,y])
        clockDot.draw()

        if angle == angleDev :
            angleMark = angle
            angleRad = math.radians(angleMark+rot)
            x2 = flashRadius*math.sin(angleRad)
            y2 = flashRadius*math.cos(angleRad)
            flash = True
        #set position of flash
        if frameN <= 4 and flash:
            flashDot.setPos([x2,y2])
            flashDot.draw()
            frameN = frameN+1
        win.flip()

        if event.getKeys(keyList="escape"):
            core.quit()
        event.clearEvents('mouse') #only really needed for pygame windows
    win.flip()

    theseKeys = event.waitKeys(float('inf'), keyList=('left', 'right', 'escape'), timeStamped = False)
    #Check if user wants to quit
    if "escape" in theseKeys:
        core.quit()
    key_response = theseKeys[0]
    #was the response correct?

    correct = key_response==response
    data_out.loc[len(data_out)+1]=[key_response, correct, rot]
    data_out.to_csv(outputfn, index=False)
    core.wait(.5)

#-------End Routine "Main Experiment"-------

#-------Analyze Data and To do: Fit Logit model----
grabMeans = data_out.groupby(['rotation']).mean().reset_index()
plt.figure(figsize=(4,4))
sns.regplot(x='rotation', y='correct', data=grabMeans,fit_reg=False)
plotfn =  _thisDir + os.sep +'data/%saccuracy_%s_.png' %(expInfo['User'], expName)
plt.savefig(plotfn)
