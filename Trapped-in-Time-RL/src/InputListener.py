'''
---CHANGELOG---
2019/04/20:		(JSS5783)
				Updated Map code.
				Added debug right-click to move a non-Player Entity down 1 tile.
				
2019/04/19		(Bryan)
				updated input handlers to return "endTurn" for turn order tracking
				Modified "g" function to work with Item get functions

2019/04/19:		(JSS5783)
				Modified "get item" code.
				[space] -> [t] for time-travel.

2019/04/17:		(JSS5783)
				Added message log tests to mouse controls.

2019/04/16		(Bryan)
				Added get "g" input handler

2019/04/15:		(JSS5783)
				Added entity add/remove tests to mouse controls.

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
from src.item_functions import *
from src.Entity import *
from src.item_functions import *
from src.Status import *
from src import item_functions


class InputListener:
	def __init__(self):
		print("[DEBUG] Created ", type(self) )
		

	def handle_keys(self, key, mouse, inMap, inLog, inStatus):
		'''
		Handles player input.
		Arrow keys for movement.
		'''
	# 	user_input = tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS| tcod.EVENT_MOUSE, key, mouse)
	
		if key.vk == tcod.KEY_UP:		#move up
			inMap.updatePlayerPosition(inLog, inStatus, inMap.getPlayerX(), inMap.getPlayerY() - 1)
			return "endTurn"
			
		elif key.vk == tcod.KEY_DOWN:	#move down
			inMap.updatePlayerPosition(inLog, inStatus, inMap.getPlayerX(), inMap.getPlayerY() + 1)
			return "endTurn"
			
		elif key.vk == tcod.KEY_LEFT:	#move left
			inMap.updatePlayerPosition(inLog, inStatus, inMap.getPlayerX() - 1, inMap.getPlayerY() )
			return "endTurn"
			
		elif key.vk == tcod.KEY_RIGHT:	#move right
			inMap.updatePlayerPosition(inLog, inStatus, inMap.getPlayerX() + 1, inMap.getPlayerY() )
			return "endTurn"
	
		if key.text == "g":		#[g]et item
# 			item = inMap.getUnderPlayer()				
# 			print(item)
# 			print(inMap.aLstEntities)							
# 			myPlayer = inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY() )
			
		
			if inMap.getEntityIndexAt(FistoKit, inMap.getPlayerX(), inMap.getPlayerY()) != -1:
				print("Found: FistoKit")
# 				getFistoKit(item, myPlayer, inMap)
				getFistoKit(inMap, inLog, inStatus)
			elif inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()) != -1:
# 				inMap.getEntityAt(inMap.getEntityIndexAt(FistoKit, inMap.getPlayerX, inMap.getPlayerY), inMap.getPlayerX, inMap.getPlayerY)
# 				getShield(inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY()), inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY()) )
# 				getShield(item, myPlayer, inMap)
				getShield(inMap, inLog, inStatus)
			elif inMap.getEntityIndexAt(Blaster, inMap.getPlayerX(), inMap.getPlayerY()) != -1:
# 				getBlaster(item, inMap)
				getBlaster(inMap, inLog, inStatus)
			else:
				print("nothing here")
# 			print(myPlayer.hp, myPlayer.damage)
			print(INVENTORY)
			return "endTurn"
# 			for item in ITEMS:
# 				if item.x == inMap.getPlayerX() and item.y == inMap.getPlayerY():
# 						
# 					myPlayer = inMap.getTopEntity(item.x, item.y)
# 												
# 					if item.strName == "Fisto Kit":
# 						getFistoKit(item, myPlayer)
# # 					elif item.strName == "Shield":
# # 						getSheild(item, myPlayer)
# 					elif item.strName == "Blaster":
# 						getBlaster(item)
# 								
# 					print(myPlayer.hp, myPlayer.damage)
# 					print(INVENTORY)
# 					break
# 				
# 				else:
# 					print("nothing here")
# 					print(inMap.getPlayerX, item.x)
# 					print(inMap.getPlayerY, item.y)
# 		elif key.vk == tcod.KEY_SPACE:	#TODO real version: time travel without assuming only 2 timelines.
		elif key.text == "t": 
			if DEBUG_MODE: print("[DEBUG] Time-traveling attempt from timeline", inMap.getPlayerZ() )
			if (inMap.getPlayerZ() == 0):
				inMap.updatePlayerPosition(inLog, inStatus, inMap.getPlayerX(), inMap.getPlayerY(), inMap.getPlayerZ() + 1)
				inStatus.setTimeline(inMap.getPlayerZ() )
				return "endTurn"
			else:
				inMap.updatePlayerPosition(inLog, inStatus, inMap.getPlayerX(), inMap.getPlayerY(), inMap.getPlayerZ() - 1)
				inStatus.setTimeline(inMap.getPlayerZ() )
				return "endTurn"
			
		elif key.vk == tcod.KEY_ENTER and key.lalt:	#toggle fullscreen
			tcod.console_set_fullscreen(not tcod.console_is_fullscreen() )
			
		elif key.vk == tcod.KEY_ESCAPE:	#exit game
			return "code:EXIT"
		
		
		#mouse-handling; maybe move into separate function if new TCoD version permits that.
		#TODO: only return information if in FoV (skip memory FoV for now)
		if mouse.lbutton_pressed == True:	#left-click
			if (mouse.cx >= 0 and mouse.cx < MAP_WIDTH) and (mouse.cy >= 0 and mouse.cy < MAP_HEIGHT):
				inMap.printTileContents(mouse.cx, mouse.cy, 0)
				inMap.addEntityAt(Wall(mouse.cx, mouse.cy, 0), mouse.cx, mouse.cy)
# 				inLog.addMessage("The quick brown fox jumped over the lazy dog.")
		if mouse.rbutton_pressed == True:	#right-click
			if (mouse.cx >= 0 and mouse.cx < MAP_WIDTH) and (mouse.cy >= 0 and mouse.cy < MAP_HEIGHT):
# 				inMap.printTileContents(mouse.cx, mouse.cy, 1)
				inMap.printTileContents(mouse.cx, mouse.cy)
# 				inMap.getEntityIndexAt(Wall(), mouse.cx, mouse.cy)
# 				inMap.removeEntityAt(HealthConsumable(), mouse.cx, mouse.cy)
# 				inMap.removeEntityAtIndex(1, mouse.cx, mouse.cy)
# 				inMap.moveEntityTo(inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY(), inMap.getPlayerZ() - 1)
# 				inMap.moveEntityTo(inMap.getTopEntity(mouse.cx, mouse.cy), inLog, mouse.cx, mouse.cy + 1)
			for item in INVENTORY:
				print(item.strName)
				if item.strName == "Blaster":
					print("Blaster")
					for enemy in ENEMIES:
						if enemy.x == mouse.cx and enemy.y == mouse.cy:
							useBlaster(inMap, inLog, inStatus, mouse.cx, mouse.cy)
							print(enemy.hp)
							print(item.currentAmmo)
					return "endTurn"
				else:
					print(inMap.getTopEntity(mouse.cx, mouse.cy))
				
	#END handle_keys(self, key, mouse, inMap)