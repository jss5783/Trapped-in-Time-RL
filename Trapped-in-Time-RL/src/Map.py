'''
---CHANGELOG---
2019/03/22		(JSS5783)
				Map.py created and related functions.
'''

import tcod, numpy
from src.constants import *
from idlelib.iomenu import encoding
import codecs

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
					self.alstObject[x][y].append(".")
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
		
	
# 	def addItem(self, x, y):
# 		#check if top object is wall/player/monster/etc
# 		#if yes, then insert (top - 1) ((or copy-save old (top - 1) value, overwrite, and then append old value
# 		#else append


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
			aMap = [[list(".") for y in range(intMapHeight)] for x in range(intMapWidth)]
			for y in range(intMapHeight):
				self.strCurrentLine = self.fileMap.readline()
# 				print(self.strCurrentLine)
# 				strCurrentLine = reader.readline()
				for x in range(intMapWidth):
					if not (self.strCurrentLine[x] == "."):			#TODO: instead of plain char, add Floor? 
						aMap[x][y].append(self.strCurrentLine[x])	#TODO: instead of plain char, add entity; if (char = "m": add Monster)
						if (self.strCurrentLine[x] == "@"):
							self.intPlayerX = x
							self.intPlayerY = y
# 						if (self.strCurrentLine[x] != "." & self.strCurrentLine[x] != "#"):
# 							print(self.strCurrentLine[x] != ".")
# 					print(aMap[x][y])
			self.fileMap.close()
			return aMap
		finally:
			self.fileMap.close()
			
		
	def updatePlayerPosition(self, x, y):
# 		if (self.alstObject[self.intPlayerX][self.intPlayerY][self.top(x, y)] == "@"):
		self.alstObject[self.intPlayerX][self.intPlayerY].remove("@")
		self.intPlayerX = x
		self.intPlayerY = y
		self.alstObject[self.intPlayerX][self.intPlayerY].append("@")