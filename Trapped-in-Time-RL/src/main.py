
'''
---CHANGELOG---
2019/04/24		(Bryan)
				Added Enemy movement (function located in enemy class in Entity module)
				End Game game state (prevents a dead player message from being spammed if one is added)
				
2019/04/20		(Bryan)
				Added level up condition
				
2019/04/19		(Bryan)
				Added Turn Order
				Added Enemy and Player Death Functions
				Finished item usability
        
2019/04/19:		(JSS5783)
				Status added.
				Story added.

2019/04/09:		(JSS5783)
				[BUGFIX] Font now displays properly in black background/white foreground.
				[BUGFIX] Longer messages are properly overwritten in console now.

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

# imports
import tcod
# from InputListener import *
from src.Map import *
from src.constants import *
from src.Entity import *
from src.MessageLog import *
from src.InputListener import *
from src.Status import *
from tcod.libtcodpy import console_set_char_foreground
from tcod import event
from GameStates import *
from DeathFunctions import *


def main():

# declaration and initialization
	map1 = Map(MAP_WIDTH, MAP_HEIGHT, 2)
	tcod.console_set_custom_font(FONT, tcod.FONT_LAYOUT_CP437)  # set console font
	console = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title="Trapped in Time RL (pre-alpha)", fullscreen=False)  # create main console
	tcod.sys_set_fps(FPS_CAP)  # set FPS cap; only if real-time, but keeping as acttion-rate limiter
	
	# stores key inputs
	key = tcod.Key()
	mouse = tcod.Mouse()
	# event = tcod.event()
	log = MessageLog()
	status = Status()
	handler = InputListener()
	gameState = GameStates.PLAYERS_TURN
	turnCount = 0

	log.addMessage("You awake in an abandoned factory, head pounding.")
	log.addMessage("Who... are you? You look yourself over.")
	log.addMessage("There is a strange watch-like device on one arm.")
	log.addMessage("SYSTEM: [g]rab item / [t]ime-travel /  move")
	
	# main loop
	while not tcod.console_is_window_closed():
		tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
    
		if gameState == GameStates.PLAYERS_TURN:
			print(gameState)
			if map1.getTopEntity(map1.getPlayerX(), map1.getPlayerY(), map1.getPlayerZ()).hp <= 0:
				gameState = GameStates.PLAYER_DEAD
				
			strCode = handler.handle_keys(key, mouse, map1, log, status)

			console.clear()

    # 	bTest = handle_event(mouse)
			if (mouse.cx >= 0 and mouse.cx < MAP_WIDTH) and (mouse.cy >= 0 and mouse.cy < MAP_HEIGHT):
    # 		tcod.console_set_default_background(console, ORANGE_LIGHT)
    # 		tcod.console_set_default_foreground(console, BLUE_LIGHT)
  # 			tcod.console_rect(console, 0, MAP_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT, True)
  # 			tcod.console.Console.print_(console, 0, MAP_HEIGHT, "(" + str(mouse.cx) + "," + str(mouse.cy) + "): " + map1.getTopEntity(mouse.cx, mouse.cy).getName() )	#"tooltip" lists top Entity's name
  				status.setTooltip("(" + str(mouse.cx) + "," + str(mouse.cy) + "): " + map1.getTopEntity(mouse.cx, mouse.cy).getName())  # "tooltip" lists top Entity's name
    # 		tcod.console_print_ex(console, 0, MAP_HEIGHT, tcod.BKGND_NONE, tcod.LEFT, "(" + str(mouse.cx) + "," + str(mouse.cy) + "): " + map1.alstObject[mouse.cx][mouse.cy][map1.top(mouse.cx, mouse.cy)].getName() + "   ")
    # 		tcod.console_flush()

			for y in range(MAP_HEIGHT):
				for x in range(MAP_WIDTH):
					if map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == True:  # if in FoV
						tcod.console_put_char_ex(console, x, y, map1.getTopEntity(x, y).getSymbol(), map1.getTopEntity(x, y).getBGColor(), map1.getTopEntity(x, y).getFGColor())
  # 				elif (map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == False and map1.isExplored(x, y) == True):
  # 					tcod.console_put_char_ex(console, x, y, map1.getTopEntity(x,y).getSymbol(), BLACK, GRAY_LIGHT)
					elif (map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == False and map1.aSymbolMemory[x][y][map1.getPlayerZ()] != "" and map1.aBoolIsExplored[x][y][map1.getPlayerZ()] == True):
						tcod.console_put_char_ex(console, x, y, map1.aSymbolMemory[x][y][map1.getPlayerZ()], BLACK, GRAY_DARK)

          # TODO: other timeline memory's inverted. "Assuming that the timelines are roughly analogous, here is what the MOST RECENT other one looked like"
  # 				elif (map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == False and map1.aSymbolMemory[x][y][map1.getPlayerZ()] != "" and map1.aBoolIsExplored[x][y][map1.getPlayerZ()] == True):
  # 					tcod.console_put_char_ex(console, x, y, map1.aSymbolMemory[x][y][map1.getPlayerZ()], BLACK, GRAY_DARK)
					else:
						tcod.console_put_char_ex(console, x, y, " ", BLACK, BLACK)
    # 	tcod.console.Console.rect(console, 0, MAP_HEIGHT, STATUS_WIDTH, STATUS_HEIGHT, True, 0)
    # 	tcod.console.Console.rect(console, MAP_WIDTH - MESSAGE_WIDTH, MAP_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT, True, 0)
			log.printLog(console)
			status.printStatus(console)
			tcod.console_flush()
    # 	tcod.console_blit(console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

  # 		tcod.console_rect(console, 0, MAP_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT, True)
			if (strCode == "code:EXIT"):
				break
			if (strCode == "endTurn"):
				gameState = GameStates.ENEMY_TURN
				turnCount += 1
				print(turnCount)
			if map1.getUnderPlayer().strName == "portal":
				print("level up")
				gameState = GameStates.LEVEL_UP

		if gameState == GameStates.ENEMY_TURN:
			print(gameState)
			for x in range(MAP_WIDTH):
				for y in range(MAP_HEIGHT):
					if map1.getTopEntity(x, y).strName == "enemy":
						ENEMIES.append(map1.getTopEntity(x, y))
			print(ENEMIES)
			print(len(ENEMIES))
			for enemy in ENEMIES:
				if enemy.hp <= 0:
					deadEnemy(enemy, map1)
				elif (map1.aTcodMaps[enemy.z].fov[enemy.y][enemy.x] == True):
					enemy.move(map1)
			ENEMIES.clear()
			gameState = GameStates.PLAYERS_TURN   
			
		if gameState == GameStates.LEVEL_UP:
			log.addMessage("CONGRATULATIONS! You have leveled up.  Blasters now have unlimited ammo.  Have fun storming the castle!")
			Blaster.ammo = float('inf')
			map1.aLstEntities[map1.getPlayerX()][map1.getPlayerY()][map1.getPlayerZ()].remove(map1.getUnderPlayer())
			gameState = GameStates.ENEMY_TURN

		if gameState == GameStates.PLAYER_DEAD:
			
			deadPlayer(map1.getTopEntity(map1.getPlayerX(), map1.getPlayerY(), map1.getPlayerZ()))
			
			for y in range(MAP_HEIGHT):
				for x in range(MAP_WIDTH):
					if map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == True:  # if in FoV
						tcod.console_put_char_ex(console, x, y, map1.getTopEntity(x, y).getSymbol(), map1.getTopEntity(x, y).getBGColor(), map1.getTopEntity(x, y).getFGColor())
  # 				elif (map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == False and map1.isExplored(x, y) == True):
  # 					tcod.console_put_char_ex(console, x, y, map1.getTopEntity(x,y).getSymbol(), BLACK, GRAY_LIGHT)
					elif (map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == False and map1.aSymbolMemory[x][y][map1.getPlayerZ()] != "" and map1.aBoolIsExplored[x][y][map1.getPlayerZ()] == True):
						tcod.console_put_char_ex(console, x, y, map1.aSymbolMemory[x][y][map1.getPlayerZ()], BLACK, GRAY_DARK)

          # TODO: other timeline memory's inverted. "Assuming that the timelines are roughly analogous, here is what the MOST RECENT other one looked like"
  # 				elif (map1.aTcodMaps[map1.getPlayerZ()].fov[y][x] == False and map1.aSymbolMemory[x][y][map1.getPlayerZ()] != "" and map1.aBoolIsExplored[x][y][map1.getPlayerZ()] == True):
  # 					tcod.console_put_char_ex(console, x, y, map1.aSymbolMemory[x][y][map1.getPlayerZ()], BLACK, GRAY_DARK)
					else:
						tcod.console_put_char_ex(console, x, y, " ", BLACK, BLACK)
    # 	tcod.console.Console.rect(console, 0, MAP_HEIGHT, STATUS_WIDTH, STATUS_HEIGHT, True, 0)
    # 	tcod.console.Console.rect(console, MAP_WIDTH - MESSAGE_WIDTH, MAP_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT, True, 0)
			log.printLog(console)
			status.printStatus(console)
			tcod.console_flush()
			gameState = GameStates.END_GAME
			
		if gameState == GameStates.END_GAME:
			strCode = handler.handle_keys(key, mouse, map1, log, status)
			if (strCode == "code:EXIT"):
				break

# END main()

	
if __name__ == "__main__":
	main()
