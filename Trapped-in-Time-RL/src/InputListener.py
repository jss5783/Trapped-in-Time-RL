'''
---CHANGELOG---
2019/04/16		(Bryan)
				Added get "g" input handler

2019/04/10:		(JSS5783)
				Moved tile-reporting code into Map.printTileContents().
				[BUGFIX] Clicking outside of the map no longer crashes the game.

2019/04/09:		(JSS5783)
				Moved Map-checking code into Map.py.
				Added debug right-click to see what's in second timeline.

2019/04/05:		(JSS5783)
				Created InputListener.py.
				Migrated control code from main.py.
'''

import tcod
from src.constants import *
from src.Map import *
from tcod import event


class InputListener:
	def __init__(self):
		print("[DEBUG] Created ", type(self) )
		

	def handle_keys(self, key, mouse, inMap):
		'''
		Handles player input.
		Arrow keys for movement.
		'''
	# 	user_input = tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS| tcod.EVENT_MOUSE, key, mouse)
	
		if key.vk == tcod.KEY_UP:		#move up
			inMap.updatePlayerPosition(inMap.getPlayerX(), inMap.getPlayerY() - 1)
			
		elif key.vk == tcod.KEY_DOWN:	#move down
			inMap.updatePlayerPosition(inMap.getPlayerX(), inMap.getPlayerY() + 1)
			
		elif key.vk == tcod.KEY_LEFT:	#move left
			inMap.updatePlayerPosition(inMap.getPlayerX() - 1, inMap.getPlayerY() )
			
		elif key.vk == tcod.KEY_RIGHT:	#move right
			inMap.updatePlayerPosition(inMap.getPlayerX() + 1, inMap.getPlayerY() )
		
		if key.text == "g": 
			for item in ITEMS:
				if item.x == inMap.getPlayerX() and item.y == inMap.getPlayerY():
										
					myPlayer = inMap.getTopEntity(item.x, item.y)
											
					if item.strName == "Fisto Kit":
						getFistoKit(item, myPlayer)
					elif item.strName == "Shield":
						getSheild(item, myPlayer)
					elif item.strName == "Blaster":
						getBlaster(item)
								
					print(myPlayer.hp, myPlayer.damage)
					print(INVENTORY)
					break
				
			else:
				print("nothing here")
# 				print(inMap.getPlayerX, item.x)
# 				print(inMap.getPlayerY, item.y)
			
		elif key.vk == tcod.KEY_SPACE:	#TODO real version: time travel without assuming only 2 timelines.
			if DEBUG_MODE: print("[DEBUG] Time-traveling attempt from timeline", inMap.getPlayerZ() )
			if (inMap.getPlayerZ() == 0):
				inMap.updatePlayerPosition(inMap.getPlayerX(), inMap.getPlayerY(), inMap.getPlayerZ() + 1)
			else:
				inMap.updatePlayerPosition(inMap.getPlayerX(), inMap.getPlayerY(), inMap.getPlayerZ() - 1)
			
		elif key.vk == tcod.KEY_ENTER and key.lalt:	#toggle fullscreen
			tcod.console_set_fullscreen(not tcod.console_is_fullscreen() )
			
		elif key.vk == tcod.KEY_ESCAPE:	#exit game
			return "code:EXIT"
		
		
		#mouse-handling; maybe move into separate function if new TCoD version permits that.
		#TODO: only return information if in FoV (skip memory FoV for now)
		if mouse.lbutton_pressed == True:	#left-click
			if (mouse.cx >= 0 and mouse.cx < MAP_WIDTH) and (mouse.cy >= 0 and mouse.cy < MAP_HEIGHT):
				inMap.printTileContents(mouse.cx, mouse.cy, 0)
		if mouse.rbutton_pressed == True:	#right-click
			if (mouse.cx >= 0 and mouse.cx < MAP_WIDTH) and (mouse.cy >= 0 and mouse.cy < MAP_HEIGHT):
				inMap.printTileContents(mouse.cx, mouse.cy, 1)
		#if mouse.rbutton_pressed == True:
			print("right clicked")
			for item in INVENTORY:
				print(item.strName)
				if item.strName == "Blaster":
					print("Blaster")
					for enemy in ENEMIES:
						if enemy.x == mouse.cx and enemy.y == mouse.cy:
							useBlaster(enemy, item)
							print(enemy.hp)
							print(item.ammo)
		
	#END handle_keys(self, key, mouse, inMap)