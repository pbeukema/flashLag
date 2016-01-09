#!/usr/bin/env python2
from psychopy import visual, core, event
import numpy, time
from math import sin, cos, radians
from random import shuffle, randint, uniform
import os, csv

dotSize = .25
circleRadius = dotSize
win = visual.Window([800,800], monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True)

handVerts = numpy.array([ [0,0.8],[-0.05,0],[0,-0.05],[5,0] ])#vertices (using numpy means we can scale them easily)

second = visual.ShapeStim(win, vertices= [[0,0.00], [0,0.8]], lineColor=[1,1,1],fillColor=[1,1,1], interpolate=False, lineWidth=1, autoLog=False, autoDraw=False)

#flash = visual.ShapeStim(win, vertices= [[0,0.85], [0,1.4]], lineColor=[1,1,1],fillColor=[1,1,1], interpolate=True, lineWidth=1, autoLog=False)

fixSpot = visual.GratingStim(win,tex=None, mask="gauss", size=(0.05,0.05),color='white')
clock = core.Clock() # to grab RTs, -- maybe make global?


clockDot = visual.PatchStim(win=win, mask="gauss", size=(0.12,0.12),color='white')

flashDot = visual.PatchStim(win=win, mask="gauss", size=(0.1,0.1),color='yellow')

while True: #ie forever Hard capped to 60Hz refresh unless have better comp but not likely, therefore accuracy limited to +/- min(~16 ms).
    fixSpot.draw()
    t = time.localtime()
    angleRad = radians(second.ori)
    x = circleRadius*sin(angleRad)
    y = circleRadius*cos(angleRad)
    clockDot.setPos([x,y])
    clockDot.draw()

    flashRadius = circleRadius+.1
    angleRad = radians(second.ori)
    x = flashRadius*sin(angleRad)
    y = flashRadius*cos(angleRad)
    flashDot.setPos([x,y])
    #flashDot.draw()

    #secPos = 0 #NB floor will round down to previous second

    # To make this adaptive just take second.ori and add staircase to adaptRate.
    second.ori = second.ori+4.5   #add adaptive staircase here
    #second.draw()

    if second.ori % 90 == 0: #jackson pollock looking hack here but its 12:16am and unclear how to do more elegant atm.
        #flash.ori = second.ori
        flashDot.draw()


    win.flip()
    if 'q' in event.getKeys():
        break
    event.clearEvents('mouse') #only really needed for pygame windows
