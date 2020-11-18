from Config import DATA
import os
from GlobalFuncs import *

def preloadFrames(dir, scale=None, loadingBar=None):
    numFrames = len(os.listdir(DATA + '/' + dir))
    frames = []

    if scale is None:
        for i in range(numFrames):
            frames.append(loadImage(dir + str(i) + '.png'))
            if loadingBar is not None: 
                loadingBar.progress()
    else:
        for i in range(numFrames):
            frames.append(pygame.transform.scale(loadImage(dir + str(i) + '.png'), scale))
            if loadingBar is not None: 
                loadingBar.progress()

    return frames

class Animation:
    def __init__(self, dir=None, scale=None, startFrame=0, loop=True, secondsPerLoop=1, preloadedFrames=None):
        self.currentFrame = startFrame
        self.secondsPerLoop = secondsPerLoop
        self.loop = loop

        if preloadedFrames is None:
            self.numFrames = len(os.listdir(DATA + '/' + dir))
            self.frames = []

            if scale is None:
                for i in range(self.numFrames):
                    self.frames.append(loadImage(dir + str(i) + '.png'))
            else:
                for i in range(self.numFrames):
                    self.frames.append(pygame.transform.scale(loadImage(dir + str(i) + '.png'), scale))
        else:
            assert(scale is None and dir is None)
            self.numFrames = len(preloadedFrames)
            self.frames = preloadedFrames


    def animate(self):
        if self.secondsPerLoop < 1:
            self.currentFrame += 1 / self.secondsPerLoop
        else:
            self.currentFrame += 1

        if self.currentFrame >= self.numFrames * self.secondsPerLoop:
            if self.loop:
                self.currentFrame = 0
            else:
                return

        return self.frames[int(self.currentFrame / self.secondsPerLoop)]


    def getSize(self):
        return self.frames[0].get_size()