# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

import locale
import hashlib
import os
from  subprocess import *
import threading, os, signal
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.ElencoMagazzini import ElencoMagazzini
from promogest.ui.ElencoListini import ElencoListini
from promogest.ui.VistaPrincipale import VistaPrincipale
from promogest.ui.SendEmail import SendEmail
from promogest.lib.utils import hasAction, fenceDialog
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *
import Login


class AnagrafichePrincipaliFrame(GladeWidget):
    """ Frame per la gestione delle anagrafiche principali """

    def __init__(self, mainWindow, azs, modules=None):
        self.mainWindow = mainWindow
        self.aziendaStr = azs
        self.modules = modules
        GladeWidget.__init__(self, 'anagrafiche_principali_select_frame',
                            fileName='_anagrafiche_principali_select.glade' )
        self.setModulesButtons()

    def setModulesButtons(self):
        if self.modules is not None:
            for module in self.modules.iteritems():
                module_button = gtk.Button()
                module_butt_image = gtk.Image()
                module_butt_image.set_from_file(module[1]['guiDir']+'/'+module[1]['module'].VIEW_TYPE[2])
                module_button.set_image(module_butt_image)
                module_button.set_label(module[1]['module'].VIEW_TYPE[1])
                module_button.connect('clicked', self.on_module_button_clicked)
                self.anagrafiche_moduli_vbox.pack_start(module_button, False, False, 0)
            return
        else:
            return

    def on_module_button_clicked(self, button):
        label = button.get_label()
        for mk in self.modules.iteritems():
            module = mk[1]['module']
            if label == module.VIEW_TYPE[1]:
                #chiave di tutto il richiamo di passaggio alla classe in module.py che poi fa la vera istanza"
                anag = module.getApplication()
                showAnagrafica(self.mainWindow, anag, button=None)

    def on_articoli_button_clicked(self, toggleButton):
        if not hasAction(actionID=2): return
        if toggleButton.get_property('active') is False:
            return

        from promogest.ui.anagArti.AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)


    def on_forniture_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from promogest.ui.anagForniture.AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)


    def on_clienti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from promogest.ui.anagClienti.AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)


    def on_fornitori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from promogest.ui.anagFornitori.AnagraficaFornitori import AnagraficaFornitori
        anag = AnagraficaFornitori(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)


    def on_vettori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from promogest.ui.anagVettori.AnagraficaVettori import AnagraficaVettori
        anag = AnagraficaVettori(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)

    def on_agenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if posso("AG"):
            from promogest.ui.anagAgenti.AnagraficaAgenti import AnagraficaAgenti
            anag = AnagraficaAgenti(aziendaStr=self.aziendaStr)
            showAnagrafica(self.mainWindow, anag, toggleButton)
        else:
            fenceDialog()
            toggleButton.set_active(False)

def on_anagrafica_destroyed(anagrafica_window, argList):
    mainWindow = argList[0]
    anagraficaButton = argList[1]
    mainClass = argList[2]
    if anagrafica_window in Environment.windowGroup:
        Environment.windowGroup.remove(anagrafica_window)
    if anagraficaButton is not None:
        anagraficaButton.set_active(False)
    if mainClass is not None:
        mainClass.on_button_refresh_clicked()

def showAnagrafica(window, anag, button=None, mainClass=None):
    anagWindow = anag.getTopLevel()
    anagWindow.connect("destroy", on_anagrafica_destroyed, [window, button,mainClass])
    #anagWindow.connect("hide", on_anagrafica_destroyed, [window, button,mainClass])
    anagWindow.set_transient_for(window)
    anagWindow.show_all()
