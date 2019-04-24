'''
---CHANGELOG---
2019/04/23		(JSS5783)
				Updated some constructors with defaults.

2019/04/20		(Bryan)
				Changed Blaster ammo to a class variable instead of instance variable for level up purposes
				
2019/04/18		(JSS5783)
				Modified FistoKit to not use coordinates.

2019/04/16		(Bryan)
				Updated Item classes (Blaster, Shield, and Fisto Kit) as needed
				Updated Player and Enemy classes enough for item testing (may need further updating)
				
2019/04/05		(JSS5783)
				Finished reworking code. Creating a new Entity type in code is simpler now.

2019/03/29		(JSS5783)
				Added strict typing as a test.

2019/03/27		(JSS5783)
				Created main.py.
				Hard-coded entities.
'''


from src.constants import *


class Entity:
	#TODO: Might add coordinates back to Entity later, along with getters/setters.
	def __init__(self, intInX, intInY, intInZ, cInSymbol='?', strInName="UNDEFINED (please report to developers)", clrInForeground=MAGENTA_DARK, clrInBackground=GREEN_DARK, bInIsSolid=True, bInIsTranslucent=False):
		'''
			Entity constructor.
			Uses ear-searing default colors to help identify generation errors.
		'''
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground
		self.bIsSolid = bInIsSolid
		self.bIsTransparent = bInIsTranslucent
		self.intX = intInX
		self.intY = intInY
		if (intInZ == -1):		#TODO: get Player Z	
			self.intX = 1
		else:
			self.intZ = intInZ
		
	#END __init__(self, cInSymbol='?', strInName="UNDEFINED (please report to developers)", clrInForeground=MAGENTA_DARK, clrInBackground=GREEN_DARK, bInIsSolid=True, bInIsTranslucent=False)
	
	
	def setSymbol(self, cInSymbol):
		'''
		Set Entity symbol.
		The symbol is the character used to represent an Entity on the screen, and must be found in CP437 (https://en.wikipedia.org/wiki/Code_page_437).
		'''
		self.cSymbol = cInSymbol
	#END setSymbol(self, cInSymbol)
		
	def getSymbol(self):
		'''
		Get Entity symbol.
		The symbol is the character used to represent an Entity on the screen.
		'''
		return self.cSymbol
	#END getSymbol(self)
	
	
	def setName(self, strInName):
		'''
		Set Entity name.
		'''
		self.strName = strInName
	#END setName(self, strInName)
	
	def getName(self):
		'''
		Get Entity name.
		'''
		return self.strName
	#END getName(self)


	def setFGColor(self, clrInForeground):
		'''
		Set Entity foreground color (text color).
		'''
		self.clrForeground = clrInForeground
	#END setFGColor(self, clrInForeground)
	
	def getFGColor(self):
		'''
		Get Entity foreground color (text color).
		'''
		return self.clrForeground
	#END getFGColor(self)
	
	
	def setBGColor(self, clrInBackground):
		'''
		Set Entity background color (color behind text).
		'''
		self.clrBackground = clrInBackground
	#END setBGColor(self, clrInBackground)
	
	def getBGColor(self):
		'''
		Get Entity background color (color behind text).
		'''
		return self.clrBackground
	#END getBGColor(self)
	
	
	def setX(self, intInX):
		'''
		Set Entity x-coordinate.
		'''
		self.intX = intInX
	#END setX(self, intInX)
	
	def getX(self):
		'''
		Get Entity x-coordinate.
		'''
		return self.intX
	#END getX(self)
	
	
	def setY(self, intInY):
		'''
		Set Entity y-coordinate.
		'''
		self.intY = intInY
	#END setY(self, intInY)
	
	def getY(self):
		'''
		Get Entity y-coordinate.
		'''
		return self.intY
	#END getY(self)
	
	
	def setZ(self, intInZ):
		'''
		Set Entity z-coordinate.
		'''
		self.intZ = intInZ
	#END setZ(self, intInZ)
	
	def getZ(self):
		'''
		Get Entity z-coordinate.
		'''
		return self.intZ
	#END getZ(self)
