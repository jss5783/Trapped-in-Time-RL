'''
---CHANGELOG---
2019/04/17:		(JSS5783)
				Added removeEntityAt.
				addEntityAt, getEntityAt, getEntityIndexAt, and removeEntityAt all work now, with updating FoV.

				
2019/04/15:		(JSS5783)
				Continued working on addEntityAt, getEntityAt, and getEntityIndexAt.


2019/04/11:		(JSS5783)
				Added addEntityAt, getEntityAt, and getEntityIndexAt.


2019/04/10:		(JSS5783)
				Added Map.printTileContents().
				Moved memory code out of updateFoV() and into updateMemory().
				[BUGFIX] Got rid of phantom players; got first timeline to save in memory.


2019/04/09		(JSS5783)
				Rolled back attempts at adding Entity ID and Map coordinate Position system, none of which were ever pushed upstream because they weren't just buggy WIP, they were completely broken code.
				Refactored the last working build from 2019/04/06.
					Timeline merged into Map.
					Map is much more human-readable (code, comments, functions).
					"Remembered explored (but not in FoV)"-type of FoV added.
					[BUG] Phantom players from time-traveling (or spooky feature?). Does not record timeline[0].
				Moved license code to LICENSES.txt.
					

2019/04/08		(JSS5783)
				Tried to refactor code, merging Timeline class back into Map.
					Could barely make sense of Map+Timeline code with all of the duplicate methods and tacked on TCoD maps.
						Could not understand/finish own attempts at adding Entity ID and Map coordinate Position system.
				Rolled back attempts at adding Entity ID and Map coordinate Position system.

2019/04/06		(JSS5783)
				Worked on adding time travel and FoV.
					FoV works. No "remembered explored (but not in FoV)"-type of FoV yet. 
					Time travel worked... very, very briefly.

2019/04/05		(JSS5783)
				Moved Map bits into Timeline.

2019/03/29		(JSS5783)
				Partially-implemented addObject.
				Added updatePlayerPosition.
				
2019/03/27		(JSS5783)
				Now adds actual entities to map, instead of just characters.

2019/03/22		(JSS5783)
				Map.py created and related functions.
'''

import tcod, numpy
from src.constants import *
from idlelib.iomenu import encoding
import codecs
from src.Entity import *
from random import *
from src.MessageLog import *
from src.Item import *
from src.item_functions import *
from tcod.constants import FOV_BASIC


	#	TODO: add turn order, action code here?, I guess (probably belongs within InputListener).
	#	if Player in same map and monster in FoV, then move toward player; else, move randomly (if letting "time pass" or wait (pass turn). Monsters always have full knowledge of their map (no extra FoV calculations).
	#	Base map (Floor = "mossy cobblestone"/Wall = "tree") and non-Floor/Wall entities eventually perhaps, but whole maps for now, sans player in non-starting map.
