'''
---CHANGELOG---
2019/04/09:		(JSS5783)
				Updated code with new Map variables and methods after several (broken, unfinished) dead-ends.
				Moved code into main().

2019/04/05		(JSS5783)
				Split input-handling into InputListener.
				Added debug maps.
				Removed test objects.

2019/03/29		(JSS5783)
				Debug command: click on a tile to print its contents to console.
				Debug: placed test objects for various tests.
				Added message log.

2019/03/22		(JSS5783)
				Map code implemented. Moving is no longer just painting characters onto the console.
				Player can start anywhere in map. Player can no longer go out of map bounds.
				Added basic time-travel tests.
				Added basic mouse-over and left-click-handling.

2019/03/17		(JSS5783)
				Created main.py.
 				Implemented basic movement/quitting.
'''

#imports
import tcod
import tcod.event
# from InputListener import *
from src.Map import *
from src.constants import *
from src.Entity import *
from src.MessageLog import *
from src.InputListener import *
from tcod.libtcodpy import console_set_char_foreground
from tcod import event


# <<<<<<< bryan
# 	if key.vk == tcod.KEY_UP:
# # 		print(inMap.alstObject[0][0][0].append("?")
# # 		if not inMap.isEmptyTile(intPlayerX, intPlayerY):
# # 			inMap.alstObject[intPlayerX][intPlayerY].pop(inMap.top(intPlayerX,intPlayerY))
# # 		inMap.alstObject[intPlayerX][intPlayerY - 1].append("@")
# # 		intPlayerY -= 1
# 		if ((map1.intPlayerY - 1) >= 0):
# 			map1.updatePlayerPosition(map1.intPlayerX, map1.intPlayerY - 1)
# 	elif key.vk == tcod.KEY_DOWN:
# # 		if not inMap.isEmptyTile(intPlayerX, intPlayerY):
# # 			inMap.alstObject[intPlayerX][intPlayerY].pop(inMap.top(intPlayerX,intPlayerY))
# # 		inMap.alstObject[intPlayerX][intPlayerY + 1].append("@")
# # 		intPlayerY += 1
# 		if ((map1.intPlayerY + 1) < MAP_HEIGHT):
# 			map1.updatePlayerPosition(map1.intPlayerX, map1.intPlayerY + 1)
# 	elif key.vk == tcod.KEY_LEFT:
# # 		if not inMap.isEmptyTile(map1.intPlayerX, map1.intPlayerY):
# # 			inMap.alstObject[intPlayerX][intPlayerY].pop(inMap.top(intPlayerX,intPlayerY))
# # 		inMap.alstObject[intPlayerX - 1][intPlayerY].append("@")
# # 		intPlayerX -= 1
# 		if ((map1.intPlayerX - 1) >= 0):
# 			map1.updatePlayerPosition(map1.intPlayerX - 1, map1.intPlayerY)
# 	elif key.vk == tcod.KEY_RIGHT:
# # 		if not inMap.isEmptyTile(intPlayerX, intPlayerY):
# # 			inMap.alstObject[intPlayerX][intPlayerY].pop(inMap.top(intPlayerX,intPlayerY))
# # 		inMap.alstObject[intPlayerX + 1][intPlayerY].append("@")
# # 		intPlayerX += 1
# 		if ((map1.intPlayerX + 1) < MAP_WIDTH):
# 			print(map1.intPlayerX + 1, map1.intPlayerY)
# 			map1.updatePlayerPosition(map1.intPlayerX + 1, map1.intPlayerY)
# 	elif key.vk == tcod.KEY_SPACE:	#TODO: time travel; checks for collision.
# 		bIsSafe = True
# 		bIsBlocked = False
# 		for y in range(map1.intPlayerY - 1, map1.intPlayerY + 2):
# 			for x in range(map1.intPlayerX - 1, map1.intPlayerX + 2):
# 				print(map1.alstObject[x][y][map1.top(x, y)] )
# 				#TODO: if timelines use the same overall layout, add Wall+Gate (open AND closed) to checks. Other timeline: "has Enemy, item, or even Portal?"
# 				if (type(map1.alstObject[x][y][map1.top(x, y)]) != Floor and type(map1.alstObject[x][y][map1.top(x, y)]) != Player):
# 					bIsSafe = False
# 				if (type(map1.alstObject[map1.intPlayerX][map1.intPlayerY][map1.top(map1.intPlayerX, map1.intPlayerY)]) != Floor and type(map1.alstObject[map1.intPlayerX][map1.intPlayerY][map1.top(map1.intPlayerX, map1.intPlayerY)]) != Player):
# 					bIsBlocked = True
# 		print("[DEBUG] bIsSafe:", bIsSafe, "| bIsBlocked:", bIsBlocked)
	
