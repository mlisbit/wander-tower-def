#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui

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
		self.showTime(qp)
		#print "."
		qp.end()

	def start(self):
		self.setStyleSheet("QWidget { background: #A4A4A4 }") 
		self.setGeometry(600, 0, 200, 520)

		btn1 = QtGui.QPushButton("Tower 1", self)
		btn1.move(10, 50)

		btn2 = QtGui.QPushButton("Tower 2", self)
		btn2.move(110, 50)

		btn1.clicked.connect(self.towerOne)            
		btn2.clicked.connect(self.towerTwo)

	def towerOne(self):
		sender = self.sender()
		self.mainBoard.mouse_size = 1
		self.mainBoard.isTowerSelected = True

	def towerTwo(self):
		sender = self.sender()
		self.mainBoard.mouse_size = 2
		self.mainBoard.isTowerSelected = True

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