class Map:
	'''
	Contains map-relevant data (visibility mapping, etc.).
	A Map has [1,10] timelines.
	Each timeline has FoV/walkability/transparency + entities
	entities only check in same timeline, time-traveling aside
	'''
	def __init__(self, intInWidth, intInHeight, intInDepth): 
		self.intWidth = intInWidth
		self.intHeight = intInHeight
		self.intDepth = intInDepth	#might be better to call this something else when floors are implemented. NOTE: like intWidth and intheight, this is 1-indexed
			#intCyrrentTimeline would be a 0-indexed "current timeline" name
		self.aLstEntities = [[[list() for z in range(self.intDepth)] for y in range(self.intHeight)] for x in range(self.intWidth)]	#x=horizontal, y=vertical, z=timeline
		self.aTcodMaps = [tcod.map.Map(self.intWidth, self.intHeight) for z in range(self.intDepth)]	#required for TCoD FoV calculations and such.	TODO: come up with better name; WARNING: uses (y,x) numpy-style coordi
		print(self.aTcodMaps[0])
		self.aBoolIsExplored = [[[bool(False) for z in range(self.intDepth)] for y in range(self.intHeight)] for x in range(self.intWidth)]	#is tile known by player and therefore should be visible (and not complete blackness)?
		self.aSymbolMemory = [[[str() for z in range(self.intDepth)] for y in range(self.intHeight)] for x in range(self.intWidth)]	#top entity char is stored when moving out of FoV
			#technically a String because Python char differs from Java char. Don't store more than 1 character (the symbol) in it
		
		self.intPlayerX = -1	#TODO: better location/error marker
		self.intPlayerY = -1
		self.intPlayerZ = -1
		if DEBUG_MODE: print("[DEBUG] Map__init__", self.intPlayerX, self.intPlayerY, self.intPlayerZ)
		
		for y in range(self.intHeight):
			for x in range(self.intWidth):
				self.aTcodMaps[self.intDepth - 1].fov[y][x] = False			#in FoV?
		
		#TODO: replace with real loading code; add map generator too
		#TODO: replace placeholder 2 with folder file-count	TODO: put paired timelines into folders and process that.
		if (DEBUG_MODE):
			self.loadMapFile("../resources/L01_T0_80x45.txt", 0)
			self.loadMapFile("../resources/L01_T1_80x45.txt", 1)
			print("[DEBUG] Map__init__", self.intPlayerX, self.intPlayerY, self.intPlayerZ)
		else:
			self.loadMapFile("../resources/L01_T0_80x45.txt", 0)
			self.loadMapFile("../resources/L01_T1_80x45.txt", 1)
		
		self.updateFoV()
	#END __init__(self, intInWidth, intInHeight, intInDepth)	


	def loadMapFile(self, strFilePath, intInTimeline):
		'''
		Loads map from file into aLstEntities and aTcodMaps. (aBoolIsExplored is updated with FoV)
		TODO: Add Entities to Position list and Entity IDs here.
		Uses intWidth for map sizing, etc., so map files are modified to fit as needed.
			intTimeline is 0-based
		'''
		try:
			self.fileMap = codecs.open(strFilePath, encoding="utf-8")	#must use utf-8 or else "•" is read as "â€¢"
			self.strCurrentLine = ""
	# 		print("file open!")
	# 		aMap = [[list(Floor() ) for y in range(intMapHeight)] for x in range(intMapWidth)]	#just auto-fill everything with a floor underneath
			
			self.rng = tcod.random.Random(tcod.random.MERSENNE_TWISTER, SEED)
			
			for y in range(self.intHeight):
				self.strCurrentLine = self.fileMap.readline()
	# 			print(self.strCurrentLine)
				for x in range(self.intWidth):
					if (self.strCurrentLine[x] == "."):
						self.aLstEntities[x][y][intInTimeline].append(Floor() )	#get last used ID
						self.aTcodMaps[intInTimeline].transparent[y][x] = True	#allows light through?
						self.aTcodMaps[intInTimeline].walkable[y][x] = True		#walkable? (not solid?)
						
					elif (self.strCurrentLine[x] == "@"):
						self.aLstEntities[x][y][intInTimeline].append(Floor() )	#add Floor beneath Player
						self.aLstEntities[x][y][intInTimeline].append(Player() )
						self.aTcodMaps[intInTimeline].transparent[y][x] = True	#allows light through?
						self.aTcodMaps[intInTimeline].walkable[y][x] = False		#walkable? (not solid?)
						self.intPlayerX = x
						self.intPlayerY = y
						self.intPlayerZ = intInTimeline
						if DEBUG_MODE: print(self.intPlayerX, self.intPlayerY, self.intPlayerZ)
						#TODO: set Player x, y so map refreshes properly (at -1, -1 right now)
					elif (self.strCurrentLine[x] == "E"):
						self.aLstEntities[x][y][intInTimeline].append(Floor() )
						self.aLstEntities[x][y][intInTimeline].append(Enemy() )
						self.aTcodMaps[intInTimeline].transparent[y][x] = True	#allows light through?
						self.aTcodMaps[intInTimeline].walkable[y][x] = False		#walkable? (not solid?)
						
						enemy = Baddie(x, y, 4)
						ENEMIES.append(enemy)
						
					elif (self.strCurrentLine[x] == "!"):	#place random item
						self.aLstEntities[x][y][intInTimeline].append(Floor() )
						self.intResult = self.rng.randint(0,2)
						