# 	'''
# 	BRYAN: begin code add/change
# 	Uses the 'g' key to pick up an item.  Checks all items in the game to see if 
# 	they have the same position on the map as the player.  If there is an item there
# 	the item is placed into the inventory. Print commands are for testing only and will
# 	eventually be removed.  Still need to remove item and icon from map position.
# 	Had to change elif to if because of syntax error caused by commenting
# 	'''
	
# 	if key.text == "g": 
# 		for item in ITEMS:
# 			if item.x == map1.intPlayerX and item.y == map1.intPlayerY:
# 				INVENTORY.append(item)
# 				print(INVENTORY)
# 				print(item.strName)
# 				if item.strName == "Fisto Kit":
# 					map1.Player.damage = item.damage
# 				elif item.strName == "Shield":
# 					for i in item.charges:
# 						if map1.Player.hp < item.maxcharges:
# 							map1.Player.hp += 1
# 				print(map1.Player.hp, map1Player.damage)
# 				break
				
# 		else:
# 			print("nothing here")
# 			print(map1.intPlayerX, item.x)
# 			print(map1.intPlayerY, item.y)
	
# 	'''
# 	Bryan: end code add/change
# 	'''
# 	if key.vk == tcod.KEY_ENTER and key.lalt:	#toggle fullscreen
# 		tcod.console_set_fullscreen(not tcod.console_is_fullscreen() )
# 	elif key.vk == tcod.KEY_ESCAPE:	#exit game
# 		return "code:EXIT"

# 	#mouse-handling
# 	if mouse.lbutton_pressed == True:
# 		print("[DEBUG] Left-clicked at ", mouse.cx, ",", mouse.cy, "; (" + str(mouse.cx) + "," + str(mouse.cy) + "): " + map1.alstObject[mouse.cx][mouse.cy][map1.top(mouse.cx, mouse.cy)].getName() + "   ")
# 		for i in range(len(map1.alstObject[mouse.cx][mouse.cy] )):
# 			print(map1.alstObject[mouse.cx][mouse.cy][i].getName())
# 	if mouse.rbutton_pressed == True:
# 		print("right clicked")
# 		for item in INVENTORY:
# 			print(item.strName)
# 			if item.strName == "Blaster":
# 				print("Blaster")
# 				for enemy in ENEMIES:
# 					if enemy.x == mouse.cx and enemy.y == mouse.cy:
# 						useBlaster(enemy, item)
# 						print(enemy.hp)
# 						print(item.charges)
# 	if (mouse.cx >= 0 and mouse.cx < MAP_WIDTH) and (mouse.cy >= 0 and mouse.cy < MAP_HEIGHT):
# 		return "code:MOUSE"
# #END handle_keys()


