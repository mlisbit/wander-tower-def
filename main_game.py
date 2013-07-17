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

	def mousePressEvent(self, e):
		self.mainBoard.updateTowers()

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.MouseMove:
			if event.buttons() == QtCore.Qt.NoButton and str(source).find("gameBoard") > 0:
 				pos = event.pos()
 				#print pos.x(), pos.y()
 				#self.edit.setText('x: %d, y: %d' % (pos.x(), pos.y()))
 				self.mainBoard.updateMouse(2, pos.x(), pos.y())
 				self.mainBoard.isMouseIn = True
			else:
				self.mainBoard.isMouseIn = False
				self.mainBoard.repaint()
		return QtGui.QMainWindow.eventFilter(self, source, event)
	

class gameBoard(QtGui.QFrame):
	boardWidth = 600
	boardHeight = 520
	blockSize = 20

	mouse_x = -1;
	mouse_y = -1;
	mouse_size = 1;

	isMouseIn = False;
	towerOccupancy = []
	nonOccupiable = []

	def start(self):
		self.setStyleSheet("QWidget { background: #A9F5D0 }") 
		self.setFixedSize(self.boardWidth, self.boardHeight)

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawGrid(qp)
		self.drawEnemies(qp)
		
		self.drawTowers(qp)
		self.drawOutline(qp)
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
		pass

	def drawTowers(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(255, 80, 0, 255))
		for i in self.towerOccupancy:
			qp.drawRect(i[0], i[1], i[2], i[2])

	def pause(self):
		print "paused"

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
		if not self.checkPlacement():
			qp.setPen(QtCore.Qt.NoPen)
			qp.setBrush(QtGui.QColor(0, 0, 0, 155))
			qp.drawRect(self.myround(self.get_x()), self.myround(self.get_y()), self.mouse_size*20, self.mouse_size*20)

	#rounds to base, for positioning of towers and outlines
	def myround(self, x, base=20):
		return x - (x%base)

	#called by controller: updates the value of mouse positions
	def updateMouse(self, size, x, y):
		self.mouse_size = size
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
	def updateTowers(self):
		#print self.isMouseIn
		if self.checkPlacement():
			if self.isMouseIn:
				self.towerOccupancy.append([self.myround(self.get_x()),self.myround(self.get_y()),self.mouse_size*self.blockSize])
			if self.mouse_size == 1:
				self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
			elif self.mouse_size == 2:
				self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
				self.nonOccupiable.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())])
				self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())+self.blockSize])
				self.nonOccupiable.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())+self.blockSize])
		else:
			print "Unplaceable Tower!"
		#print self.nonOccupiable
		self.repaint()

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
