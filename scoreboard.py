#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui

from towers import *

class scoreBoard(QtGui.QFrame):
	'''
	THINGS TO ADD. MAYBE.
	creeps
	gold
	lives
	leaks
	kills
	LEVEL
	types of enemies
	fast forward
	pause/start
	'''
	def __init__(self, parent):
		QtGui.QFrame.__init__(self, parent)
		self.mainBoard = parent.mainBoard

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.showGameStats(qp)
		self.showTowerStats(qp)
		#print "."
		qp.end()

	def start(self):
		self.setStyleSheet("QWidget { background: #A4A4A4 }") 
		self.setGeometry(600, 0, 200, 520)

		y_off = 85
		btn1 = QtGui.QPushButton("Tower 1", self)
		btn1.move(10, y_off)

		btn2 = QtGui.QPushButton("Tower 2", self)
		btn2.move(110, y_off)

		btn3 = QtGui.QPushButton("Tower 3", self)
		btn3.move(10, y_off+30)

		btn4 = QtGui.QPushButton("Tower 4", self)
		btn4.move(110, y_off+30)

		btn1.clicked.connect(self.towerOne)            
		btn2.clicked.connect(self.towerTwo)
		btn3.clicked.connect(self.towerThree)
		btn4.clicked.connect(self.towerFour)

	def showTowerStats(self, qp):
		y_off = 150
		qp.setPen(QtGui.QColor(0, 0, 0))
		qp.setBrush(QtGui.QColor(0, 0, 0, 0))
		qp.drawRect(10, y_off, 180, 80)

		if self.mainBoard.isTowerClicked or self.mainBoard.isTowerSelected:
			qp.setPen(QtGui.QColor(0, 34, 3))
			qp.setFont(QtGui.QFont('Decorative', 10))
			qp.drawText(15,y_off+15, "DAMAGE: " + str(self.mainBoard.lastPlacedTower.damage))
			qp.drawText(15,y_off+30, "RANGE: " + str(self.mainBoard.lastPlacedTower.shotrange))
			qp.drawText(15,y_off+45, "RoF: " + str(self.mainBoard.lastPlacedTower.rof))
			qp.drawText(15,y_off+60, "VALUE: " + str(self.mainBoard.lastPlacedTower.retailvalue))
			qp.drawText(15,y_off+75, "LEVEL: " + str(self.mainBoard.lastPlacedTower.level))

	def showGameStats(self, qp):
		y_off =5
		qp.setPen(QtGui.QColor(0, 0, 0))
		qp.setBrush(QtGui.QColor(0, 0, 0, 0))
		qp.drawRect(10, y_off, 180, y_off + 70)
		qp.setPen(QtGui.QColor(0, 34, 3))
		qp.setFont(QtGui.QFont('Decorative', 10))
		qp.drawText(15,20, "MONEY: "+ str(self.mainBoard.money))

	def towerSelected(self):
		self.mainBoard.isTowerSelected = True
		self.mainBoard.isTowerClicked = False
		
	def towerOne(self):
		self.towerSelected()
		self.mainBoard.lastPlacedTower = Tower(None, None, "ONE")

	def towerTwo(self):
		self.towerSelected()
		self.mainBoard.lastPlacedTower = Tower(None, None, "TWO")

	def towerThree(self):
		self.towerSelected()
		self.mainBoard.lastPlacedTower = Tower(None, None, "THREE")

	def towerFour(self):
		self.towerSelected()
		self.mainBoard.lastPlacedTower = Tower(None, None, "FOUR")

	def buttonClicked(self):
		sender = self.sender()
		print "button was pressed", sender.text()

	def showTime(self, qp):
		qp.setPen(QtGui.QColor(0, 34, 3))
		qp.setFont(QtGui.QFont('Decorative', 10))
		qp.drawText(10,20, "GAME TICKS: ")
		#print "TIME REDRAWN!"

	def towerOptions(self, qp):
		pass