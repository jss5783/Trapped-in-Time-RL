'''
---CHANGELOG---
2019/03/29		(JSS5783)
				MessageLog.py created.
				Can add messages, which get split into separate lines as needed.
				Can print messages to message log.
'''

import tcod
from src.constants import *


class MessageLog:
	def __init__(self):
		self.intWidth = MESSAGE_WIDTH
		self.intHeight = MESSAGE_HEIGHT
		self.alstMessageLog = []	#store strings in here
		print(type(self.alstMessageLog))
# 		self.alstMessageLog.append("Test String 1")
# 		self.alstMessageLog.append("The quick brown fox jumped over the lazy dog.")
		self.addMessage("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()")		#really long test message
		#eventually: Messages with colors


	def addMessage(self, strInNewMessage):
		#TODO: trim log once in a while to delete old messages (maybe use a sentinel value)
# 		self.alstMessage.remove
		if len(strInNewMessage) > MESSAGE_WIDTH:	#if message is too long to fit onto one line, then hard-split it for now
			self.intLines = len(strInNewMessage) // MESSAGE_WIDTH	#not using Python's ceiling function because (https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python). While effectively 0% probability of this problem occurring in a roguelike, why not?
			if (len(strInNewMessage) % MESSAGE_WIDTH > 0):	#if has remainder
				self.intLines += 1	#add extra line
			for i in range(self.intLines):
				intMessageStart = i * MESSAGE_WIDTH
				intMessageEnd = (i + 1) * MESSAGE_WIDTH
				self.alstMessageLog.append(strInNewMessage[intMessageStart:intMessageEnd])
				print(self.alstMessageLog[len(self.alstMessageLog) - 1])
# 			self.alstMessageLog.append(strInNewMessage[0:MESSAGE_WIDTH])
# 			print(self.alstMessageLog[self.alstMessageLog.__len__() - 1])
# # 			self.alstMessageLog.append(strInNewMessage[MESSAGE_WIDTH:MESSAGE_WIDTH+strInNewMessage.__len__()])
# 			self.alstMessageLog.append(strInNewMessage[MESSAGE_WIDTH:MESSAGE_WIDTH+MESSAGE_WIDTH])
# 			self.alstMessageLog.append(strInNewMessage[MESSAGE_WIDTH+MESSAGE_WIDTH:strInNewMessage.__len__()])
# 			print(self.alstMessageLog[self.alstMessageLog.__len__() - 1])
# 			print(self.alstMessageLog[0])
# 			print(self.alstMessageLog[1])
		else:
			self.alstMessageLog.append(strInNewMessage)
	
	
	def printLog(self, inConsole):
		#take most recent string. how long? split according to intWidth, count # of resulting lines.
		#print from bottom up, I guess.
		y = 0
		for i in range(self.alstMessageLog.__len__()):
			tcod.console_print(inConsole, MAP_WIDTH - MESSAGE_WIDTH, MAP_HEIGHT + y, self.alstMessageLog[i])
			y += 1
	# 			console, 0, MAP_HEIGHT, tcod.BKGND_NONE, tcod.LEFT, "(" + str(mouse.cx) + "," + str(mouse.cy) + "): " + map1.alstObject[mouse.cx][mouse.cy][map1.top(mouse.cx, mouse.cy)].getName() + "   ")
	# 			print("message log:", MAP_WIDTH, MAP_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT, self.alstMessageLog[i])

'''
	LOG:
		1
		2
		3
	oldLog[] = LOG
	newMessage[]: abc (too long for 1 line)
	log[] = oldLog + newMessage.split
		log is new/rewritten every time function is called
	if log.len <= 5
		print from 0 to 4
	else
		print from log.len - 4 to log.len - 1
'''