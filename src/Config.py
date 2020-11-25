from os.path import dirname, join; 
DIR = join(dirname(__file__), '..')
DATA = join(DIR, 'data')
GUI_THEME_FILE = DIR + 'data/other/myTheme.json'

# One Newton is the force needed to accelerate one kilogram of mass at the rate of one meter per second squared

import jstyleson as json

with open(DATA + "/config.jsonc", 'r') as f:
    config = json.load(f)


#* Game.py
# The delay between a key being pressed, and it pressing itself really fast
# Units: milliseconds
KEY_REPEAT_DELAY = config['KEY_REPEAT_DELAY']
# How fast that key should press itself
# Units: milliseconds
KEY_REPEAT_INTERVAL = config['KEY_REPEAT_INTERVAL']
# Units: Frames per second
FPS = config['FPS']
# Whether the game should start in full screen or not
START_FULLSCREEN = config['START_FULLSCREEN']
# Which display to start the program in, if there are multiple monitors - doesn't currently work, I don't know why.
# Units: int
START_DISPLAY = config['START_DISPLAY']
# Whether to use vsync - does not work until pygame 2.0.0 or greater
VSYNC = config['VSYNC']


# 1 m/s = config[''] pixels / 60 frames
PIXELS_PER_METER = config['PIXELS_PER_METER']


#* PickPlanet.py
# Defines how fast the planet animations rotate
PLANET_SECONDS_PER_ROTATION = config['PLANET_SECONDS_PER_ROTATION']


#* Lander.py
# Defines how fast the lander decelarates when in contact with the ground
# Units: Arbitrary
GROUND_FRICTION = config['GROUND_FRICTION']
# How much stronger the lander legs are against horizontal momentum vs vertical momentum
# Units: m/s
EXTRA_LANDER_LEG_SIDE_STRENGTH = config['EXTRA_LANDER_LEG_SIDE_STRENGTH']
# Defines how sensitive landers are to momentum is
# Units: Inverted Arbitrary
MOMENTUM_SENSITIVITY = config['MOMENTUM_SENSITIVITY']
# Defines how sesitive the landers are to rotating
# Units: Arbitrary
ROTATION_SENSITIVITY = config['ROTATION_SENSITIVITY']
# Defines how sensitive landers are to gravity
# Units: Inverted Arbitrary
GRAVITY_SENSITIVITY = config['GRAVITY_SENSITIVITY']
# Defines how much mass fuel has
# Units: kilograms
FUEL_WEIGHT = config['FUEL_WEIGHT']
# Defines how much momentum change fuel will give you
# Units: Newtons
FUEL_THRUST = config['FUEL_THRUST']
# Defines a good default rotation speed (this changes based on how fast key repeat is set to)
# Units: Arbitrary
BASE_ROTATION_SPEED = config['BASE_ROTATION_SPEED']
# Defines how much fuel is used to change 1 m/s
# Units: Inverted km/s (I think it's inverted)
SPECIFIC_IMPULSE = config['SPECIFIC_IMPULSE']


#* Planet.py
# Where the ground starts being drawn at
# Units: pixels from the bottom
GROUND_START_Y = config['GROUND_START_Y']
# How long the lander should explode for
# Units: frames
EXPLODE_TIME = config['EXPLODE_TIME']
# How long after a lander stops exploding to show the death menu
# Units: seconds
DEATH_DELAY_TIME = config['DEATH_DELAY_TIME']
# How far to the right we create another ground point to draw to (I think)
# Units: pixels??
GROUND_X_WIDTH = config['GROUND_X_WIDTH']
# How far from the left or right edges of the window do we start scrolling that direction
# Units: pixels
SCROLL_WIDTH = config['SCROLL_WIDTH']
# How much the grond tends to slope up or down
# I have no idea why this does what it does, or what I was thinking when I made it. It's super touchy though.
# Units: Arbitrary??
SLOPE = config['SLOPE']
# The height of the subjective column that we allow new ground points to be drawn in (i.e. how flat the ground is)
# Units: pixels
FLATTNESS = config['FLATTNESS']
# How far off the ground items float
# Units: pixels
ITEM_FLOAT_HEIGHT = config['ITEM_FLOAT_HEIGHT']

#! Depricated
# How likely a gas can item is to spawn as soon as you scroll
# Units: Inverted chance
# GAS_CAN_SPAWN_CHANCE = config['GAS_CAN_SPAWN_CHANCE']
#! Depricated
# The minimum spread gas can items may have
# Units: pixels
# MIN_GAS_CAN_SPAWN_DIST = config['MIN_GAS_CAN_SPAWN_DIST'] # 1379
#! Depricated
# The maximum spread gas can items may have
# Units: pixels
# MAX_GAS_CAN_SPAWN_DIST = config['MAX_GAS_CAN_SPAWN_DIST']
#! Depricated
# How likely a coin item is to spawn as soon as you scroll
# Units: Inverted chance
# COIN_SPAWN_CHANCE = config['COIN_SPAWN_CHANCE']
#! Depricated
# The minimum spread coin items can have
# Units: pixels
# MIN_COIN_SPAWN_DIST = config['MIN_COIN_SPAWN_DIST']
#! Depricated
# The maximum spread coin items can have
# Units: pixels
# MAX_COIN_SPAWN_DIST = config['MAX_COIN_SPAWN_DIST']

# How many bytecoin coins give you when you collect them
COIN_VALUE = config['COIN_VALUE']

#! Depricated
# How likely a super coin item is to spawn as soon as you scroll
# Units: Inverted chance
# SUPER_COIN_SPAWN_CHANCE = config['SUPER_COIN_SPAWN_CHANCE']
#! Depricated
# The minimum spread super coin items can have
# Units: pixels
# MIN_SUPER_COIN_SPAWN_DIST = config['MIN_SUPER_COIN_SPAWN_DIST']

# How many bytecoin super coins give you when you collect them
SUPER_COIN_VALUE = config['SUPER_COIN_WORTH']

#! Depricated
# Defines how far in one direction we have to go to try to generate another item
# (This solves the problem that when you go in one direction slowly, more items are generated)
# Units: pixels
# ITEM_GENERATE_MORE_IGNORE_AMOUNT = config['ITEM_GENERATE_MORE_IGNORE_AMOUNT']


METERS_PER_SECOND = PIXELS_PER_METER / FPS

UPGRADE_ROUND_PLACES = 3


#* Changing the values to make their units make sense
DEATH_DELAY_TIME *= FPS
SPECIFIC_IMPULSE *= METERS_PER_SECOND
FUEL_THRUST *= METERS_PER_SECOND
GRAVITY_SENSITIVITY *= METERS_PER_SECOND
BASE_ROTATION_SPEED *= KEY_REPEAT_DELAY


#* Some arbitrary enums
SCROLLING_LEFT  = 1
SCROLLING_RIGHT = 2
NOT_SCROLLING   = 0

LEFT = True
RIGHT = False

CENTER_ALIGN = True
LEFT_ALIGN   = False