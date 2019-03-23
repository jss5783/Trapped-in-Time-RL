'''
---CHANGELOG---
2019/03/22		(JSS5783)
				Map code implemented. Moving is no longer just painting characters onto the console.
				Player can start anywhere in map. Player can no longer go out of map bounds.
				Added basic time-travel tests.
				Added basic mouse-over and left-click-handling.

2019/03/17		(JSS5783)
				Created main.py.
 				Implemented basic movement/quitting.
 				
 ---LICENSES--- TODO: move into LICENSES.txt once TiTRL's license is decided
Python 3 (https://docs.python.org/3/license.html): PSF license
tcod (https://pypi.org/project/tcod/): Simplified BSD License
terminal16x16_gs_ro.png	(https://github.com/libtcod/python-tcod/tree/master/fonts)/libtcod) license: public domain
Starting code based on Jotaf's roguelike tutorial
	(http://www.roguebasin.com/index.php?title=Talk:Complete_Roguelike_Tutorial,_using_python%2Blibtcod)
		I've been thinking more about this, and I think I will just leave it in the Public Domain. Opinions? Jotaf (talk) 03:37, 17 December 2012 (CET)  
'''

#imports
import tcod
# from InputListener import *
from src.Map import *
from src.Tile import *
from src.constants import *

#declaration and initialization
map1 = Map(MAP_WIDTH, MAP_HEIGHT, "../resources/map.txt")

#setting up console: set font, create main console, set FPS cap
tcod.console_set_custom_font(FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)
console = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title="Trapped in Time RL", fullscreen=False)
tcod.sys_set_fps(FPS_CAP)	#only if real-time, but keeping before input-blocking is added

#stores key inputs
key = tcod.Key()
mouse = tcod.Mouse()
# event = tcod.event()

'''
handle_keys()
Handles player input.
Arrow keys for movement
'''
def handle_keys(key, mouse, inMap):
# def handle_keys(key, mouse, in):
# 	global intPlayerX, intPlayerY
# 	user_input = tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS| tcod.EVENT_MOUSE, key, mouse)

	if key.vk == tcod.KEY_UP:
# 		print(inMap.alstObject[0][0][0].append("?")
# 		if not inMap.isEmptyTile(intPlayerX, intPlayerY):
# 			inMap.alstObject[intPlayerX][intPlayerY].pop(inMap.top(intPlayerX,intPlayerY))
# 		inMap.alstObject[intPlayerX][intPlayerY - 1].append("@")
# 		intPlayerY -= 1
		if ((map1.intPlayerY - 1) >= 0):
			map1.updatePlayerPosition(map1.intPlayerX, map1.intPlayerY - 1)
	elif key.vk == tcod.KEY_DOWN:
# 		if not inMap.isEmptyTile(intPlayerX, intPlayerY):
# 			inMap.alstObject[intPlayerX][intPlayerY].pop(inMap.top(intPlayerX,intPlayerY))
# 		inMap.alstObject[intPlayerX][intPlayerY + 1].append("@")
# 		intPlayerY += 1
		if ((map1.intPlayerY + 1) < MAP_HEIGHT):
			map1.updatePlayerPosition(map1.intPlayerX, map1.intPlayerY + 1)
	elif key.vk == tcod.KEY_LEFT:
# 		if not inMap.isEmptyTile(map1.intPlayerX, map1.intPlayerY):
# 			inMap.alstObject[intPlayerX][intPlayerY].pop(inMap.top(intPlayerX,intPlayerY))
# 		inMap.alstObject[intPlayerX - 1][intPlayerY].append("@")
# 		intPlayerX -= 1
		if ((map1.intPlayerX - 1) >= 0):
			map1.updatePlayerPosition(map1.intPlayerX - 1, map1.intPlayerY)
	elif key.vk == tcod.KEY_RIGHT:
# 		if not inMap.isEmptyTile(intPlayerX, intPlayerY):
# 			inMap.alstObject[intPlayerX][intPlayerY].pop(inMap.top(intPlayerX,intPlayerY))
# 		inMap.alstObject[intPlayerX + 1][intPlayerY].append("@")
# 		intPlayerX += 1
		if ((map1.intPlayerX + 1) < MAP_WIDTH):
			map1.updatePlayerPosition(map1.intPlayerX + 1, map1.intPlayerY)
	elif key.vk == tcod.KEY_SPACE:	#TODO: time travel; checks for collision.
		bIsSafe = True
		bIsBlocked = False
		for y in range(map1.intPlayerY - 1, map1.intPlayerY + 2):
			for x in range(map1.intPlayerX - 1, map1.intPlayerX + 2):
				print(map1.alstObject[x][y][map1.top(x, y)] )
				if (map1.alstObject[x][y][map1.top(x, y)] != "." and map1.alstObject[x][y][map1.top(x, y)] != "@"):
					bIsSafe = False
				if (map1.alstObject[map1.intPlayerX][map1.intPlayerY][map1.top(map1.intPlayerX, map1.intPlayerY)] != "." and map1.alstObject[map1.intPlayerX][map1.intPlayerY][map1.top(map1.intPlayerX, map1.intPlayerY)] != "@"):
					bIsBlocked = True
		print("[DEBUG] bIsSafe:", bIsSafe, "| bIsBlocked:", bIsBlocked)
	elif key.vk == tcod.KEY_ENTER and key.lalt:	#toggle fullscreen
		tcod.console_set_fullscreen(not tcod.console_is_fullscreen() )
	elif key.vk == tcod.KEY_ESCAPE:	#exit game
		return "code:EXIT"

	#mouse-handling
	if mouse.lbutton_pressed == True:
		print("[DEBUG] Left-clicked at ", mouse.cx, ",", mouse.cy)
	if (mouse.cx >= 0 and mouse.cx < MAP_WIDTH) and (mouse.cy >= 0 and mouse.cy < MAP_HEIGHT):
		return "code:MOUSE"
#END handle_keys()


'''
main loop
'''
while not tcod.console_is_window_closed():
	tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
	
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			tcod.console_put_char_ex(console, x, y, map1.alstObject[x][y][map1.top(x, y)], tcod.black, tcod.white)
	tcod.console_flush()
# 	tcod.console_blit(console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	
	strCode = handle_keys(key, mouse, map1)
# 	bTest = handle_event(mouse)
	if (strCode == "code:MOUSE"):
		tcod.console_set_default_foreground(console, tcod.white)
		tcod.console_print_ex(console, 0, MAP_HEIGHT, tcod.BKGND_NONE, tcod.LEFT, "(" + str(mouse.cx) + "," + str(mouse.cy) + "): " + map1.alstObject[mouse.cx][mouse.cy][map1.top(mouse.cx, mouse.cy)] + "   ")
# 		tcod.console_flush()
	elif (strCode == "code:EXIT"):
		break


	
# if __name__ == '__main__':
# 	main()