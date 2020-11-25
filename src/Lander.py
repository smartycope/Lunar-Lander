from GlobalFuncs import *
from Config import *
import os, math, random
from copy import deepcopy
import numpy as np

#* To create a new lander:
    # Creating a new lander is pretty simple. You just need to create the class and have 
    # it inherit from Lander, then define init(). From there, just define the following data members:
    # dir:
    #   The directory to get the lander's assets from
    #   Default Value: class name + '/'
    #   Units: filepath
    # _mass: 
    #   How much mass the lander has
    #   Default Value: 100
    #   Units: kilograms
    # legStrength:
    #   How fast you can go before the lander explodes when you hit the ground
    #   Default Value: 10
    #   Units: m/s
    # mainThrust:
    #   How much thrust the bottom thruster can provide
    #   Default Value: 50
    #   Units: kilonewtons (1 (m/s/s)/kg)
    # rightThrust:
    #   How much thrust the right thruster can provide
    #   Default Value: 10
    #   Units: kilonewtons
    # leftThrust:
    #   How much thrust the right thruster can provide
    #   Default Value: 10
    #   Units: kilonewtons
    # specificImpulse:
    #   How efficent the Lander is at converting fuel to momentum
    #   Default Value: THRUSTERfuelCapacity_USAGE_MULTIPLIER
    #   Units: Arbitrary
    # rotationSpeed:
    #   How fast the lander can rotate
    #   Default Value: BASE_ROTATION_SPEED
    #   Units: Arbitrary
    # fuelCapacity:
    #   How much fuel the lander can hold
    #   Default Value: 1000
    #   Units: Arbitrary
    #
    # No other methods are required


