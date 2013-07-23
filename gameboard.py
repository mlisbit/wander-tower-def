#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui

from towers import *

class gameBoard(QtGui.QFrame):
	boardWidth = 600
	boardHeight = 520
	blockSize = 20

	def __init__(self, parent):
		QtGui.QFrame.__init__(self, parent)
		
		self.mouse_size = 2
		self.score = 0
		self.mouse_x = -1
		self.mouse_y = -1
	
		self.gameTime = 0

		self.enemyPath = [[0,2], [1,2], [2,2], [3,2], [4,2], [4,3], [4,4], [4,5], [4,6], [4,7], [4,8], [4,9], [4,10]]

		self.isMouseIn = False
		self.towerSelected = True
		self.isTowerSelected = False
		self.lastPlacedTower = Tower()

		self.towerOccupancy = []
		self.nonOccupiable = []

	def start(self):
		self.setStyleSheet("QWidget { background: #A9F5D0 }") 
		self.setFixedSize(self.boardWidth, self.boardHeight)
		#self.secondaryBoard = scoreBoard()

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawGrid(qp)
		self.drawEnemies(qp)
		self.drawPath(qp)
		self.drawTowers(qp)
		if self.isTowerSelected:
			self.drawOutline(qp)
		if self.towerSelected:
			self.selectTower(qp, self.lastPlacedTower)
		#self.secondaryBoard.repaint()
		#print "!"
		qp.end()

	def drawGrid(self, qp):
		pen = QtGui.QPen(QtGui.QColor(25, 180, 40, 55), 2, QtCore.Qt.SolidLine)
		qp.setPen(pen)
		for i in range(0, 600, self.blockSize):
			qp.drawLine(i, 0, i, self.boardHeight)
			qp.drawLine(0, i, self.boardWidth, i)

	def drawEnemies(self, qp):
		pass

	def drawPath(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(255, 80, 100, 255))
		for i in self.enemyPath:
			qp.drawRect(i[0]*self.blockSize, i[1]*self.blockSize, 20, 20)

	def drawTowers(self, qp):
		#qp.setPen(QtCore.Qt.NoPen)
		color = QtGui.QColor(0, 0, 0)
		qp.setPen(color)
		qp.setBrush(QtGui.QColor(255, 80, 0, 255))
		for i in self.towerOccupancy:
			qp.drawRect(i.position_x, i.position_y, i.size, i.size)

	def pause(self):
		print "paused"

	#returns modified mouse co-ordinates to account for board dimensions.
	def get_x(self):
		if self.mouse_x > self.boardWidth-40 and self.mouse_size == 2:
			return self.boardWidth-40
		return self.mouse_x

	def get_y(self):
		if self.mouse_y > self.boardHeight-40 and self.mouse_size == 2:
			return self.boardHeight-40
		return self.mouse_y

	#draws outline on mouse hover 
	def drawOutline(self, qp):
		if self.isMouseIn:
			qp.setPen(QtCore.Qt.NoPen)
			qp.setBrush(QtGui.QColor(255, 80, 0, 155))
			qp.drawRect(self.myround(self.get_x()), self.myround(self.get_y()), self.mouse_size*20, self.mouse_size*20)
		#checks to see if the mouse is over occupied grid.
		if not self.checkPlacement() and self.isMouseIn:
			qp.setPen(QtCore.Qt.NoPen)
			qp.setBrush(QtGui.QColor(0, 0, 0, 155))
			qp.drawRect(self.myround(self.get_x()), self.myround(self.get_y()), self.mouse_size*20, self.mouse_size*20)

	def selectTower(self, qp, t):
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(0, 0, 0, 55))
		qp.drawEllipse(t.getCenter(), t.shotrange, t.shotrange)


	#rounds to base, for positioning of towers and outlines
	def myround(self, x, base=20):
		return x - (x%base)

	#called by controller: updates the value of mouse positions
	def updateMouse(self, x, y):
		self.mouse_y = y
		self.mouse_x = x
		#print x, y
		self.repaint()

	#returns true if current mouse pointer/size is able to be placed.
	def checkPlacement(self):
		if self.mouse_size==1:
			if [self.myround(self.get_x()),self.myround(self.get_y())] in self.nonOccupiable:
				return False
		elif self.mouse_size==2:
			if [self.myround(self.get_x()),self.myround(self.get_y())] in self.nonOccupiable or \
				[self.myround(self.get_x()),self.myround(self.get_y())+self.blockSize] in self.nonOccupiable or \
				[self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())] in self.nonOccupiable or \
				[self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())+self.blockSize] in self.nonOccupiable:
				return False
		return True

	#called by controller: adds tower to array of towers when mouse clicked.
	def placeTowers(self):
		#print self.isMouseIn
		if self.checkPlacement() and self.isTowerSelected:
			if self.isMouseIn:
				self.lastPlacedTower = Tower(self.myround(self.get_x()),self.myround(self.get_y()),self.mouse_size*self.blockSize)
				#self.towerOccupancy.append([self.myround(self.get_x()),self.myround(self.get_y()),self.mouse_size*self.blockSize])
				self.towerOccupancy.append(self.lastPlacedTower)
				self.isTowerSelected = False

			if self.mouse_size == 1:
				self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
				self.lastPlacedTower.occupied.append([self.myround(self.get_x()),self.myround(self.get_y())])
			elif self.mouse_size == 2:
				self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
				self.nonOccupiable.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())])
				self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())+self.blockSize])
				self.nonOccupiable.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())+self.blockSize])

				self.lastPlacedTower.occupied.append([self.myround(self.get_x()),self.myround(self.get_y())])
				self.lastPlacedTower.occupied.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())])
				self.lastPlacedTower.occupied.append([self.myround(self.get_x()),self.myround(self.get_y())+self.blockSize])
				self.lastPlacedTower.occupied.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())+self.blockSize])
		elif self.isMouseIn:
			print "Unplaceable Tower!"
			for i in self.towerOccupancy:
				if [self.myround(self.get_x()),self.myround(self.get_y())] in i.getOccupied():
					print "print tower stats"
					self.lastPlacedTower = i
					self.isTowerSelected = False
					break
		#print self.nonOccupiable
		self.repaint()