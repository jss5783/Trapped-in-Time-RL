'''
---CHANGELOG---
2019/03/27		(JSS5783)
				Created main.py.
				Hard-coded entities.
'''

from src.constants import * 

class Entity:
	def __init__(self, cInSymbol, strInName, clrInForeground, clrInBackground=None):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground
	
	def setSymbol(self, cInSymbol):
		self.cSymbol = cInSymbol
		
	def getSymbol(self):
		return self.cSymbol
	
	def setName(self, strInName):
		self.strName = strInName
	
	def getName(self):
		return self.strName

	def setFGColor(self, clrInForeground):
		self.clrForeground = clrInForeground
	
	def getFGColor(self):
		return self.clrForeground
	
	def setBGColor(self, clrInBackground):
		self.clrBackground = clrInBackground
	
	def getBGColor(self):
		return self.clrBackground
#END Entity


class Wall(Entity):
	def __init__(self, cInSymbol='#', strInName="wall", clrInForeground=WHITE, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Floor(Entity):
	def __init__(self, cInSymbol='.', strInName="floor", clrInForeground=GRAY_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Enemy(Entity):
	def __init__(self, cInSymbol='E', strInName="enemy", clrInForeground=ORANGE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Player(Entity):
	def __init__(self, cInSymbol='@', strInName="player", clrInForeground=WHITE, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class ShieldConsumable(Entity):
	def __init__(self, cInSymbol='¿', strInName="shield repair kit", clrInForeground=BLUE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class HealthConsumable(Entity):
	def __init__(self, cInSymbol='¡', strInName="medical kit", clrInForeground=BLUE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Ammo(Entity):
	def __init__(self, cInSymbol=',', strInName="pistol bullet", clrInForeground=BLUE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Portal(Entity):
	def __init__(self, cInSymbol='*', strInName="portal", clrInForeground=BLUE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class GateOpen(Entity):
	def __init__(self, cInSymbol='_', strInName="gate (open)", clrInForeground=BLACK, clrInBackground=BLUE_LIGHT):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class GateClosed(Entity):
	def __init__(self, cInSymbol='=', strInName="gate (closed)", clrInForeground=BLACK, clrInBackground=BLUE_LIGHT):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

