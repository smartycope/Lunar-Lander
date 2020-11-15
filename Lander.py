from GlobalFuncs import *
from Config import *
import os, math, random
from copy import deepcopy
import numpy as np

class Lander:
    def __init__(self, startPoint = Pointf(0, 0)):
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

        self.size = self.image.get_size()
        # self.fuel = LANDER_FUEL
        self.fuel = 0
        self.exploded = False
        self.rotation = 0
        self.mass = LANDER_WEIGHT

        self.thrusters = {
            'right':  False,
            'left':   False,
            'bottom': False
        }

        self.momentum = {
            'vert': 0,
            'horz': 0
        }


    def update(self, gravity, groundPoints, surface, offset = Pointf(0, 0)):
        if not self.exploded:
            self.mass = LANDER_WEIGHT + (self.fuel * FUEL_WEIGHT)
            gp = getGroundPoints(groundPoints)

            centerPoint = Pointf(self.image.get_rect().center) + (self.loc - (Pointf(self.size) / 2)) + offset

            bottomRight = Pointf(self._image.get_rect().bottomright) + (centerPoint - (Pointf(self.size) / 2))
            bottomLeft  = Pointf(self._image.get_rect().bottomleft)  + (centerPoint - (Pointf(self.size) / 2))    
            # topRight    = Pointf(self._image.get_rect().topright)    + (centerPoint - (Pointf(self.size) / 2))
            # topLeft     = Pointf(self._image.get_rect().topleft)     + (centerPoint - (Pointf(self.size) / 2))

            # tr = rotatePointf(topRight,    -self.rotation, centerPoint)
            # tl = rotatePointf(topLeft,     -self.rotation, centerPoint)
            br = rotatePoint(bottomRight, -self.rotation, centerPoint)
            bl = rotatePoint(bottomLeft,  -self.rotation, centerPoint)

            Lleg = bl
            Rleg = br

            closestLlegPoint = findClosestXPoint(Lleg, gp, offsetIndex=offset.x)
            closestRlegPoint = findClosestXPoint(Rleg, gp, offsetIndex=offset.x)

            LlegInContact = closestLlegPoint.y <= Lleg.y
            RlegInContact = closestRlegPoint.y <= Rleg.y

            # if closestLlegPoint.y > Lleg.y:
            #     Lleg.y = closestLlegPoint
            # if closestRlegPoint.y > Rleg.y:
            #     Rleg.y = closestRlegPoint

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
                self.momentum['vert'] += gravity / GRAVITY_SENSITIVITY


            #* Check if only the right leg is in contact with the ground
            if RlegInContact and not LlegInContact:
                self.rotation += abs(self.momentum['horz'] / gravity + ROTATION_SENSITIVITY) + abs(self.momentum['vert'] / gravity + ROTATION_SENSITIVITY)

            #* Check if only the left leg is in contact with the ground
            if LlegInContact and not RlegInContact:
                self.rotation -= abs(self.momentum['horz'] / gravity + ROTATION_SENSITIVITY) + abs(self.momentum['vert'] / gravity + ROTATION_SENSITIVITY)
                
            self.image = pygame.transform.rotate(self._image, self.rotation)

            # pygame.draw.circle(surface, [255, 0, 0], .data(), 5)

            if self.fuel < 0:
                self.fuel = 0
            
            # When the lander is going fast, the fire gets out of place
            centerPoint += Pointf(self.momentum['horz'], self.momentum['vert']) / MOMENTUM_FIRE_ADJUST

            #* Apply thrusters and display fire
            if self.fuel:
                if self.thrusters['bottom']:
                    # print((LANDER_THRUST / self.mass) * math.cos(math.radians(self.rotation)))
                    self.momentum['vert'] -= (LANDER_THRUST / self.mass) * math.cos(math.radians(self.rotation))
                    self.momentum['horz'] -= (LANDER_THRUST / self.mass) * math.sin(math.radians(self.rotation))
                    self.fuel -= LANDER_THRUST * THRUSTER_FUEL_USAGE_MULTIPLIER

                    self.fire, where = rotateSurface(self._fire, -self.rotation, centerPoint.data(), pygame.math.Vector2(random.randint(-2, 2), 51))
                    surface.blit(self.fire, where)

                if self.thrusters['left']:
                    self.momentum['vert'] -= (LANDER_SIDE_THRUST / self.mass) * math.sin(math.radians(self.rotation))
                    self.momentum['horz'] -= (LANDER_SIDE_THRUST / self.mass) * math.cos(math.radians(self.rotation))
                    self.fuel -= LANDER_SIDE_THRUST * THRUSTER_FUEL_USAGE_MULTIPLIER

                    self.fireRight, where = rotateSurface(self._fireRight, -self.rotation, centerPoint.data(), pygame.math.Vector2(40, random.randint(-1, 1)))
                    surface.blit(self.fireRight, where)

                if self.thrusters['right']:
                    self.momentum['vert'] += (LANDER_SIDE_THRUST / self.mass) * math.sin(math.radians(self.rotation))
                    self.momentum['horz'] += (LANDER_SIDE_THRUST / self.mass) * math.cos(math.radians(self.rotation))
                    self.fuel -= LANDER_SIDE_THRUST * THRUSTER_FUEL_USAGE_MULTIPLIER

                    self.fireLeft, where = rotateSurface(self._fireLeft, -self.rotation, centerPoint.data(), pygame.math.Vector2(-40, random.randint(-1, 1)))
                    surface.blit(self.fireLeft, where)
                    

            # print(f'vertical momentum: {self.momentum["vert"]}\t horizontal momentum: {self.momentum["horz"]}')
            self.loc.x += self.momentum['horz'] / MOMENTUM_SENSITIVITY
            self.loc.y += self.momentum['vert'] / MOMENTUM_SENSITIVITY

            surface.blit(self.image, (self.loc - (Pointf(self.size) / 2) + offset).data())
    

    def rotate(self, positive):
        self.rotation += (BASE_ROTATION_SPEED * (1 if positive else -1)) / self.mass


    def reset(self, loc = None):
        if loc is not None:
            self.loc = loc
        self.momentum['vert'] = 0
        self.momentum['horz'] = 0
        self.exploded = False
        self.fuel = LANDER_FUEL
        self.rotation = 0


    def refuel(self, amount = LANDER_FUEL):
        self.fuel = amount

    
    def getRect(self, *params, offset = Pointf(0, 0)):
        return self.image.get_rect(center=(self.loc + offset).datai(), *params)


    def explode(self, surface, initial=False, offset = Pointf(0, 0)):
        if not self.exploded or initial:
            self.exploded = True
            surface.blit(self.explosion0, (self.loc + offset - self.size + 12).data())
        else:
            surface.blit(random.choice([self.explosion1, self.explosion2]), (self.loc + offset - self.size + 12).data())
