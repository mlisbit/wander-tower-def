#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui


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

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_P:
			self.mainBoard.pause()

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.MouseMove:
			if event.buttons() == QtCore.Qt.NoButton and str(source).find("gameBoard") > 0:
 				pos = event.pos()
 				print pos.x(), pos.y()
 				#self.edit.setText('x: %d, y: %d' % (pos.x(), pos.y()))
			else:
				pass # do other stuff
		return QtGui.QMainWindow.eventFilter(self, source, event)
	

class gameBoard(QtGui.QFrame):
	boardWidth = 600
	boardHeight = 520
	blockSize = 20
	boardOccupancy = [[0,0]]
	startPosition = [0,0]

	def start(self):
		self.setStyleSheet("QWidget { background: #A9F5D0 }") 
		self.setFixedSize(self.boardWidth, self.boardHeight)

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawGrid(qp)
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
		qp.setBrush(QtGui.QColor(255, 80, 0, 255))
		qp.drawRect(0, 0, 40, 40)
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(225, 180, 40, 255))
		qp.drawRect(0, 0, 20, 20)

	def drawPath(self, qp):
		pass

	def pause(self):
		print "paused"

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
	def start(self):
		self.setStyleSheet("QWidget { background: #A4A4A4 }") 
		self.setGeometry(600, 0, 200, 520)


app = QtGui.QApplication(sys.argv)
towerdef = TowerDefence()
towerdef.show()
app.installEventFilter(towerdef)

sys.exit(app.exec_())