#             			randItem = randint(0,2)
# 						if randItem == 0:
# 							item = Item(x, y, "Blaster", 4, 4, 2)
# 							ITEMS.append(item)
# 							print(item.strName)
# 						elif randItem == 1:
# 							item = Item(x, y, "Fisto Kit", 2, 2, 5)
# 							ITEMS.append(item)
# 							print(item.strName)
# 						elif randItem == 2:
# 							item = Item(x, y, "Shield", 5, 5)
# 							ITEMS.append(item)
# 							print(item.strName)
							
						if (self.intResult == 0):
							self.aLstEntities[x][y][intInTimeline].append(HealthConsumable() )
						elif (self.intResult == 1):
							self.aLstEntities[x][y][intInTimeline].append(ShieldConsumable() )
						elif (self.intResult == 2):
							self.aLstEntities[x][y][intInTimeline].append(Ammo() )
						
						self.aTcodMaps[intInTimeline].transparent[y][x] = True	#allows light through?
						self.aTcodMaps[intInTimeline].walkable[y][x] = True		#walkable? (not solid?)
					elif (self.strCurrentLine[x] == "☼"):
						self.aLstEntities[x][y][intInTimeline].append(Floor() )
						self.aLstEntities[x][y][intInTimeline].append(Portal() )
						self.aTcodMaps[intInTimeline].transparent[y][x] = True	#allows light through?
						self.aTcodMaps[intInTimeline].walkable[y][x] = False		#walkable? (not solid?)
						
					elif (self.strCurrentLine[x] == "▬"):
						self.aLstEntities[x][y][intInTimeline].append(Floor() )
						self.aLstEntities[x][y][intInTimeline].append(GateOpen() )
						self.aTcodMaps[intInTimeline].transparent[y][x] = True	#allows light through?
						self.aTcodMaps[intInTimeline].walkable[y][x] = True		#walkable? (not solid?)
						
					elif (self.strCurrentLine[x] == "╬"):
						self.aLstEntities[x][y][intInTimeline].append(Floor() )
						self.aLstEntities[x][y][intInTimeline].append(GateClosed() )
						self.aTcodMaps[intInTimeline].transparent[y][x] = False	#allows light through?
						self.aTcodMaps[intInTimeline].walkable[y][x] = False		#walkable? (not solid?)
						
					else:	#assuming that blank space/errors should all be Walls for now
						self.aLstEntities[x][y][intInTimeline].append(Floor() )
						self.aLstEntities[x][y][intInTimeline].append(Wall() )
						self.aTcodMaps[intInTimeline].transparent[y][x] = False	#allows light through?
						self.aTcodMaps[intInTimeline].walkable[y][x] = False		#walkable? (not solid?)
						
			self.fileMap.close()
		finally:
			self.fileMap.close()
	#ENF loadMapFile(self, strFilePath, intInTimeline)


	def getTopIndex(self, x, y, z=-1):
		'''
		getTopIndexAtTile
		Returns top Entity's index at given coordinates.
			(generally player/monster/wall/portal, assuming a stack of floor+item+player, but if none exist, then something like an item probably)
		Otherwise, return floor tile.
		'''
		if (z == -1):	#if no z value given, use player's z-coord
			if len(self.aLstEntities[x][y][self.getPlayerZ() ] ) > 0:
				return len(self.aLstEntities[x][y][self.getPlayerZ() ] ) - 1
			else:
				return 0
		else:	#if z value given
			if len(self.aLstEntities[x][y][z] ) > 0:
				return len(self.aLstEntities[x][y][z] ) - 1
			else:
				return 0
	#END getTopIndex(self, x, y, z=-1):
	
	
	def getEntityIndexAt(self, inEntityType : Entity, intInX, intInY, intInZ=-1):
		'''
			getEntityIndexAtTile
			Finds the index of the given Entity type (e.g., HealthRestorative) in a tile and returns it.
			TODO (real version): Handle duplicate Entity types (e.g., health pack #1, and then health pack #2 dropped). 
		'''
		if (intInZ == -1):
			intInZ = self.getPlayerZ()
		
		self.intEntityIndex = 0
		
		for i in range(len(self.aLstEntities[intInX][intInY][intInZ]) ):
			if isinstance(self.aLstEntities[intInX][intInY][intInZ][i], type(inEntityType) ):
				self.intEntityIndex = i
# 		print(self.intEntityIndex)
		
		return self.intEntityIndex
	#END getEntityIndexAt(self, inEntityType, intInX, intInY, intInZ=-1)
	
	
	def addEntityAt(self, inEntity, intInX, intInY, intInZ=-1, intInDropRadius=1):
		'''
			addEntityAtTile
			Adds given Entity where appropriate in given tile. If Entity cannot be added for some reason in given tile, checks around the tile (default radius = 1 tile out) for an empty space in the same timeline to use instead.
			TODO (real version): Drop items in random available space (in first free space when first implementing). Probably use a boolean canPlaceItem[x][y], pick until True (placeable) is found, and then use those random x and y values in aLstEntities[randX][randY][intPlayerZ].
				Do multiple times/in a pattern for AoEs.
			Return -1 if cannot add Entity.
			TODO: add/remove blocking. Removed enemy = walkable.
		'''
		if (intInZ == -1):
			intInZ = self.getPlayerZ()
		
		self.strInEntity = ""
		
		
		if isinstance(inEntity, GateClosed) or isinstance(inEntity, Portal) or isinstance(inEntity, Wall):
			self.strInEntity = "FULL"	#"full"
		elif isinstance(inEntity, Enemy) or isinstance(inEntity, Player):
			self.strInEntity = "CREATURE"	#creature
		elif isinstance(inEntity, HealthConsumable) or isinstance(inEntity, ShieldConsumable) or isinstance(inEntity, Ammo):
			self.strInEntity = "ITEM"	#items
		elif isinstance(inEntity, GateOpen):
			self.strInEntity = "TERRAIN"	#GateOpen
		elif isinstance(inEntity, Floor):
			self.strInEntity = "FLOOR"	#floor or GateOpen (TODO (real version): separate this out, just in case of "Summon Gate" skill or something that might stack Gates.
		else:
			self.strInEntity = "[ERROR] unknown strInEntity"
			
		print("self.strInEntity", self.strInEntity)
		
		self.strTileEntityTop = ""
		
		if isinstance(self.getTopEntity(intInX, intInY, intInZ), GateClosed) or isinstance(self.getTopEntity(intInX, intInY, intInZ), Portal) or isinstance(self.getTopEntity(intInX, intInY, intInZ), Wall):
			self.strTileEntityTop = "FULL"	# "full" tile
		elif isinstance(self.getTopEntity(intInX, intInY, intInZ), Enemy) or isinstance(self.getTopEntity(intInX, intInY, intInZ), Player):
			self.strTileEntityTop = "CREATURE"	#creature on top
		elif isinstance(self.getTopEntity(intInX, intInY, intInZ), HealthConsumable) or isinstance(self.getTopEntity(intInX, intInY, intInZ), ShieldConsumable) or isinstance(self.getTopEntity(intInX, intInY, intInZ), Ammo):
			self.strTileEntityTop = "ITEM"	#items
		elif isinstance(self.getTopEntity(intInX, intInY, intInZ), GateOpen):
			self.strTileEntityTop = "TERRAIN"	#GateOpen
		elif isinstance(self.getTopEntity(intInX, intInY, intInZ), Floor):
			self.strTileEntityTop = "FLOOR"	#floor
		print("self.strTileEntityTop", self.strTileEntityTop)
		if self.strTileEntityTop == "FULL":	#can't place anything in full tile
			return -1
		elif self.strTileEntityTop == "CREATURE":	#can't place FULL or CREATURE... or TERRAIN
			if self.strInEntity == "FULL" or self.strInEntity == "CREATURE" or self.strInEntity == "TERRAIN" or self.strInEntity == "FLOOR":
				return -1
			elif self.strInEntity == "ITEM":
