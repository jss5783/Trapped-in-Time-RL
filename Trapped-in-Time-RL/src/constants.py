'''
---CHANGELOG---
2019/04/10		(JSS5783)
				Non-debug seed now uses system clock for default.

2019/04/06		(JSS5783)
				Added FOV_RADIUS.

2019/04/05		(JSS5783)
				Added DEBUG_MODE to control console output/RNG seed for debugging.

2019/03/31		(JSS5783)
				Adjusted some colors.

2019/03/27		(JSS5783)
				Added colors. Added STATUS/MESSAGE.

2019/03/22		(JSS5783)
				constants.py created. Constants moved.
'''

import tcod, datetime


SCREEN_WIDTH : int = 80		#for entire game; screen (game window) has multiple viewports (consoles)
SCREEN_HEIGHT : int = 50
MAP_WIDTH : int = SCREEN_WIDTH
MAP_HEIGHT : int = SCREEN_HEIGHT - 5
STATUS_WIDTH : int = 30
STATUS_HEIGHT : int = SCREEN_HEIGHT - MAP_HEIGHT
MESSAGE_WIDTH : int = SCREEN_WIDTH - STATUS_WIDTH
MESSAGE_HEIGHT : int = STATUS_HEIGHT
FPS_CAP : int = 20
FONT = '../resources/terminal16x16_gs_ro.png'
WHITE = tcod.Color(250,250,250)
BLACK = tcod.Color(5,5,5)
GRAY_DARK = tcod.Color(100,100,100)
GRAY_LIGHT = tcod.Color(192,192,192)
RED_DARK = tcod.Color(165,50,50)
RED_LIGHT = tcod.Color(245,175,175)
ORANGE_DARK = tcod.Color(165,90,15)
ORANGE_LIGHT = tcod.Color(245,185,105)
GREEN_DARK = tcod.Color(50,165,50)
GREEN_LIGHT = tcod.Color(175,245,175)
BLUE_DARK = tcod.Color(15,100,165)
BLUE_LIGHT = tcod.Color(100,200,245)
MAGENTA_DARK = tcod.Color(165,50,165)
MAGENTA_LIGHT = tcod.Color(245,175,245)
ITEMS = []		#Bryan: Added ITEMS list to store all items in game
INVENTORY = []	#Bryan: Added INVENTORY list to handle items currently held by player
ENEMIES = []  	#Bryan: Added ENEMIES list to store all enemies in game
DEBUG_MODE = False
if DEBUG_MODE:	#TODO: use system datetime for non-debug value
	SEED = 5
else:
	SEED = datetime.datetime.now()
FOV_RADIUS = 5
