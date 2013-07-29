#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui

class Enemy(object):
	
	
	def __init__(self, x=None, y=None, ep=None):
		self.enemyPath = ep
		self.health = 100
		self.speed = 2

		self.size = 8
		self.grace_offset = self.size + 2

		self.color = QtGui.QColor(25, 80, 100, 255)
		
		self.position_x = 10
		self.position_y = 50

		self.current_block = [x,y]
		self.direction = "RIGHT"

	def move(self):
		if self.direction == "RIGHT":
			self.position_x += self.speed
		elif self.direction == "DOWN":
			self.position_y += self.speed
		elif self.direction == "LEFT":
			self.position_x -= self.speed
		elif self.direction == "UP":
			self.position_y -= self.speed

		temp = self.current_block
		self.current_block = self.getCurrentBlock()

		if temp != self.getCurrentBlock():
			print "shit needs to go down"
			header = self.enemyPath.pop(0)
			if self.enemyPath[1] != self.getFutureBlock():
				print "TURN REQUIRED!"
				print self.getCurrentBlock()
				print self.enemyPath[1]
				if self.getCurrentBlock()[1] < self.enemyPath[1][1]:
					print "TURN DOWN!"
					self.direction = "DOWN"
				elif self.getCurrentBlock()[1] > self.enemyPath[1][1]:
					print "TURN UP!"
					self.direction = "UP"
				elif self.getCurrentBlock()[0] < self.enemyPath[1][0]:
					print "TURN RIGHT!"
					self.direction = "RIGHT"
				elif self.getCurrentBlock()[0] > self.enemyPath[1][0]:
					print "TURN LEFT!"
					self.direction = "LEFT"


		#print "current block", self.current_block
		#print "future block", self.getFutureBlock()

	def getCurrentBlock(self):
		#print self.position_x, self.position_y
		current_x = ((self.position_x) - (self.position_x)%20)/20
		current_y = ((self.position_y) - (self.position_y)%20)/20
		return [current_x, current_y]
		#return x - (x%base)

	def getFutureBlock(self):
		if self.direction	== "RIGHT":
			return [self.getCurrentBlock()[0]+1,self.getCurrentBlock()[1]]
		elif self.direction	== "LEFT":
			return [self.getCurrentBlock()[0]-1,self.getCurrentBlock()[1]]
		elif self.direction	== "UP":
			return [self.getCurrentBlock()[0],self.getCurrentBlock()[1]-1]
		elif self.direction	== "DOWN":
			return [self.getCurrentBlock()[0],self.getCurrentBlock()[1]+1]
		return None

	def getCenter(self):
		return QtCore.QPoint(self.position_x, self.position_y)
