from Point import Point
from GlobalFuncs import *

import os, math, random
from copy import deepcopy

import numpy as np

GROUND_FRICTION = 1.5
LEG_ADJ = [35, 35]
LANDER_FUEL = 500000
LANDER_LEG_STRENGTH = 55
LANDER_THRUST = 4
LANDER_SIDE_THRUST = 1

class Lander:
    def __init__(self, startPoint = Point):
        self.loc = startPoint

        self._image =       loadImage('lander.png')
        self._fire =        loadImage('fire1.png')
        self._fireLeft =    loadImage('fireLeft.png')
        self._fireRight =   loadImage('fireRight.png')
        self.image =        self._image
        self.fire =         self._fire
        self.fireLeft =     self._fireLeft
        self.fireRight =    self._fireRight
        self.explosion0 =   loadImage('explosion3.png')
        self.explosion1 =   loadImage('explosion2.png')
        self.explosion2 =   loadImage('explosion1.png')
        # self.fire2 = loadImage('fire2.png')

        self.size = self.image.get_size()
        self.fuel = LANDER_FUEL
        # self.isLanded = False
        self.exploded = False
        self.rotation = 0

        self.thrusters = {
            'right':  False,
            'left':   False,
            'bottom': False
        }

        self.momentum = {
            'vert': 0,
            'horz': 0
        }

        # self.momentum = pygame.math.Vector2(0, 0)


    # The surface is only for debugging
    def update(self, gravity, thrusters, groundPoints, surface, offset = Point(0, 0)):
        if not self.exploded:
            gp = getGroundPoints(groundPoints)

            centerPoint = Point(self.image.get_rect().center) + (self.loc - (Point(self.size) / 2)) + offset

            bottomRight = Point(self._image.get_rect().bottomright) + (centerPoint - (Point(self.size) / 2))
            bottomLeft  = Point(self._image.get_rect().bottomleft)  + (centerPoint - (Point(self.size) / 2))
            topRight    = Point(self._image.get_rect().topright)    + (centerPoint - (Point(self.size) / 2))
            topLeft     = Point(self._image.get_rect().topleft)     + (centerPoint - (Point(self.size) / 2))

            # tr = rotatePoint(topRight,    -self.rotation, centerPoint)
            # tl = rotatePoint(topLeft,     -self.rotation, centerPoint)
            br = rotatePoint(bottomRight, -self.rotation, centerPoint)
            bl = rotatePoint(bottomLeft,  -self.rotation, centerPoint)

            Lleg = bl
            Rleg = br

            # print(offset)
            # drawAllGroundPoints(surface, gp)

            LlegInContact = findClosestXPoint(Lleg, gp, offsetIndex=offset.x).y <= Lleg.y
            RlegInContact = findClosestXPoint(Rleg, gp, offsetIndex=offset.x).y <= Rleg.y

            #* Check if the lander is at all in contact with the ground
            if RlegInContact or LlegInContact:
                # We're comin' in too hot!
                if self.momentum['vert'] > LANDER_LEG_STRENGTH or self.momentum['horz'] > LANDER_LEG_STRENGTH * 1.5:
                    self.explode(surface)

                if self.momentum['vert'] > 0:
                    self.momentum['vert'] = 0
                if self.momentum:
                    self.momentum['horz'] /= GROUND_FRICTION
            else:
                self.momentum['vert'] += gravity


            #* Check if only the right leg is in contact with the ground
            if RlegInContact and not LlegInContact:
                self.rotation += abs(self.momentum['horz'] / gravity) + abs(self.momentum['vert'] / gravity)

            #* Check if only the left leg is in contact with the ground
            if LlegInContact and not RlegInContact:
                self.rotation -= abs(self.momentum['horz'] / gravity) + abs(self.momentum['vert'] / gravity)
                
            self.image = pygame.transform.rotate(self._image, self.rotation)

            # pygame.draw.circle(surface, [255, 0, 0], .data(), 5)

            if self.fuel < 0:
                self.fuel = 0
            
            # When the lander is going fast, the fire gets out of place
            centerPoint += Point(self.momentum['horz'], self.momentum['vert']) / 10

            #* Apply thrusters and display fire
            if self.fuel:
                if thrusters['bottom']:
                    self.momentum['vert'] -= LANDER_THRUST * math.cos(math.radians(self.rotation))
                    self.momentum['horz'] -= LANDER_THRUST * math.sin(math.radians(self.rotation))
                    self.fuel -= LANDER_THRUST

                    self.fire, where = rotateSurface(self._fire, -self.rotation, centerPoint.data(), pygame.math.Vector2(random.randint(-2, 2), 51))
                    surface.blit(self.fire, where)

                if thrusters['left']:
                    self.momentum['vert'] -= LANDER_SIDE_THRUST * math.sin(math.radians(self.rotation))
                    self.momentum['horz'] -= LANDER_SIDE_THRUST * math.cos(math.radians(self.rotation))
                    self.fuel -= LANDER_SIDE_THRUST

                    self.fireRight, where = rotateSurface(self._fireRight, -self.rotation, centerPoint.data(), pygame.math.Vector2(40, random.randint(-1, 1)))
                    surface.blit(self.fireRight, where)

                if thrusters['right']:
                    self.momentum['vert'] += LANDER_SIDE_THRUST * math.sin(math.radians(self.rotation))
                    self.momentum['horz'] += LANDER_SIDE_THRUST * math.cos(math.radians(self.rotation))
                    self.fuel -= LANDER_SIDE_THRUST

                    self.fireLeft, where = rotateSurface(self._fireLeft, -self.rotation, centerPoint.data(), pygame.math.Vector2(-40, random.randint(-1, 1)))
                    surface.blit(self.fireLeft, where)

            self.loc.x += self.momentum['horz'] / 10
            self.loc.y += self.momentum['vert'] / 10

            surface.blit(self.image, (self.loc - (Point(self.size) / 2) + offset).data())
    

    def reset(self, loc=None):
        if loc is not None:
            self.loc = loc
        self.momentum['vert'] = 0
        self.momentum['horz'] = 0
        self.exploded = False
        self.fuel = LANDER_FUEL


    def explode(self, surface, initial=False, offset = Point(0, 0)):
        if not self.exploded or initial:
            self.exploded = True
            surface.blit(self.explosion0, (self.loc + offset - self.size + 12).data())
        else:
            surface.blit(random.choice([self.explosion1, self.explosion2]), (self.loc + offset - self.size + 12).data())