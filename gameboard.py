#!/usr/bin/python
import sys, time, json
from PyQt4 import QtCore, QtGui
import copy

from towers import *
from enemies import *
from projectiles import *

import globals

class gameBoard(QtGui.QFrame):
	

	def __init__(self, parent):
		QtGui.QFrame.__init__(self, parent)
		self.controller = parent

		self.mouse_x = -1
		self.mouse_y = -1

		self.currentWave = 1
		self.isWaveSent = False
		self.isWaveInProgress = False

		self.graceUnits = 4

		self.NoU_sent = 0

		self.isLastWave = False
		self.isMouseIn = False
		self.isTowerSelected = False
		self.isTowerClicked = False

		self.lastPlacedTower = Tower()

		self.projectileOccupancy = []
		self.towerOccupancy = []
		self.enemyOccupancy = []
		self.nonOccupiable = []

	def start(self):
		self.setStyleSheet("QWidget { background: #A9F5D0 }") 
		self.setFixedSize(globals.boardWidth, globals.boardHeight)
		#adds the enemy path to non occupiable blocks.
		for i in globals.enemyPath:
			self.nonOccupiable.append([i[0]*globals.blockSize, i[1]*globals.blockSize])

	def pause(self):
		print "paused"

	def gameOver(self, qp):
		for i in range(len(self.enemyOccupancy)):
			self.enemyOccupancy.pop()
		for i in range(len(self.towerOccupancy)):
			self.towerOccupancy.pop()
		for i in range(len(self.nonOccupiable)):
			self.nonOccupiable.pop()

		qp.setPen(QtGui.QColor(0, 34, 3))
		qp.setFont(QtGui.QFont('Decorative', 50))
		qp.drawText(95,280, "GAME OVER!")
		self.controller.timer.stop() 

	def winner(self, qp):
		for i in range(len(self.enemyOccupancy)):
			self.enemyOccupancy.pop()
		for i in range(len(self.towerOccupancy)):
			self.towerOccupancy.pop()
		for i in range(len(self.nonOccupiable)):
			self.nonOccupiable.pop()

		qp.setPen(QtGui.QColor(0, 34, 3))
		qp.setFont(QtGui.QFont('Decorative', 50))
		qp.drawText(125,280, "WINNER!")
		self.controller.timer.stop() 

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		if globals.lives <= 0:
			self.gameOver(qp)
		elif self.isLastWave and self.enemyOccupancy.__len__() == 0:
			self.winner(qp)
		else:
			self.waveManager()
			self.drawGrid(qp)
			self.drawPath(qp)
			self.drawTowers(qp)
			self.drawProjectiles(qp)
			if self.isTowerSelected:
				self.drawOutline(qp)
			if self.isTowerClicked:
				self.selectTower(qp, self.lastPlacedTower)
			self.drawEnemies(qp)
			self.drawEnemyHP(qp)
		qp.end()

	#timed loop for moving enemies and such.
	def timedLoop(self):
		self.moveEnemies()
		self.dealDamage()

 	#determines which waves are next, how many, health, etc. Reads from waves.json
	def waveManager(self):
		json_data=open('waves.json')
		data = json.load(json_data)

		id = data["wave_"+str(self.currentWave)]["type"]
		NoU = data["wave_"+str(self.currentWave)]["units"]
		hp = int(data["wave_"+str(self.currentWave)]["HP"])
		#print "need to send", NoU, "units. sent", self.NoU_sent
		

		if self.isWaveSent and self.isWaveInProgress == False:
			#sends the first enemy

			if self.NoU_sent == 0 or len(self.enemyOccupancy) == 0: 
				self.enemyOccupancy.insert(0, getattr(sys.modules[__name__], id)(copy.deepcopy(globals.enemyPath), hp))
				self.NoU_sent += 1
			#sends enemy after certain delay
			elif self.NoU_sent < data["wave_"+str(self.currentWave)]["units"] + self.graceUnits:
				if not len(self.enemyOccupancy) == 0:
					if self.enemyOccupancy[0].position_x >= data["wave_"+str(self.currentWave)]["delay"]:
						self.enemyOccupancy.insert(0, getattr(sys.modules[__name__], id)(copy.deepcopy(globals.enemyPath), hp))
						self.NoU_sent += 1
						print self.NoU_sent
				#ending of wave
				if self.NoU_sent == data["wave_"+str(self.currentWave)]["units"]:
					self.isWaveSent = False
					self.isWaveInProgress = True
					try:
						id = data["wave_"+str(self.currentWave + 1)]["type"]
						self.currentWave += 1
						self.NoU_sent = 0
					except:
						#print "DONE", self.currentWave
						self.isLastWave = True
						self.NoU_sent = 0
		if self.isWaveInProgress and self.enemyOccupancy.__len__() == 0:
			self.isWaveInProgress = False
			self.isWaveSent = False


		json_data.close()

	def drawGrid(self, qp):
		pen = QtGui.QPen(QtGui.QColor(25, 180, 40, 55), 2, QtCore.Qt.SolidLine)
		qp.setPen(pen)
		for i in range(0, 600, globals.blockSize):
			qp.drawLine(i, 0, i, globals.boardHeight)
			qp.drawLine(0, i, globals.boardWidth, i)

	def moveEnemies(self):
		if self.towerOccupancy > 0:
			for i in self.enemyOccupancy:
				i.move()

	def drawEnemies(self, qp):
		#qp.setPen(QtCore.Qt.NoPen)
		for i in self.enemyOccupancy:
			qp.setBrush(i.color)
			qp.drawEllipse(i.getCenter(), i.size, i.size)
			if i.isFinished:
				globals.lives -= 1
		self.enemyOccupancy[:] = [tup for tup in self.enemyOccupancy if tup.isFinished == False]
		self.enemyOccupancy[:] = [tup for tup in self.enemyOccupancy if tup.isDead == False]
			

	def drawPath(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(255, 80, 100, 255))
		for i in globals.enemyPath:
			qp.drawRect(i[0]*globals.blockSize, i[1]*globals.blockSize, 20, 20)

	def drawTowers(self, qp):
		#qp.setPen(QtCore.Qt.NoPen) uncomment to not draw tower borders.
		color = QtGui.QColor(0, 0, 0)
		qp.setPen(color)
		
		for i in self.towerOccupancy:
			qp.setBrush(i.color)
			qp.drawRect(i.position_x, i.position_y, i.size*globals.blockSize, i.size*globals.blockSize)

	#returns modified mouse co-ordinates to account for board dimensions.
	def get_x(self):
		if self.mouse_x > globals.boardWidth-40 and self.lastPlacedTower.size == 2:
			return globals.boardWidth-40
		return self.mouse_x

	def get_y(self):
		if self.mouse_y > globals.boardHeight-40 and self.lastPlacedTower.size == 2:
			return globals.boardHeight-40
		return self.mouse_y

	#draws outline on mouse hover 
	def drawOutline(self, qp):
		#self.lastPlacedTower.size = self.lastPlacedTower.size
		if self.isMouseIn:
			qp.setPen(QtCore.Qt.NoPen)
			qp.setBrush(self.lastPlacedTower.getColor())
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
				[self.myround(self.get_x()),self.myround(self.get_y())+globals.blockSize] in self.nonOccupiable or \
				[self.myround(self.get_x())+globals.blockSize,self.myround(self.get_y())] in self.nonOccupiable or \
				[self.myround(self.get_x())+globals.blockSize,self.myround(self.get_y())+globals.blockSize] in self.nonOccupiable:
				return False
		return True

	#called by controller: adds tower to array of towers when mouse clicked.
	def placeTowers(self):
		if self.checkPlacement() and self.isTowerSelected:
			self.lastPlacedTower.position_x = self.myround(self.get_x())
			self.lastPlacedTower.position_y = self.myround(self.get_y())

			if self.isMouseIn and globals.money >= self.lastPlacedTower.cost:
				self.towerOccupancy.append(self.lastPlacedTower)
				self.isTowerSelected = False
				self.isTowerClicked = True
				globals.money -= self.lastPlacedTower.cost

				if self.lastPlacedTower.size == 1:
					self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
					self.lastPlacedTower.occupied.append([self.myround(self.get_x()),self.myround(self.get_y())])
				elif self.lastPlacedTower.size == 2:
					self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
					self.nonOccupiable.append([self.myround(self.get_x())+globals.blockSize,self.myround(self.get_y())])
					self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())+globals.blockSize])
					self.nonOccupiable.append([self.myround(self.get_x())+globals.blockSize,self.myround(self.get_y())+globals.blockSize])

					self.lastPlacedTower.occupied.append([self.myround(self.get_x()),self.myround(self.get_y())])
					self.lastPlacedTower.occupied.append([self.myround(self.get_x())+globals.blockSize,self.myround(self.get_y())])
					self.lastPlacedTower.occupied.append([self.myround(self.get_x()),self.myround(self.get_y())+globals.blockSize])
					self.lastPlacedTower.occupied.append([self.myround(self.get_x())+globals.blockSize,self.myround(self.get_y())+globals.blockSize])
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
	'''
	def drawProjectiles(self, qp):
		pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
		qp.setPen(pen)
		for i in self.towerOccupancy:
			for k in self.enemyOccupancy:
				if i.inRange(k):
					qp.drawLine(i.getCenter(), k.getCenter())
	'''

	def targettedEnemies(self):
		pass

	def dealDamage(self):
		for i in self.projectileOccupancy:
			i.dealDamage()
			#print "damage dealt!", i.destination.health

	def drawProjectiles(self, qp):
		pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
		qp.setPen(pen)
		self.projectileOccupancy = []
		for i in self.towerOccupancy:
			#determin targets should return an array of qpoints
			for k in i.determineTarget(self.enemyOccupancy):
				qp.drawLine(i.getCenter(), k.getCenter())
				self.projectileOccupancy.append(Projectile(i,k))

	def drawEnemyHP(self,qp):
		qp.setPen(QtGui.QColor(0, 34, 3))
		qp.setFont(QtGui.QFont('Decorative', 6))
		for i in self.enemyOccupancy:
			qp.drawText(i.getHPcoord().x(),i.getHPcoord().y(), str(i.health))
	'''
	def determineProjectiles(self):
		print "======================="
		for i in self.towerOccupancy:
			i.determineTarget(self.enemyOccupancy)
		'''

			