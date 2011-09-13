#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#
# iTerminal : Le Terminal Intuitif
# completion.py
# Copyright (C) Intuitive 2009 <projet_fe@yahoo.com>
#
#
#
# iTerminal is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iTerminal is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import os


class Completion:
	def __init__ (self, location):
		self.location = location
	
	def getList (self, path):
		lst = []
		
		tmp = self.getFromPath (path)
		for i in tmp:
			lst.append (i)

		tmp = self.getFromBash ()
		for i in tmp:
			lst.append (i)

		tmp = self.getFromCWD ()
		for i in tmp:
			lst.append (i)

		lst.sort()
		return lst

	def getFromPath (self, path):
		lst = []
		
		chemin_executable = path.split(":")
		for chemin in chemin_executable:
			list_executable = os.listdir(chemin)
			for i in list_executable:
				lst.append (i)
		return lst

	def getFromCWD (self):
		lst = []
		
		liste_fichier = os.listdir(os.getcwd())
		for i in liste_fichier:
			lst.append (i)
		return lst

	def getFromBash (self):
		lst = []
		
		f = open (os.path.join (self.location, "bash.txt"))
		for line in f:
			lst.append (line.split()[0])
		f.close()
		return lst