# 				self.aLstEntities[intInX][intInY][intInZ].insert(self.getTopIndex(intInX, intInY) - 1, inEntity)	#TODO: test Entity placement (item under creature)
				self.aLstEntities[intInX][intInY][intInZ].insert(len(self.aLstEntities[intInX][intInY][intInZ]) - 1, inEntity)
			else:	#else do nothing; can't add more GateOpens (TERRAIN) or Floor to Floor for now 
				return -1
			#else do nothing; can't add more GateOpens (TERRAIN) or Floor to Floor for now 
		elif self.strTileEntityTop == "ITEM":
			if self.strInEntity == "CREATURE" or self.strInEntity == "ITEM":
				self.aLstEntities[intInX][intInY][intInZ].append(inEntity)
				if self.strInEntity == "FULL" or self.strInEntity == "CREATURE":
					self.aTcodMaps[intInZ].walkable[intInY][intInX] = False
# 					self.aTcodMaps[intInZ].transparent[intInY][intInX] = False
			elif self.strInEntity == "FULL" or self.strInEntity == "TERRAIN" or self.strInEntity == "FLOOR":
				return -1
# 				self.aLstEntities[intInX][intInY][intInZ].insert(len(self.aLstEntities) - 2, inEntity)
		elif self.strTileEntityTop == "TERRAIN":
			if self.strInEntity == "CREATURE" or self.strInEntity == "ITEM":
				self.aLstEntities[intInX][intInY][intInZ].append(inEntity)
				if self.strInEntity == "CREATURE":
					self.aTcodMaps[intInZ].walkable[intInY][intInX] = False
			else:	#self.strInEntity == "FULL" or self.strInEntity == "TERRAIN" or self.strInEntity == "FLOOR":
				return -1
		else:	#else do nothing; can't add more GateOpens (TERRAIN) or Floor to Floor for now 
			if self.strInEntity != "FLOOR":
				self.aLstEntities[intInX][intInY][intInZ].append(inEntity)
				if self.strInEntity == "FULL" or self.strInEntity == "CREATURE":
					self.aTcodMaps[intInZ].walkable[intInY][intInX] = False
				if self.strInEntity == "FULL":
					self.aTcodMaps[intInZ].transparent[intInY][intInX] = False
			else:
				return -1
		
		self.updateFoV()
	#END addEntityAt(self, inEntity, intInX, intInY, intInZ=-1, intInDropRadius=1)
	
	
	def getEntityAt(self, intInEntityIndex, intInX, intInY, intInZ=-1):
		'''
			getEntityAtTileIndex
			Finds the Entity of the given index (e.g., HealthRestorative) in a tile and returns it.
		'''
		if (intInZ == -1):
			intInZ = self.getPlayerZ()
		
		return self.aLstEntities[intInX][intInY][intInZ][intInEntityIndex]
	#END getEntityAt(self, intInEntityIndex, intInX, intInY, intInZ=-1)
	
	
	def removeEntityAt(self, inEntity : Entity, intInX, intInY, intInZ=-1):
		'''
		Removes Entity of given type at given Map coordinates.
			TODO: remove specific Entity, not first instance in list.
			Ammo (3) != Ammo (5).
		'''
		if (intInZ == -1):
			intInZ = self.getPlayerZ()
		
			print("is",self.strInEntity)
		#IF Entity type at target index = inbound Entity type, THEN delete
		if isinstance(self.aLstEntities[intInX][intInY][intInZ][self.getEntityIndexAt(inEntity, intInX, intInY)], type(inEntity)):
			self.strInEntity = ""
			
			if isinstance(inEntity, GateClosed) or isinstance(inEntity, Portal) or isinstance(inEntity, Wall):
				self.strInEntity = "FULL"	# "full" tile
			elif isinstance(inEntity, Enemy) or isinstance(inEntity, Player):
				self.strInEntity = "CREATURE"	#creature on top
			elif isinstance(inEntity, HealthConsumable) or isinstance(inEntity, ShieldConsumable) or isinstance(inEntity, Ammo):
				self.strInEntity = "ITEM"	#items
			elif isinstance(inEntity, GateOpen):
				self.strInEntity = "TERRAIN"	#GateOpen
			elif isinstance(inEntity, Floor):
				self.strInEntity = "FLOOR"	#floor
			if self.strInEntity == "FULL" or self.strInEntity == "CREATURE":
				self.aTcodMaps[intInZ].walkable[intInY][intInX] = True
			if self.strInEntity == "FULL":
				self.aTcodMaps[intInZ].transparent[intInY][intInX] = True
				
			del self.aLstEntities[intInX][intInY][intInZ][self.getEntityIndexAt(inEntity, intInX, intInY)]
			#TODO: return it. Or just GET and REMOVE in 2 lines

			self.updateFoV()
	#END removeEntityAt(self, inEntity : Entity, intInX, intInY, intInZ=-1
	
	
	def removeEntityAtIndex(self, intInEntityIndex, intInX, intInY, intInZ=-1):
		'''
		Removes Entity at given tile index at given Map coordinates.
		'''
		if (intInZ == -1):
			intInZ = self.getPlayerZ()
		
		if (intInEntityIndex <= len(self.aLstEntities[intInX][intInY][intInZ]) - 1 and not isinstance(self.aLstEntities[intInX][intInY][intInZ][intInEntityIndex], Player)):
			self.strInEntity = ""
			
			if isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), GateClosed) or isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), Portal) or isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), Wall):
				self.strInEntity = "FULL"	# "full" tile
			elif isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), Enemy) or isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), Player):
				self.strInEntity = "CREATURE"	#creature on top
			elif isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), HealthConsumable) or isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), ShieldConsumable) or isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), Ammo):
				self.strInEntity = "ITEM"	#items
			elif isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), GateOpen):
				self.strInEntity = "TERRAIN"	#GateOpen
			elif isinstance(self.getEntityAt(intInEntityIndex, intInX, intInY, intInZ), Floor):
				self.strInEntity = "FLOOR"	#floor
			if self.strInEntity == "FULL" or self.strInEntity == "CREATURE":
				self.aTcodMaps[intInZ].walkable[intInY][intInX] = True
			if self.strInEntity == "FULL":
				self.aTcodMaps[intInZ].transparent[intInY][intInX] = True
			
			del self.aLstEntities[intInX][intInY][intInZ][intInEntityIndex]
			
			self.updateFoV()
			


	#END removeEntityAtIndex(self, intInEntityIndex, intInX, intInY, intInZ=-1)
	

	def getTopEntity(self, x, y, z=-1):
		'''
		Returns top Entity at given coordinates.
			(generally player/monster/wall/portal, assuming a stack of floor+item+player, but if none exist, then something like an item probably)
		(Otherwise, return floor tile.)
		'''
		if (z == -1):	#if no z value given, use player's z-coord
			return self.aLstEntities[x][y][self.getPlayerZ()][self.getTopIndex(x, y, self.getPlayerZ() ) ]
