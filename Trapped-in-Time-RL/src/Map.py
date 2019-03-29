'''
---CHANGELOG---
2019/03/29		(JSS5783)
				Partially-implemented addObject. 
				
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
from builtins import map

'''
Contains map-relevant data (visibility mapping, etc.).
'''
class Map:
	
	def __init__(self, intInMapWidth, intInMapHeight, pathMap="", aObjMap=[]):
		self.intWidth = intInMapWidth
		self.intHeight = intInMapHeight
		self.intPlayerX = -1	#TODO: better location/error marker
		self.intPlayerY = -1
		
		self.abIsKnown = [[bool(False) for y in range(self.intHeight)] for x in range(self.intWidth)]	#explored
		self.abIsVisible = [[bool(False) for y in range(self.intHeight)] for x in range(self.intWidth)]	#in FoV
		self.abIsSolid = [[bool(False) for y in range(self.intHeight)] for x in range(self.intWidth)]	#can enter?
		if (pathMap != ""):
			self.alstObject = self.loadMap(pathMap, MAP_WIDTH, MAP_HEIGHT)	#formerly aObj
			print("Map loaded!")
		else:
			self.alstObject = [[list() for y in range(self.intHeight)] for x in range(self.intWidth)]			#entities
			for y in range(self.intHeight):
				for x in range(self.intWidth):
					self.alstObject[x][y].append(Floor() )
# 			self.alstObject[intPlayerX][intPlayerY].append("@")	#TODO: replace
			self.updatePlayerPosition(MAP_WIDTH // 2, MAP_HEIGHT // 2)
			
			print("Map created!")
# 		print("[Map.__init__(self, intInMapWidth, intInMapHeight, aObjMap=[], pathMap=\"\")]", self.alstObject[1][2][self.top(1, 2)])	#x, y, object (list) index
	#END __init__(self, intInMapWidth, intInMapHeight, pathMap="", aObjMap=[])


	'''
	Returns value at top of list (generally player/monster/wall/portal, assuming a stack of floor+item+player, but if none exist, then something like an item probably)
	Otherwise, return floor tile.
	'''
	def top(self, x, y):
# 		print("len=",len(self.alstObject[x][y]))
		if len(self.alstObject[x][y]) > 0:
			return len(self.alstObject[x][y]) - 1
		else:
			return 0
	#END top(self, x, y)
	
	'''
	Returns value at "bottom" of list (generally item, assuming a stack of floor+item+player, but if no items exist, then something like a player/monster/wall/portal probably)
	'''
	def bottom(self, x, y):
		if len(self.alstObject[x][y]) > 0:
			return 1
		else:
			return 0	#returns value for floor (tile is empty)


	def isEmptyTile(self, x, y):
		if len(self.alstObject[x][y]) > 1:
			return False
		else:	#floor-only (tile is empty)
			return True
		
	
	'''
		Adds entInEntity to map1[x, y], placing it in the stack where necessary.
		TODO: handle "player/enemy/wall/gate (open/closed)/portal replacing other 'top'-placed entity"
		For now, if 'top' and 'top', nothing, 'middle' appends on top of middle, and 'top' on 'top'-less middle.
			Other conditions, like 'bottom' and 'bottom' nothing are NOT handled.
	'''
	def addObject(self, entInEntity, x, y):
		self.intEntityPlacement = self.top(x, y)
		print("is",type(entInEntity))
		if (isinstance(entInEntity, Player) or isinstance(entInEntity, Enemy) or isinstance(entInEntity, Wall) or isinstance(entInEntity, GateClosed) or isinstance(entInEntity, GateOpen) or isinstance(entInEntity, Portal) ):
			self.bIsInTopObject = True
		else:
			self.bIsInTopObject = False
		if (isinstance(self.alstObject[x][y][self.top(x, y)], Player) or isinstance(self.alstObject[x][y][self.top(x, y)], Enemy) or isinstance(self.alstObject[x][y][self.top(x, y)], Wall) or isinstance(self.alstObject[x][y][self.top(x, y)], GateClosed) or isinstance(self.alstObject[x][y][self.top(x, y)], GateOpen) or isinstance(self.alstObject[x][y][self.top(x, y)], Portal) ):	
			self.bHasCurrentTopObject = True
		else:
			self.bHasCurrentTopObject = False
		if (self.bIsInTopObject == False and self.bHasCurrentTopObject == True):
			print("non-top-level entity " + entInEntity.getName() + " inserted above " + self.alstObject[x][y][self.top(x, y)].getName() )
			self.alstObject[x][y].insert(self.top(x, y) - 1, entInEntity)
		elif (not self.bHasCurrentTopObject):
			print("entity " + entInEntity.getName() + " inserted above " + self.alstObject[x][y][self.top(x, y)].getName() )
# 			self.alstObject[x][y].insert(self.top(x, y), entInEntity)
			self.alstObject[x][y].append(entInEntity)


	'''
	Loads map from file.
	Returns resulting map (aList).
	TODO: handle enemies, etc. so can pass to Map constructor.
	'''
	def loadMap(self, pathMap, intMapWidth, intMapHeight):
		try:
			self.fileMap = codecs.open(pathMap, encoding="utf-8")	#must use utf-8 or else "•" is read as "â€¢"
			self.strCurrentLine = ""
# 			print("file open!")
# 			aMap = [[list(Floor() ) for y in range(intMapHeight)] for x in range(intMapWidth)]	#just auto-fill everything with a floor underneath
			self.aMap = [[list() for y in range(intMapHeight)] for x in range(intMapWidth)]
			for y in range(intMapHeight):
				self.strCurrentLine = self.fileMap.readline()
# 				print(self.strCurrentLine)
# 				strCurrentLine = reader.readline()
				for x in range(intMapWidth):
					if (self.strCurrentLine[x] == "."):
						self.aMap[x][y].append(Floor() )
					elif (self.strCurrentLine[x] == "@"):
						self.aMap[x][y].append(Floor() )	#add Floor beneath Player
						self.aMap[x][y].append(Player() )
						self.intPlayerX = x
						self.intPlayerY = y
					elif (self.strCurrentLine[x] == "E"):
						self.aMap[x][y].append(Floor() )
						self.aMap[x][y].append(Enemy() )
					elif (self.strCurrentLine[x] == "I"):	#place random item
# 						if (rng.randint(0,2) == 0):
# 							aMap[x][y].append(self.strCurrentLine[HealthConsumable() ] )
# 						elif (rng.randint(0,2) == 1):
# 							aMap[x][y].append(self.strCurrentLine[ShieldConsumable() ] )
# 						elif (rng.randint(0,2) == 2):
# 							aMap[x][y].append(self.strCurrentLine[Ammo() ] )
						self.aMap[x][y].append(Floor() )
						self.aMap[x][y].append(HealthConsumable() )
					elif (self.strCurrentLine[x] == "*"):
						self.aMap[x][y].append(Floor() )
						self.aMap[x][y].append(Portal() )
					elif (self.strCurrentLine[x] == "_"):
						self.aMap[x][y].append(Floor() )
						self.aMap[x][y].append(GateOpen() )
					elif (self.strCurrentLine[x] == "="):
						self.aMap[x][y].append(Floor() )
						self.aMap[x][y].append(GateClosed() )
					else:	#assuming that blank space/errors should all be Walls for now
						self.aMap[x][y].append(Floor() )
						self.aMap[x][y].append(Wall() )
# 					if not (self.strCurrentLine[x] == "."):			#TODO: instead of plain char, add Floor? 
# 						aMap[x][y].append(self.strCurrentLine[x])	#TODO: instead of plain char, add entity; if (char = "m": add Monster)
# 						if (self.strCurrentLine[x] == "@"):
# 							self.intPlayerX = x
# 							self.intPlayerY = y
# 						if (self.strCurrentLine[x] != "." & self.strCurrentLine[x] != "#"):
# 							print(self.strCurrentLine[x] != ".")
# 					print(aMap[x][y])
			self.fileMap.close()
			return self.aMap
		finally:
			self.fileMap.close()
			
		
	def updatePlayerPosition(self, x, y):
		print("test")
# 		if (self.alstObject[self.intPlayerX][self.intPlayerY][self.top(x, y)] == "@"):
# 		self.alstObject[self.intPlayerX][self.intPlayerY].remove("@")
		for i in range(len(self.alstObject[x][y]) ):
			print(self.alstObject[x][y])
		
# 		self.alstObject[x][y].append(Player() )
		self.alstObject[self.intPlayerX][self.intPlayerY].pop()	#TODO: make sure there are no weird situations which would grab not-a-Player
		self.intPlayerX = x
		self.intPlayerY = y
# 		self.alstObject[self.intPlayerX][self.intPlayerY].append("@")
		self.alstObject[self.intPlayerX][self.intPlayerY].append(Player() )