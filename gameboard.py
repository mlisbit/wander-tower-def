#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui
import copy

from towers import *
from enemies import *

class gameBoard(QtGui.QFrame):
	boardWidth = 600
	boardHeight = 520
	blockSize = 20

	def __init__(self, parent):
		QtGui.QFrame.__init__(self, parent)
		
		self.money = 1000
		self.score = 0
		self.lives = 20

		self.mouse_x = -1
		self.mouse_y = -1

		self.enemyPath = [[0,2], [1,2], [2,2], [2,1], [2,0], [3,0], [4,0], [5,0], [5,1], [5,2], [5,3], [4,3], [3,3], [3,4], [3,5], [3,6], [3,7], [2,7], [1,7], [1,8], [1,9], [1,10], [1,11], [1,12], [1,13]]

		self.isMouseIn = False
		self.isTowerSelected = False
		self.isTowerClicked = False

		self.lastPlacedTower = Tower()

		self.towerOccupancy = []
		self.enemyOccupancy = []
		self.nonOccupiable = []

	def start(self):
		self.setStyleSheet("QWidget { background: #A9F5D0 }") 
		self.setFixedSize(self.boardWidth, self.boardHeight)
		#first_enemy.enemyPath = 
		first_enemy = Enemy(self.enemyPath[0][0], self.enemyPath[0][1], copy.deepcopy(self.enemyPath))
		
		self.enemyOccupancy.append(first_enemy)
		#self.secondaryBoard = scoreBoard()

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawGrid(qp)
		
		self.drawPath(qp)
		self.drawTowers(qp)
		if self.isTowerSelected:
			self.drawOutline(qp)
		if self.isTowerClicked:
			self.selectTower(qp, self.lastPlacedTower)
		self.drawEnemies(qp)
		qp.end()

	def drawGrid(self, qp):
		pen = QtGui.QPen(QtGui.QColor(25, 180, 40, 55), 2, QtCore.Qt.SolidLine)
		qp.setPen(pen)
		for i in range(0, 600, self.blockSize):
			qp.drawLine(i, 0, i, self.boardHeight)
			qp.drawLine(0, i, self.boardWidth, i)

	def drawEnemies(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
		for i in self.enemyOccupancy:
			qp.setBrush(i.color)
			qp.drawEllipse(i.getCenter(), i.size, i.size)

	def drawPath(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(255, 80, 100, 255))
		for i in self.enemyPath:
			qp.drawRect(i[0]*self.blockSize, i[1]*self.blockSize, 20, 20)

	def drawTowers(self, qp):
		#qp.setPen(QtCore.Qt.NoPen)
		color = QtGui.QColor(0, 0, 0)
		qp.setPen(color)
		
		for i in self.towerOccupancy:
			qp.setBrush(i.color)
			qp.drawRect(i.position_x, i.position_y, i.size*self.blockSize, i.size*self.blockSize)

	def pause(self):
		print "paused"

	#returns modified mouse co-ordinates to account for board dimensions.
	def get_x(self):
		if self.mouse_x > self.boardWidth-40 and self.lastPlacedTower.size == 2:
			return self.boardWidth-40
		return self.mouse_x

	def get_y(self):
		if self.mouse_y > self.boardHeight-40 and self.lastPlacedTower.size == 2:
			return self.boardHeight-40
		return self.mouse_y

	#draws outline on mouse hover 
	def drawOutline(self, qp):
		#self.lastPlacedTower.size = self.lastPlacedTower.size
		if self.isMouseIn:
			qp.setPen(QtCore.Qt.NoPen)
			qp.setBrush(QtGui.QColor(255, 80, 0, 155))
			qp.drawRect(self.myround(self.get_x()), self.myround(self.get_y()), self.lastPlacedTower.size*20, self.lastPlacedTower.size*20)
			qp.setBrush(QtGui.QColor(0, 0, 0, 55))
			center = QtCore.QPoint(self.myround(self.get_x()) + (self.lastPlacedTower.size*20/2), self.myround(self.get_y()) + self.lastPlacedTower.size*20/2)
			qp.drawEllipse(center, self.lastPlacedTower.shotrange, self.lastPlacedTower.shotrange)
		#checks to see if the mouse is over occupied grid.
		if not self.checkPlacement() and self.isMouseIn:
			qp.setPen(QtCore.Qt.NoPen)
			qp.setBrush(QtGui.QColor(0, 0, 0, 155))
			qp.drawRect(self.myround(self.get_x()), self.myround(self.get_y()), self.lastPlacedTower.size*20, self.lastPlacedTower.size*20)

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
		if self.lastPlacedTower.size==1:
			if [self.myround(self.get_x()),self.myround(self.get_y())] in self.nonOccupiable:
				return False
		elif self.lastPlacedTower.size==2:
			if [self.myround(self.get_x()),self.myround(self.get_y())] in self.nonOccupiable or \
				[self.myround(self.get_x()),self.myround(self.get_y())+self.blockSize] in self.nonOccupiable or \
				[self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())] in self.nonOccupiable or \
				[self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())+self.blockSize] in self.nonOccupiable:
				return False
		return True

	#called by controller: adds tower to array of towers when mouse clicked.
	def placeTowers(self):
		if self.checkPlacement() and self.isTowerSelected:
			#self.lastPlacedTower = Tower(self.myround(self.get_x()),self.myround(self.get_y()), self.currentlySelectedTower)
			self.lastPlacedTower.position_x = self.myround(self.get_x())
			self.lastPlacedTower.position_y = self.myround(self.get_y())


			if self.isMouseIn and self.money >= self.lastPlacedTower.cost:

				#self.towerOccupancy.append([self.myround(self.get_x()),self.myround(self.get_y()),self.mouse_size*self.blockSize])
				self.towerOccupancy.append(self.lastPlacedTower)
				self.isTowerSelected = False
				self.isTowerClicked = True
				self.money -= self.lastPlacedTower.cost

				if self.lastPlacedTower.size == 1:
					self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
					self.lastPlacedTower.occupied.append([self.myround(self.get_x()),self.myround(self.get_y())])
				elif self.lastPlacedTower.size == 2:
					self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
					self.nonOccupiable.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())])
					self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())+self.blockSize])
					self.nonOccupiable.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())+self.blockSize])

					self.lastPlacedTower.occupied.append([self.myround(self.get_x()),self.myround(self.get_y())])
					self.lastPlacedTower.occupied.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())])
					self.lastPlacedTower.occupied.append([self.myround(self.get_x()),self.myround(self.get_y())+self.blockSize])
					self.lastPlacedTower.occupied.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())+self.blockSize])
			else:
				self.lastPlacedTower = Tower()
				self.isTowerSelected = False
				#print "insufficeient funds"

		elif self.isMouseIn:
			for i in self.towerOccupancy:
				if [self.myround(self.get_x()),self.myround(self.get_y())] in i.getOccupied():
					print "print tower stats"
					self.lastPlacedTower = i
					self.isTowerSelected = False
					self.isTowerClicked = True
					break
				else:
					self.isTowerClicked = False
		#print self.nonOccupiable
		self.repaint()