# 			return self.getTopEntity(x, y, self.getPlayerZ())
		else:	#if z value given
# 			return self.getTopEntity(x, y, z)
			return self.aLstEntities[x][y][z][self.getTopIndex(x, y, z) ]
	#END getTopEntity(self, x, y, z=-1)
# # 
# 	def getTopEntity(self, x, y, z=-1):
# 		if len(self.alstObject[x][y]) > 0:
# 			return self.alstObject[x][y][len(self.alstObject[x][y]) - 1]
# # 			return len(self.alstObject[x][y] - 1)
# 		else:
# 			return self.alstObject[x][y]
# 		
# 		if (z == -1):
# 			if len(self.aLstEntities[x][y][self.getPlayerZ() ] ) > 0:
# 				return self.aLstEntities[x][y][self.getPlayerZ() ].getTopIndex(x, y, z)
# 			else:
# 				return self.aLstEntities[x][y][self.getPlayerZ() ][0]
# 		else:	#if z value given
# 			if len(self.aLstEntities[x][y][z] ) > 0:
# 				return len(self.aLstEntities[x][y][z] ) - 1
# 			else:
# 				return 0
# # 			return self.aLstEntities[x[y][self.getPlayerZ()]
# 	#END top(self, x, y)

# 	
# 	'''
# 	Returns index at "bottom" of list (generally item, assuming a stack of floor+item+player, but if no items exist, then something like a player/monster/wall/portal probably)
# 	'''
# 	def getBottomIndex(self, x, y, z=-1):
# 		if z == -1:
# 			if len(self.aLstEntities[x][y][self.intPlayerZ]) > 0:
# 				return 1
# 			else:
# 				return 0	#returns value for floor (tile is empty)
# 		else:
# 			if len(self.aLstEntities[x][y][z]) > 0:
# 				return 1
# 			else:
# 				return 0	#returns value for floor (tile is empty)
	
# 	'''
# 	Returns Entity at "bottom" of list (generally item, assuming a stack of floor+item+player, but if no items exist, then something like a player/monster/wall/portal probably)
# 	'''
# 	def getBottomEntity(self, x, y, z=-1):
# 		if z == -1:
# 			return self.aLstEntities[self.getPlayerZ()].bottom(x, y)
# 		else:
# 			return self.aTimelines[z].bottom(x, y)

