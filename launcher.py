#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui

from enemies import *
from towers import *
from scoreboard import *
from gameboard import *


class TowerDefence(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.setFixedSize(800,520)
		self.setWindowTitle('Dat Tower Defence!')
		self.mainBoard = gameBoard(self)
		self.secondaryBoard = scoreBoard(self)

		self.setCentralWidget(self.mainBoard)
		
		self.mainBoard.start()
		self.secondaryBoard.start()

		self.mainBoard.mouse_size = 2

		self.timer = QtCore.QBasicTimer()
		self.timer.start(200, self)
		self.update()

	#game thread
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			self.repaint()
		else:
			QtGui.QFrame.timerEvent(self, event)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_P:
			self.mainBoard.pause()
	
	def mousePressEvent(self, event):
		self.mainBoard.placeTowers()

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.MouseMove:
			if event.buttons() == QtCore.Qt.NoButton and str(source).find("gameBoard") > 0:
 				pos = event.pos()
 				#print pos.x(), pos.y()
 				#self.edit.setText('x: %d, y: %d' % (pos.x(), pos.y()))
 				self.mainBoard.updateMouse(pos.x(), pos.y())
 				self.mainBoard.isMouseIn = True
			else:
				self.mainBoard.isMouseIn = False
				self.mainBoard.repaint()
		return QtGui.QMainWindow.eventFilter(self, source, event)


app = QtGui.QApplication(sys.argv)
towerdef = TowerDefence()
towerdef.show()
app.installEventFilter(towerdef)

sys.exit(app.exec_())
