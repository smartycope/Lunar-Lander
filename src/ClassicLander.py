from Lander import *


class ClassicLander(Lander):
    def __init__(self, startPoint = Pointf(0, 0)):
        super().__init__('ClassicLander/', startPoint)
        self._mass = 100
        self.legStrength = 10
        self.mainThrust = 50
        self.rightThrust = 10
        self.leftThrust = 10
        self.fuelUsage = THRUSTER_FUEL_USAGE_MULTIPLIER
        self.rotationSpeed = BASE_ROTATION_SPEED
        self._fuel = 1000

        