class Lander:
    def __init__(self, startPoint=Pointf(0, 0), saveFile=None):
        self.init()
        if saveFile is not None:
            with open(saveFile, 'r') as file:
                landerUpgrades = json.load(file)[self.name]
                
            self.mainThrust = landerUpgrades['thrust']
            self.leftThrust = landerUpgrades['sideThrust']
            self.rightThrust = landerUpgrades['sideThrust']
            self.fuelCapacity = landerUpgrades['fuelCapacity']
            self.legStrength = landerUpgrades['legStrength']
            self._mass = landerUpgrades['weight']
            self.specificImpulse = landerUpgrades['specificImpulse']
            self.rotationSpeed = landerUpgrades['specificImpulse'] + BASE_ROTATION_SPEED


        self.loc = startPoint

        self.mainThrust *= 1000
        self.rightThrust *= 1000
        self.leftThrust *= 1000

        self.dir = 'landers/' + self.name + '/'

        self.loadAssets()

        # self.mass = self._mass

        self.size = self.image.get_size()

        self.fuel = 0
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


    def init(self):
        raise NotImplementedError


    def loadAsset(self, name, extension='png'):
        return loadAsset(self.dir, name, extension)


    def loadAssets(self):
        # raise NotImplementedError
        self._image =       self.loadAsset('lander')
        self._fire =        self.loadAsset('fire1')
        self._fireLeft =    self.loadAsset('fireLeft')
        self._fireRight =   self.loadAsset('fireRight')
        self.image =        self._image
        self.fire =         self._fire
        self.fireLeft =     self._fireLeft
        self.fireRight =    self._fireRight
        self.explosion0 =   self.loadAsset('explosion3')
        self.explosion1 =   self.loadAsset('explosion2')
        self.explosion2 =   self.loadAsset('explosion1')


    def update(self, gravity, groundPoints, surface, offset = Pointf(0, 0)):
        if not self.exploded:
            self.mass = self._mass + (self.fuel * FUEL_WEIGHT)
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
                if self.momentum['vert'] > self.legStrength or self.momentum['horz'] > self.legStrength * EXTRA_LANDER_LEG_SIDE_STRENGTH:
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
            centerPoint += Pointf(self.momentum['horz'], self.momentum['vert'])

            #* Apply thrusters and display fire
            if self.fuel:
                if self.thrusters['bottom']:
                    # print((LANDER_THRUST / self.mass) * math.cos(math.radians(self.rotation)))
                    self.momentum['vert'] -= ((self.mainThrust * FUEL_THRUST) / self.mass) * math.cos(math.radians(self.rotation))
                    self.momentum['horz'] -= ((self.mainThrust * FUEL_THRUST) / self.mass) * math.sin(math.radians(self.rotation))
                    self.fuel -= (self.mainThrust / 1000) / self.specificImpulse

                    self.fire, where = rotateSurface(self._fire, -self.rotation, centerPoint.data(), pygame.math.Vector2(random.randint(-2, 2), 51))
                    surface.blit(self.fire, where)

                if self.thrusters['left']:
                    self.momentum['vert'] -= ((self.rightThrust * FUEL_THRUST) / self.mass) * math.sin(math.radians(self.rotation))
                    self.momentum['horz'] -= ((self.rightThrust * FUEL_THRUST) / self.mass) * math.cos(math.radians(self.rotation))
                    self.fuel -= (self.rightThrust / 1000) / self.specificImpulse

                    self.fireRight, where = rotateSurface(self._fireRight, -self.rotation, centerPoint.data(), pygame.math.Vector2(40, random.randint(-1, 1)))
                    surface.blit(self.fireRight, where)

                if self.thrusters['right']:
                    self.momentum['vert'] += ((self.leftThrust * FUEL_THRUST) / self.mass) * math.sin(math.radians(self.rotation))
                    self.momentum['horz'] += ((self.leftThrust * FUEL_THRUST) / self.mass) * math.cos(math.radians(self.rotation))
                    self.fuel -= (self.leftThrust / 1000) / self.specificImpulse

                    self.fireLeft, where = rotateSurface(self._fireLeft, -self.rotation, centerPoint.data(), pygame.math.Vector2(-40, random.randint(-1, 1)))
                    surface.blit(self.fireLeft, where)
                    

            # print(f'vertical momentum: {round(self.momentum["vert"], 3)}\t horizontal momentum: {round(self.momentum["horz"], 3)}')
            self.loc.x += self.momentum['horz'] / MOMENTUM_SENSITIVITY
            self.loc.y += self.momentum['vert'] / MOMENTUM_SENSITIVITY

            surface.blit(self.image, (self.loc - (Pointf(self.size) / 2) + offset).data())
    

    def rotate(self, positive):
        self.rotation += (self.rotationSpeed * (1 if positive else -1)) / self.mass


    def reset(self, loc = None):
        if loc is not None:
            self.loc = loc
        self.momentum['vert'] = 0
        self.momentum['horz'] = 0
        self.exploded = False
        self.fuel = self.fuelCapacity
        self.rotation = 0


    def refuel(self, amount=None):
        if amount is None:
            amount = self.fuelCapacity
        self.fuel = amount

    
    def getRect(self, *params, offset = Pointf(0, 0)):
        return self.image.get_rect(center=(self.loc + offset).datai(), *params)


    def getSpeed(self):
        return math.sqrt((self.momentum['vert'] ** 2) + (self.momentum['horz'] ** 2))


    def serialize(self):
        return [self.mainThrust, self.leftThrust, self.rightThrust, self.dir, self.fuelCapacity, self.legStrength, self._mass, self.specificImpulse, self.fuelCapacity]


    def deserialize(self, data):
        self.mainThrust = data[0]
        self.leftThrust = data[1]
        self.rightThrust = data[2]
        self.dir = data[3]
        self.fuelCapacity = data[4]
        self.legStrength = data[5]
        self._mass = data[6]
        self.specificImpulse = data[7]
        self.fuelCapacity = data[8]


    def explode(self, surface, initial=False, offset = Pointf(0, 0)):
        if not self.exploded or initial:
            self.exploded = True
            surface.blit(self.explosion0, (self.loc + offset - self.size + 12).data())
        else:
            surface.blit(random.choice([self.explosion1, self.explosion2]), (self.loc + offset - self.size + 12).data())