# '''
# main loop
# '''
# #test objects
# wall = Wall()
# floor = Floor()
# enemy = Enemy()
# player = Player()
# item1 = ShieldConsumable()
# item2 = HealthConsumable()
# item3 = Ammo()
# portal = Portal()
# gateOpen = GateOpen()
# gateClosed = GateClosed()
# map1.addObject(wall, 0, 0)
# map1.addObject(floor, 1, 0)
# map1.addObject(enemy, 2, 0)
# map1.addObject(player, 3, 0)
# map1.addObject(item1, 4, 0)
# map1.addObject(wall, 6, 2)
# map1.addObject(floor, 7, 2)
# map1.addObject(enemy, 8, 2)
# map1.addObject(player, 9, 2)
# map1.addObject(item1, 10, 2)
# log = MessageLog()
# # tcod.console.Console.default_bg = BLACK
# # tcod.console.Console.default_fg = WHITE
# while not tcod.console_is_window_closed():
# 	tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
def main():
	'''
	main loop
	'''
	#declaration and initialization
	map1 = Map(MAP_WIDTH, MAP_HEIGHT, 2)
	tcod.console_set_custom_font(FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)	#set console font
	console = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title="Trapped in Time RL", fullscreen=False)	#create main console
	tcod.sys_set_fps(FPS_CAP)	#set FPS cap; only if real-time, but keeping as acttion-rate limiter
	
	#stores key inputs
	key = tcod.Key()
	mouse = tcod.Mouse()
	# event = tcod.event()
	log = MessageLog()
	handler = InputListener()
	
	#main loop
	while not tcod.console_is_window_closed():
		tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
		
		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				if map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == True:	#if in FoV
					tcod.console_put_char_ex(console, x, y, map1.getTopEntity(x,y).getSymbol(), map1.getTopEntity(x,y).getBGColor(), map1.getTopEntity(x,y).getFGColor() )
# 				elif (map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == False and map1.isExplored(x, y) == True):
# 					tcod.console_put_char_ex(console, x, y, map1.getTopEntity(x,y).getSymbol(), BLACK, GRAY_LIGHT)
				elif (map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == False and map1.aSymbolMemory[x][y][map1.getPlayerZ()] != "" and map1.aBoolIsExplored[x][y][map1.getPlayerZ()] == True):
					#no more telepathy, but now first timeline doesn't get explored, period.
					tcod.console_put_char_ex(console, x, y, map1.aSymbolMemory[x][y][map1.getPlayerZ()], BLACK, GRAY_DARK)
				else:
					tcod.console_put_char_ex(console, x, y, " ", BLACK, BLACK)
	# 	tcod.console.Console.rect(console, 0, MAP_HEIGHT, STATUS_WIDTH, STATUS_HEIGHT, True, 0)
	# 	tcod.console.Console.rect(console, MAP_WIDTH - MESSAGE_WIDTH, MAP_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT, True, 0)
		log.printLog(console)
		tcod.console_flush()
	# 	tcod.console_blit(console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
		
		strCode = handler.handle_keys(key, mouse, map1)
		
		tcod.console_rect(console, 0, MAP_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT, True)
		
	# 	bTest = handle_event(mouse)
		if (mouse.cx >= 0 and mouse.cx < MAP_WIDTH) and (mouse.cy >= 0 and mouse.cy < MAP_HEIGHT):
	# 		tcod.console_set_default_background(console, ORANGE_LIGHT)
	# 		tcod.console_set_default_foreground(console, BLUE_LIGHT)
			tcod.console_rect(console, 0, MAP_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT, True)
			tcod.console.Console.print_(console, 0, MAP_HEIGHT, "(" + str(mouse.cx) + "," + str(mouse.cy) + "): " + map1.getTopEntity(mouse.cx, mouse.cy).getName() )	#"tooltip" lists top Entity's name
	# 		tcod.console_print_ex(console, 0, MAP_HEIGHT, tcod.BKGND_NONE, tcod.LEFT, "(" + str(mouse.cx) + "," + str(mouse.cy) + "): " + map1.alstObject[mouse.cx][mouse.cy][map1.top(mouse.cx, mouse.cy)].getName() + "   ")
	# 		tcod.console_flush()
		if (strCode == "code:EXIT"):
			break
#END main()

	
if __name__ == "__main__":
	main()