#END Entity


class Wall(Entity):
	def __init__(self, intInX, intInY, intInZ):
		super().__init__(intInX, intInY, intInZ, '#', "wall", WHITE, BLACK, True, False)
#END Wall(Entity)


class Floor(Entity):
	def __init__(self, intInX, intInY, intInZ):
		super().__init__(intInX, intInY, intInZ, '.', "floor", GRAY_LIGHT, BLACK, False, True)
#END Floor(Entity)


class Enemy(Entity):
	def __init__(self, intInX, intInY, intInZ, intInMaxHealth=4):
		super().__init__(intInX, intInY, intInZ, 'E', "enemy", ORANGE_LIGHT, BLACK, True, True)
		self.hp = intInMaxHealth
#END Enemy(Entity)


class Player(Entity):
	def __init__(self, intInX, intInY, intInZ, maxHp=1, damage=0):
		super().__init__(intInX, intInY, intInZ, '@', "player", WHITE, BLACK, True, True)
		self.maxHp = maxHp
		self.currentHp = maxHp
		self.damage = damage
#END Player(Entity)


# class ShieldConsumable(Entity):
# 	def __init__(self):
# 		super().__init__('¿', "shield repair kit", BLUE_LIGHT, BLACK, False, True)
# #END ShieldConsumable(Entity)


# class HealthConsumable(Entity):
# 	def __init__(self):
# 		super().__init__('¡', "medical kit", BLUE_LIGHT, BLACK, False, True)
# #END HealthConsumable(Entity)


# class Ammo(Entity):
# 	def __init__(self):
# 		super().__init__(',', "pistol bullet", BLUE_LIGHT, BLACK, False, True)
# #END Ammo(Entity)


class Shield(Entity):
	def __init__(self, intInX, intInY, intInZ, currentCharges, maxCharges):
		super().__init__(intInX, intInY, intInZ, '¿', "Shield", BLUE_LIGHT, BLACK, False, True)
		self.x = intInX
		self.y = intInY
		self.currentCharges = currentCharges
		self.maxCharges = maxCharges


class FistoKit(Entity):
# 	def __init__(self, x, y, charges=2, maxCharges=2, damage=5):
	def __init__(self, intInX, intInY, intInZ, currentCharges=2, maxCharges=2, damage=5):
		'''
		Melee weapon.
		'''
		super().__init__(intInX, intInY, intInZ, '¡', "Fisto Kit", BLUE_LIGHT, BLACK, False, True)
		self.currentCharges = currentCharges
		self.maxCharges = maxCharges
		self.damage = damage


class Blaster(Entity):
	def __init__(self, intInX, intInY, intInZ, maxAmmo=4, damage=2):
		'''
		Ranged weapon.
		'''
		super().__init__(intInX, intInY, intInZ, ',', "Blaster", BLUE_LIGHT, BLACK, False, True)
		self.maxAmmo = maxAmmo
		self.currentAmmo = maxAmmo
		self.damage = damage


class Portal(Entity):
	'''
	Level's end.
	'''
	def __init__(self, intInX, intInY, intInZ):
		super().__init__(intInX, intInY, intInZ, '☼', "portal", GREEN_LIGHT, BLACK, True, True)
#END Portal(Entity)


class GateOpen(Entity):
	'''
	Open state of gate.
	'''
	def __init__(self, intInX, intInY, intInZ):
		super().__init__(intInX, intInY, intInZ, '▬', "gate (open)", BLUE_LIGHT, BLACK, False, True) 
#END GateOpen(Entity)


class GateClosed(Entity):
	'''
	Closed state of gate.
	'''
	def __init__(self, intInX, intInY, intInZ):
		super().__init__(intInX, intInY, intInZ, '╬', "gate (closed)", BLACK, ORANGE_LIGHT, True, False)
#END GateClosed(Entity)
