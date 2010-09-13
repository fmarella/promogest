# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
# License GNU Gplv2

import locale
import gtk, gobject
import hashlib
import os
from  subprocess import *
import threading, os, signal
from promogest import Environment
from GladeWidget import GladeWidget
from ElencoMagazzini import ElencoMagazzini
from ElencoListini import ElencoListini
from VistaPrincipale import VistaPrincipale
from promogest.ui.SendEmail import SendEmail
from utils import hasAction,fenceDialog
from utilsCombobox import *
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
                self.vbox1.pack_start(module_button, False, False)
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

        from AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)


    def on_forniture_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)


    def on_clienti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)


    def on_fornitori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaFornitori import AnagraficaFornitori
        anag = AnagraficaFornitori(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)


    def on_vettori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaVettori import AnagraficaVettori
        anag = AnagraficaVettori(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)

    def on_agenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if "Agenti" or "pan" in Environment.modulesList:
            from promogest.modules.Agenti.ui.AnagraficaAgenti import AnagraficaAgenti
            anag = AnagraficaAgenti(aziendaStr=self.aziendaStr)
            showAnagrafica(self.mainWindow, anag, toggleButton)
        else:
            fenceDialog()
            toggleButton.set_active(False)


    #def on_contatti_button_clicked(self, toggleButton):
        #if toggleButton.get_property('active') is False:
            #return

        #from AnagraficaContatti import AnagraficaContatti
        #anag = AnagraficaContatti(aziendaStr=self.aziendaStr)

        #showAnagrafica(self.mainWindow, anag, toggleButton)

def on_anagrafica_destroyed(anagrafica_window, argList):
    mainWindow = argList[0]
    anagraficaButton= argList[1]
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