#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui

#tower objects 
class Tower(object):
	def __init__(self, x=-100, y=-100, s=0): 
		self.position_x = x
		self.position_y = y
		self.size = s
		self.occupied = []
		self.shotrange = 120

	def getCenter(self):
		#print self.size
		return QtCore.QPoint(self.position_x + (self.size/2), self.position_y + self.size/2)

	def getOccupied(self):
		return self.occupied

	def getRange(self):
		return self.shotrange