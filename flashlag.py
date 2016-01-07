#!/usr/bin/env python2
from psychopy import visual, core, event
import numpy, time
win = visual.Window([800,800], monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True)

handVerts = numpy.array([ [0,0.8],[-0.05,0],[0,-0.05],[5,0] ])#vertices (using numpy means we can scale them easily)

second = visual.ShapeStim(win, vertices= [[0,0.00], [0,0.8]],
    lineColor=[1,1,1],fillColor=None, lineWidth=6, autoLog=False) #dafuq autoLog?!

flash = visual.ShapeStim(win, vertices= [[0,0.85], [0,1.4]],
    lineColor=[1,1,1],fillColor=None, lineWidth=6, autoLog=False)

fixation = visual.Circle(win, units = 'pix', radius = 15, lineColor='white', fillColor = 'white')
clock = core.Clock() # to grab RTs, -- maybe make global?

while True: #ie forever Hard capped to 60Hz refresh unless have better comp but not likely, therefore accuracy limited to +/- min(~16 ms).
    fixation.draw()
    t = time.localtime()


    secPos = 0 #NB floor will round down to previous second

    second.ori = second.ori+1   #add adaptive staircase here
    second.draw()

    if second.ori % 90 == 0 and second.ori % 180 != 0 and second.ori % 270 != 0: #jackson pollock looking hack here but its 12:16am and unclear how to do more elegant atm.
        flash.ori = second.ori
        flash.draw()


    win.flip()
    if 'q' in event.getKeys():
        break
    event.clearEvents('mouse') #only really needed for pygame windows
