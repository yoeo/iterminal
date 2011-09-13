#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#
# iTerminal : Le Terminal Intuitif
# iTerminal.py
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



import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

import os
from subprocess import *
import sys

from outils.completion import Completion

COL_TEXT = 0
class iTerminal:
	"""
	Les objets de l'ui:
	<objet> - <liste des evenements>
	
	fenetre - quitter
	commande - valider
	reponse
	aide
	aide_region
	interrupteur_aide - aide_visibilite
	"""
	# Les fonctions automatiques pour charger et gérer Glade
	# Pour appeller un élément "element" de Glade il suffit de taper self["element"]
	def __init__ (self):
		self.Widgets = gtk.glade.XML (os.path.join (sys.path[0], "outils", "interface.glade"),"fenetre")
		self.AutoConnect ()
		self.AideVisible = True
		self.completion = None
		self.nombre = 0

		self.proposition = Completion (os.path.join (sys.path[0], "outils"))
		self.Completion ()

		

	def __getitem__ (self, key):
		return self.Widgets.get_widget(key)

	def AutoConnect(self):
		eventHandlers = {}
		for (itemName, value) in self.__class__.__dict__.items():
			if callable(value) and itemName.startswith('ui_'):
				eventHandlers[itemName[3:]] = getattr(self,itemName) 
		self.Widgets.signal_autoconnect(eventHandlers)

	# Les gestionnaires d'évenements
	# Lorsqu'un évenement est définit comme "evenement" dans l'interface,
	# son gestionnaire doit s'appeler "ui_evenement (self, source = None, event = None)"
	def ui_quitter (self, source = None, event = None):
		gtk.main_quit()

	def ui_valider (self, source = None, event = None):
		texte = self["commande"].get_text ()
		reponse = self.Executer (texte)[0]
		self["commande"].set_text ("")
		tampon = self["reponse"].get_buffer()
		tampon.set_text(reponse, len(reponse))

	def ui_aide_visibilite (self, source = None, event = None):
		if (self.AideVisible):
			self.AideVisible = False
			self["aide_section"].hide()
			self["interrupteur_aide"].set_label("Afficher l'aide")
		else:
			self.AideVisible = True
			self["aide_section"].show()
			self["interrupteur_aide"].set_label("Cacher l'aide")

	def ui_bouton_appuye (self, source = None, event = None):
		commande = self["commande"].get_text ()
		if len (commande) <= 0:
			return
		if commande[len (commande) - 1] == ' ':
			self.AfficherAide (commande)
				
	def ui_dossier_selectionne (self, source = None, event = None):
		dossier = self["dossier"].get_current_folder ()
		if os.path.exists (dossier):
			os.chdir (dossier)
			self.Completion_MiseAJour ()

	def ui_raccourcis_gcc (self, source = None, event = None):
		self.LanceUtil ("gcc")

	def ui_raccourcis_gpp (self, source = None, event = None):
		self.LanceUtil ("g++")

	def ui_raccourcis_jav (self, source = None, event = None):
		self.LanceUtil ("javac")

	def ui_raccourcis_pyt (self, source = None, event = None):
		os.execv ("/usr/bin/gnome-terminal",["gnome-terminal", "/usr/bin/python"])

	def ui_raccourcis_flex (self, source = None, event = None):
		self.LanceUtil ("flex")

	def ui_raccourcis_bis (self, source = None, event = None):
		self.LanceUtil ("bison")

	def LanceUtil (self, util):
		commande = util + " "
		self["commande"].set_text(commande)
		self["commande"].set_position(-1)

	def AfficherAide (self, text):
		liste_cmd = text.split (' ')
		liste_cmd.reverse ()
		for i in liste_cmd:
			if i == "" or i == " ":
				continue
			(aide, statut) = self.Executer ("man " + i)
			if statut == 0:
				tampon = self["aide"].get_buffer()
				tampon.set_text(aide, len(aide))
				return
		aide = "L'aide n'est pas disponible pour cette commande"
		tampon = self["aide"].get_buffer()
		# print "LUTF : ", gobject.utf8_validate (aide)
		tampon.set_text(aide, len(aide))
		
	def Completion (self):
		self.completion = gtk.EntryCompletion()
		self.completion.set_match_func (self.Completion_Match)
		
		self.completion.connect ("match-selected", self.Completion_Match_Signal)
		model = gtk.ListStore (str)
		self.completion.set_model (model)
		self.completion.set_text_column (COL_TEXT)
		self["commande"].set_completion (self.completion)
		
		self.Completion_MiseAJour ()
		
	def Completion_MiseAJour (self):
		model = self.completion.get_model ()
		model.clear ()

		(path, statut) = self.Executer ("echo $PATH")
		listCommande = self.proposition.getList (path.replace("\n",""))
		for i in listCommande:
			model.append([i])

	def Completion_Match (self, completion, key, iter):
		mot_incomplet = self.RecupereMot ()
		if mot_incomplet == "" or mot_incomplet == " ":
			return False
		else:
			model = completion.get_model()
			return model[iter][COL_TEXT].startswith(mot_incomplet)
	
	def Completion_Match_Signal (self, completion, model, iter):
		liste = self["commande"].get_text ().split (' ')
		commande = ""
		if len (liste) > 0:
			for i in range (len (liste) - 1):
				commande += liste[i] + " "
		commande += model[iter][COL_TEXT]
		self["commande"].set_text(commande)
		self["commande"].set_position(-1)
		return True
	
	def RecupereMot (self):
		texte = self["commande"].get_text ()
		liste = texte.split (' ')
		if len (liste) > 0:
			return liste[len (liste) - 1]
		else:
			return ""
		
	def Executer (self, commande):
		pipe = Popen(commande, shell=True, cwd=None, env=None, stdout=PIPE, stderr=STDOUT)
		(reponse, erreur) = pipe.communicate(input=input)
		if erreur:
			reponse = "Des Erreurs ont été rencontrées durant l'exécution"
		if not reponse:
			reponse = ""

		statut = pipe.returncode
		return (reponse, statut)

if __name__ == '__main__':
	app = iTerminal()
	gtk.main()