# 
# 	def isEmptyTile(self, x, y, z=-1):
# 		if z == -1:
# 			if len(self.alstObject[x][y][self.intPlayerZ]) > 1:
# 				return False
# 			else:	#floor-only (tile is empty)
# 				return True
# 		else:
# 			if len(self.alstObject[x][y][z]) > 1:
# 				return False
# 			else:	#floor-only (tile is empty)
# 				return True
# 	#END isEmptyTile(self, x, y, z=-1)
	
	

	def addObject(self, entInEntity, x, y, z=-1):
		'''
		TODO: unused for now, so probably not properly converted
		Adds entInEntity to map1[x, y], placing it in the stack where necessary.
		TODO: handle "player/enemy/wall/gate (open/closed)/portal replacing other 'top'-placed entity"
		For now, if 'top' and 'top', nothing, 'middle' appends on top of middle, and 'top' on 'top'-less middle.
			Other conditions, like 'bottom' and 'bottom' nothing are NOT handled.
		'''
		if z == -1:
			z = self.getPlayerZ()
		
		self.intEntityPlacement = self.getTopIndex(x, y, z)
		if (DEBUG_MODE): print("[DEBUG] addObject:", type(entInEntity))
		if (isinstance(entInEntity, Player) or isinstance(entInEntity, Enemy) or isinstance(entInEntity, Wall) or isinstance(entInEntity, GateClosed) or isinstance(entInEntity, GateOpen) or isinstance(entInEntity, Portal) ):
			self.bIsInTopObject = True
		else:
			self.bIsInTopObject = False
		if (isinstance(self.aLstEntities[x][y][z][self.intEntityPlacement], Player) or isinstance(self.aLstEntities[x][y][z][self.intEntityPlacement], Enemy) or isinstance(self.aLstEntities[x][y][z][self.intEntityPlacement], Wall) or isinstance(self.aLstEntities[x][y][z][self.intEntityPlacement], GateClosed) or isinstance(self.aLstEntities[x][y][z][self.intEntityPlacement], GateOpen) or isinstance(self.aLstEntities[x][y][z][self.intEntityPlacement], Portal) ):	
			self.bHasCurrentTopObject = True
		else:
			self.bHasCurrentTopObject = False
		if (self.bIsInTopObject == False and self.bHasCurrentTopObject == True):
			if (DEBUG_MODE): print("![DEBUG] addObject: non-top-level entity " + entInEntity.getName() + " inserted above " + self.getTopEntity(x, y).getName() )
			self.aLstEntities[x][y][z].insert(self.top(x, y) - 1, entInEntity)
		elif (not self.bHasCurrentTopObject):
			if (DEBUG_MODE): print("[DEBUG] entity " + entInEntity.getName() + " inserted above " + self.getTopEntity.getName() )	#TODO: is this used?
	# 		self.alstObject[x][y].insert(self.top(x, y), entInEntity)
			self.aLstEntities[x][y][z].append(entInEntity)
			
# 		
# 			    and self.alstObject[x][y][self.top(x, y)] is Player):	#if entInEntity is Player and top item in stack is already Player
# 			self.alstObject[x][y][self.top(x, y)] = entInEntity	#replace old player with new player (if replacing for some reason, just in case)
# 		elif (entInEntity is Player and self.alstObject[x][y][self.top(x, y)] is Player):	#insert item right under player
# 			if (self.alstObject[x][y][self.top(x, y)] is Player):
# 				self.intEntityPlacement -= 1
# 		
# 		#player, entity, wall, gate open/closed, portal
# 		items
# 		floor
# 		
# 		#then 
# 		#else placementLocation = stack length - 
# 		
# 		
# 		#elif floor
# 		#if floor exists
# 		#replace floor (though it should always be there)
# 		#check if top object is wall/player/monster/etc
# 		#if yes, then insert (top - 1) ((or copy-save old (top - 1) value, overwrite, and then append old value
# 		#else append

	#TODO: finish implementation of addEntityAt, getEntityAt, and getEntityIndexAt.
	def updatePlayerPosition(self, x, y, z=-1):
		'''
		Tries to move Player to given coordinates.
		Used for time-traveling.
		'''
# 		if (self.alstObject[self.intPlayerX][self.intPlayerY][self.top(x, y)] == "@"):
# 		self.alstObject[self.intPlayerX][self.intPlayerY].remove("@")
# 		for i in range(len(self.alstObject[x][y]) ):
# 			print("[DEBUG] updatePlayerPosition at ", x, ",", y, ":", self.alstObject[x][y])
		if (DEBUG_MODE): print("[DEBUG] updatePlayerPosition from", self.getPlayerX(), self.getPlayerY(), self.getPlayerZ(), "to", x, ",", y, ",", z, ":", self.aLstEntities[x][y][z])
		self.bVerifyTimeTravel = False
		self.bIsSafe = True
		self.bIsBlocked = True
		
