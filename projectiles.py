#!/usr/bin/python

import sys, time
from PyQt4 import QtCore, QtGui

import globals

class Projectile(object):
	def __init__(self, origin, destination):
		size = 1
		#the tower that shot the projectile
		self.origin = origin
		#the enemy/enemies the projectile is headed toward.
		self.destination = destination

		self.rof = self.origin.rof

	def move(self):
		pass

	def dealDamage(self):
		self.destination.health -= self.origin.damage

