'''
---CHANGELOG---
2019/03/17		(JSS5783)
				Created main.py.
 				Implemented basic movement/quitting.			
 				
 ---LICENSES--- TODO: move into LICENSES.txt once TiTRL's license is decided
Python 3 (https://docs.python.org/3/license.html): PSF license
tcod (https://pypi.org/project/tcod/): Simplified BSD License
terminal16x16_gs_ro.png	(https://github.com/libtcod/python-tcod/tree/master/fonts)/libtcod license: public domain
Starting code based on Jotaf's roguelike tutorial
	(http://www.roguebasin.com/index.php?title=Talk:Complete_Roguelike_Tutorial,_using_python%2Blibtcod)
		I've been thinking more about this, and I think I will just leave it in the Public Domain. Opinions? Jotaf (talk) 03:37, 17 December 2012 (CET)  
'''

#imports
import tcod

#declaration and initialization
#---CONSTANTS---
SCREEN_WIDTH = 80		#for entire game; screen (game window) has multiple viewports (consoles)
SCREEN_HEIGHT = 50
FPS_CAP = 20
FONT = '../resources/terminal16x16_gs_ro.png'	#license: public domain, as according to https://github.com/libtcod/python-tcod/tree/master/fonts/libtcod

#setting up console: set font, create main console, set FPS cap
tcod.console_set_custom_font(FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)
console = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title="Trapped in Time RL", fullscreen=False)
tcod.sys_set_fps(FPS_CAP)	#only if real-time, but keeping before input-blocking is added

#stores key inputs
key = tcod.Key()
mouse = tcod.Mouse()

#initial player character position
intPlayerX = SCREEN_WIDTH // 2
intPlayerY = SCREEN_HEIGHT // 2


'''
handle_keys()
Handles player input.
Arrow keys for movement
'''
def handle_keys():
	global intPlayerX, intPlayerY

# 	user_input = tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS| tcod.EVENT_MOUSE, key, mouse)
	tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
	
	if key.vk == tcod.KEY_UP:
		intPlayerY -= 1
	elif key.vk == tcod.KEY_DOWN:
		intPlayerY += 1
	elif key.vk == tcod.KEY_LEFT:
		intPlayerX -= 1
	elif key.vk == tcod.KEY_RIGHT:
		intPlayerX += 1
	elif key.vk == tcod.KEY_ENTER and key.lalt:	#toggle fullscreen
		tcod.console_set_fullscreen(not tcod.console_is_fullscreen() )
	elif key.vk == tcod.KEY_ESCAPE:	#exit game
		return True
#END handle_keys()


'''
main loop
'''
while not tcod.console_is_window_closed():
	
	tcod.console_put_char_ex(console, intPlayerX, intPlayerY, '@', tcod.black, tcod.white)
	tcod.console_flush()
	tcod.console_put_char_ex(console, intPlayerX, intPlayerY, '.', tcod.black, tcod.black)
	
	bExitGame = handle_keys()
	
	if bExitGame:
		break


	
# if __name__ == '__main__':
# 	main()