# 		self.alstObject[x][y].append(Player() )
		if (z != -1 and z != self.getPlayerZ() ):
			self.bVerifyTimeTravel = True
		elif (z == -1):	#probably fine with just else here, but just in case for now
			z = self.getPlayerZ()
			self.bVerifyTimeTravel = False
		
		#is destination within Map bounds?
		if (x >= 0 and x < self.intWidth and y >= 0 and y < self.intHeight and z >= 0 and z < self.intDepth):
			if DEBUG_MODE: print("[DEBUG] Destination is walkable?", self.aTcodMaps[z].walkable[y][x])
			if (self.isWalkable(x, y, z) == True):		#is Player's destination blocked?
		# 		print(type(inMap.getTopEntity(inMap.aTimelines[1].intPlayerX,inMap.aTimelines[1].intPlayerY)))
				self.bIsBlocked = False
			else:
				self.bIsBlocked = True
		
		#TODO: any movement should verify that destination works; only z-travel should do "safety check"
			if (self.bVerifyTimeTravel == True):	#if time-traveling, is it safe around the Player? (eventually, Player should be able to risky-timeline-jump; maybe instant-travel but missed turn instead of wait-and-then-(safe)-travel-for-a-free-ranged-attack)
					#BUGFIX: all movement was 1SE because x was used as "incrementing x-coordinate" for testing here, but also x as "passed x-coordinate". This is why "intInX" is a good idea.
				for yCounter in range(self.getPlayerY() - 1, self.getPlayerY() + 2):
					for xCounter in range(self.getPlayerX() - 1, self.getPlayerX() + 2):
						if DEBUG_MODE: print("[DEBUG] Testing for safe time travel: ", self.getTopEntity(xCounter,yCounter,z) )
	# 					self.aLstEntities[x][y][z]
						#TODO: if timelines use the same overall layout, add Wall+Gate (open AND closed) to checks. Other timeline: "has Enemy, item, or even Portal?"
	# 					if (type(self.getTopEntity(x,y,z) ) != Floor and type(self.getTopEntity(x,y,z) ) != Player) :
# 						if (isinstance(self.getTopEntity(xCounter,yCounter,z), Floor) == False or type(self.getTopEntity(xCounter,yCounter,z) ) != Wall and type(self.getTopEntity(xCounter,yCounter,z) ) != GateClosed and type(self.getTopEntity(xCounter,yCounter,z) ) != GateClosed):
# 						if (isinstance(self.getTopEntity(xCounter,yCounter,z), Enemy) or isinstance(self.getTopEntity(xCounter,yCounter,z), ShieldConsumable) or isinstance(self.getTopEntity(xCounter,yCounter,z), HealthConsumable) or isinstance(self.getTopEntity(xCounter,yCounter,z), Ammo) or isinstance(self.getTopEntity(xCounter,yCounter,z), Portal)):
						if (isinstance(self.getTopEntity(xCounter,yCounter,z), Enemy) or isinstance(self.getTopEntity(xCounter,yCounter,z), Portal)):	#only "risky" if Enemy or Portal - not Item
							self.bIsSafe = False
	# 			if (type(inMap.getTopEntity(inMap.aTimelines[self.intTargetTimeline].intPlayerX,inMap.aTimelines[self.intTargetTimeline].intPlayerY)) != Floor and type(inMap.getTopEntity(inMap.aTimelines[self.intTargetTimeline].intPlayerX,inMap.aTimelines[self.intTargetTimeline].intPlayerY)) != Player):
				
						
# 			if self.bIsBlocked == False and self.bIsSafe == False:
# 				if DEBUG_MODE: print("[DEBUG] can travel, something \"large\"(wall/enemy/portal?) nearby. Time-travel anyway?")
# 			elif self.bIsBlocked == False and self.bIsSafe == True:
# 				if DEBUG_MODE: print("[DEBUG] can travel safely")
# # 				self.updatePlayerPosition(self.getPlayerX(),self.getPlayerY(),self.getPlayerZ())
# 				#TODO: check if destination blocked)
# 				self.aTcodMaps[self.intPlayerZ].walkable[self.intPlayerY][self.intPlayerX] = True	#NOTE: after something blocking moves, must update origin's walkability; TODO: also need to update when something dies
# 				self.aLstEntities[x][y][z].append( self.aLstEntities[self.intPlayerX][self.intPlayerY][self.intPlayerZ].pop() )	#TODO: make sure there are no weird situations which would grab not-a-Player
# 				self.intPlayerX = x
# 				self.intPlayerY = y
# 				self.intPlayerZ = z
# 				self.aTcodMaps[self.intPlayerZ].walkable[self.intPlayerY][self.intPlayerX] = False	#new location is blocked, of course
# 				if (DEBUG_MODE): print("[DEBUG] updatePlayerPosition: now at", self.getPlayerX(), self.getPlayerY(), self.getPlayerZ() )
# 	# 			self.alstObject[self.intPlayerX][self.intPlayerY].append(Player() )
# 	# 			self.aLstEntities[self.intPlayerX][self.intPlayerY][self.intPlayerZ].append
# 				self.updateFoV()
# 			else:
# 				if DEBUG_MODE: print("[DEBUG] can't travel; player position blocked in target timeline; may or may not be unsafe as well")
			if self.bIsBlocked == False:	#removed "safe-check" - felt too clunky; better to show in GUI with "could be Enemy, Item, or Portal" for tension
				if DEBUG_MODE: print("[DEBUG] can travel safely")
