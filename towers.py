#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui
from math import sqrt
from enemies import *

#tower objects 
class Tower(object):
	def __init__(self): 
		self.position_x = -100
		self.position_y = -100
		self.occupied = []
		self.retailvalue = 1000
		self.level = 1

	def getColor(self):
		return self.color

	def getCenter(self):
		#print self.size
		return QtCore.QPoint(self.position_x + (self.size*20/2), self.position_y + self.size*20/2)

	def getOccupied(self):
		return self.occupied

	def getRange(self):
		return self.shotrange

	def getLevel(self):
		return self.level

	def inRange(self, enemy):
		return int(sqrt( pow((self.getCenter().x() - enemy.getCenter().x()), 2)+ pow((self.getCenter().y() - enemy.getCenter().y()), 2) )) <= self.shotrange

	def determineTarget(self, targets):
		print "hi"
		print targets
		new_targets = []
		#get the target with largest distance
		for i in targets:
			if self.inRange(i):
				print i.getTotalDistance()
				new_targets.append(i.getCenter())
		try:
			new_targets.pop()
		except:
			pass
		return new_targets

class PinkTower(Tower):
	def __init__(self):
		super(PinkTower, self).__init__()
		self.color = QtGui.QColor(255, 80, 100, 255)
		self.name = "mini helper"
		self.size = 1
		self.shotrange = 120
		self.cost = 200
		self.damage = 100
		self.rof = 5


class GreenTower(Tower):
	def __init__(self):
		super(GreenTower, self).__init__()
		self.color = QtGui.QColor(0, 200, 100, 255)
		self.name = "gargatuan"
		self.size = 2
		self.shotrange = 200
		self.cost = 200
		self.damage = 200
		self.rof = 1

class PurpleTower(Tower):
	def __init__(self):
		super(PurpleTower, self).__init__()
		self.color = QtGui.QColor(25, 180, 10, 255)
		self.size = 2
		self.shotrange = 160
		self.cost = 200
		self.damage = 200
		self.rof = 1

class BlueTower(Tower):
	def __init__(self):
		super(BlueTower, self).__init__()
		self.color = QtGui.QColor(55, 80, 100, 255)
		self.size = 2
		self.shotrange = 100
		self.cost = 200
		self.damage = 200
		self.rof = 1