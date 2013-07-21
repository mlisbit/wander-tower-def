#!/usr/bin/python
import sys, time
from PyQt4 import QtCore, QtGui


class TowerDefence(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.setFixedSize(800,520)
		self.setWindowTitle('Dat Tower Defence!')
		TowerDefence.mainBoard = gameBoard(self)
		self.secondaryBoard = scoreBoard(self)

		self.setCentralWidget(self.mainBoard)
		
		TowerDefence.mainBoard.start()
		self.secondaryBoard.start()

		TowerDefence.mainBoard.mouse_size = 2

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

#tower objects 
class Tower(object):
	position_x = 0
	position_y = 0
	size = 0
	shotrange = 50

	def __init__(self, x, y, s): 
		self.position_x = x
		self.position_y = y
		self.size = s

class Enemy(object):
	health = 100


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

		self.isMouseIn = False;
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
		self.drawOutline(qp)
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
		if self.checkPlacement():
			if self.isMouseIn:
				#self.towerOccupancy.append([self.myround(self.get_x()),self.myround(self.get_y()),self.mouse_size*self.blockSize])
				self.towerOccupancy.append(Tower(self.myround(self.get_x()),self.myround(self.get_y()),self.mouse_size*self.blockSize))
			if self.mouse_size == 1:
				self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
			elif self.mouse_size == 2:
				self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())])
				self.nonOccupiable.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())])
				self.nonOccupiable.append([self.myround(self.get_x()),self.myround(self.get_y())+self.blockSize])
				self.nonOccupiable.append([self.myround(self.get_x())+self.blockSize,self.myround(self.get_y())+self.blockSize])
		elif self.isMouseIn:
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
		TowerDefence.mainBoard.mouse_size = 1

	def towerTwo(self):
		sender = self.sender()
		TowerDefence.mainBoard.mouse_size = 2

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

app = QtGui.QApplication(sys.argv)
towerdef = TowerDefence()
towerdef.show()
app.installEventFilter(towerdef)

sys.exit(app.exec_())