# 				self.updatePlayerPosition(self.getPlayerX(),self.getPlayerY(),self.getPlayerZ())
				#TODO: check if destination blocked)
				self.aTcodMaps[self.intPlayerZ].walkable[self.intPlayerY][self.intPlayerX] = True	#NOTE: after something blocking moves, must update origin's walkability; TODO: also need to update when something dies
				self.aLstEntities[x][y][z].append( self.aLstEntities[self.intPlayerX][self.intPlayerY][self.intPlayerZ].pop() )	#TODO: make sure there are no weird situations which would grab not-a-Player
				self.updateMemory()
				self.intPlayerX = x
				self.intPlayerY = y
				self.intPlayerZ = z
				self.aTcodMaps[self.intPlayerZ].walkable[self.intPlayerY][self.intPlayerX] = False	#new location is blocked, of course
				if (DEBUG_MODE): print("[DEBUG] updatePlayerPosition: now at", self.getPlayerX(), self.getPlayerY(), self.getPlayerZ() )
	# 			self.alstObject[self.intPlayerX][self.intPlayerY].append(Player() )
	# 			self.aLstEntities[self.intPlayerX][self.intPlayerY][self.intPlayerZ].append
				self.updateFoV()
			else:
				if DEBUG_MODE: print("[DEBUG] can't travel; player position blocked in target timeline; may or may not be unsafe as well")
			if DEBUG_MODE: print("[DEBUG] bIsSafe:", self.bIsSafe, "| bIsBlocked:", self.bIsBlocked)
	#END updatePlayerPosition(self, x, y, z=-1):	
		
	
	def updateMemory(self, z=-1):
		'''
		Stores (old) Player FoV in Memory.
		'''
		if (z == -1):
			z = self.getPlayerZ()
		
		for y in range(self.intHeight):
			for x in range(self.intWidth):
# 				if (self.aTcodMaps[self.getPlayerZ()].fov[y][x] == True):
				if (self.aTcodMaps[z].fov[y][x] == True):
# 					self.aSymbolMemory[x][y][self.getPlayerZ()] = self.getTopEntity(x, y).getSymbol()
					self.aSymbolMemory[x][y][z] = self.getTopEntity(x, y).getSymbol()
					self.aBoolIsExplored[x][y][z] = True
# 					if DEBUG_MODE: print("[DEBUG] updateFoV(): added", self.aSymbolMemory[x][y][z])

	def updateFoV(self, z=-1):
		'''
		Recomputes Player FoV.
		TODO: (real version) set non-intPlayerZ FoV maps to not-in-FoV
		'''
		if (z == -1):
			z = self.getPlayerZ()
					
		
		#sets non-Player-containing timeline FoVs to False
		if (self.getPlayerZ() == 0):
			for y in range(self.intHeight):
				for x in range(self.intWidth):
					self.aTcodMaps[1].fov[y][x] = False
		else:
			for y in range(self.intHeight):
				for x in range(self.intWidth):
					self.aTcodMaps[0].fov[y][x] = False
					
		#updates Player-containing timeline
		self.aTcodMaps[self.intPlayerZ].compute_fov(self.intPlayerX, self.intPlayerY, FOV_RADIUS, True, tcod.FOV_SHADOW)
	#END updateFoV(self, z=-1)
	

	'''
	Coordinate getters/setters
	'''
	def getPlayerX(self, z=-1):
		return self.intPlayerX
	
	def getPlayerY(self, z=-1):
		return self.intPlayerY
	
	def getPlayerZ(self):
		return self.intPlayerZ


	def isWalkable(self, x, y, z=-1):
		'''
		Returns walkability status (solidity) of given coordinates.
		'''
		if z == -1:
			return self.aTcodMaps[self.intPlayerZ].walkable[y][x]
		else:
			return self.aTcodMaps[z].walkable[y][x]
	#END isWalkable(self, x, y, z=-1)
	
	def isExplored(self, x, y, z=-1):
		'''
		Returns explored status (known by Player) of given coordinates.
		'''
		if z == -1:
			return self.aBoolIsExplored[x][y][self.intPlayerZ]
		else:
			return self.aBoolIsExplored[x][y][z]
	#END isExplored(self, x, y, z=-1)


	def printTileContents(self, x, y, z=-1):
		if (z == -1):
			z = self.getPlayerZ()
			
		print(x, y, z, "top =", self.getTopEntity(x, y).getName(), "| walkable =", self.aTcodMaps[z].walkable[y][x], "| FoV =", self.aTcodMaps[z].fov[y][x], "| explored =", self.aBoolIsExplored[x][y][z], "| memory =", self.aSymbolMemory[x][y][z] )
		for i in range(len(self.aLstEntities[x][y][z] ) ):
			print("\t", self.aLstEntities[x][y][z][i].getName() )


