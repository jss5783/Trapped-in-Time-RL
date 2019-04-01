'''
---CHANGELOG---
2019/03/31		(JSS5783)
				Adjusted some colors.

2019/03/27		(JSS5783)
				Added colors. Added STATUS/MESSAGE.

2019/03/22		(JSS5783)
				constants.py created. Constants moved.
'''

import tcod

#---CONSTANTS---
SCREEN_WIDTH = 80		#for entire game; screen (game window) has multiple viewports (consoles)
SCREEN_HEIGHT = 50
MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT - 5
STATUS_WIDTH = 30
STATUS_HEIGHT = SCREEN_HEIGHT - MAP_HEIGHT
MESSAGE_WIDTH = SCREEN_WIDTH - STATUS_WIDTH
MESSAGE_HEIGHT = STATUS_HEIGHT
FPS_CAP = 20
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
