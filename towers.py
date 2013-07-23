#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui

#tower objects 
class Tower(object):
	def __init__(self, x=-100, y=-100, t="ONE"): 
		self.position_x = x
		self.position_y = y
		self.occupied = []
		self.retailvalue = 1000
		self.level = 1

		if t=="ONE":
			self.type1()
		elif t=="TWO":
			self.type2()
		elif t=="THREE":
			self.type3()
		elif t=="FOUR":
			self.type4()

	def type1(self):
		self.size = 1
		self.shotrange = 120
		self.cost = 200
		self.damage = 100
		self.rof = 5

	def type2(self):
		self.size = 2
		self.shotrange = 320
		self.cost = 200
		self.damage = 200
		self.rof = 1
	def type3(self):
		self.size = 2
		self.shotrange = 160
		self.cost = 200
		self.damage = 200
		self.rof = 1
	def type4(self):
		self.size = 2
		self.shotrange = 100
		self.cost = 200
		self.damage = 200
		self.rof = 1

	def getCenter(self):
		#print self.size
		return QtCore.QPoint(self.position_x + (self.size*20/2), self.position_y + self.size*20/2)

	def getOccupied(self):
		return self.occupied

	def getRange(self):
		return self.shotrange

	def getLevel(self):
		return self.level