# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Alceste Scalas  <alceste@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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


class ParametriFrame(GladeWidget):
    """ Frame per la gestione delle anagrafiche minori """

    def __init__(self, mainWindow, azs, parent=None, modules=None):
        self.mainWindow = mainWindow
        self.mainClass=parent
        self.modules = modules
        GladeWidget.__init__(self, 'parametri_select_frame',
                                    fileName='_parametri_select.glade')
        self.setModulesButtons()

    def setModulesButtons(self):
        if self.modules:
            rows = self.table10.get_property('n_rows')
            #self.table10.resize(rows, 3)
            current_row = 0
            current_column = 2
            for module in self.modules.iteritems():
                if current_row > rows:
                    print "Impossibile aggiungere altri bottoni al frame."
                    print "Sono stati inseriti %s bottoni" % str(rows)
                    print "ne restano %s" % str(len(self.modules) - rows)
                    break
                module_button = gtk.Button()
                module_butt_image = gtk.Image()
                module_butt_image.set_from_file(module[1]['guiDir']+'/'+module[1]['module'].VIEW_TYPE[2])
                module_button.set_image(module_butt_image)
                module_button.set_label(module[1]['module'].VIEW_TYPE[1])
                module_button.connect('clicked', self.on_module_button_clicked)
                self.table10.attach(module_button,current_column, current_column+1,\
                                                current_row,current_row+1,
                                                xoptions=GTK_ATTACHOPTIONS_EXPAND|GTK_ATTACHOPTIONS_FILL,\
                                                yoptions=GTK_ATTACHOPTIONS_FILL)
                current_row += 1
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

    def on_aliquote_iva_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaAliquoteIva import AnagraficaAliquoteIva
        anag = AnagraficaAliquoteIva()

        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)

    def on_imballaggi_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaImballaggi import AnagraficaImballaggi
        anag = AnagraficaImballaggi()

        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)


    def on_utenti_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if ("RuoliAzioni" in Environment.modulesList) or \
                ("FULL" in Environment.modulesList):
            from promogest.modules.RuoliAzioni.ui.AnagraficaUtenti import AnagraficaUtenti
            anag = AnagraficaUtenti()
            showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)
        else:
            fencemsg()
            toggleButton.set_property('active',False)

    def on_ruoli_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if ("RuoliAzioni" in Environment.modulesList) or \
                ("FULL" in Environment.modulesList):
            from promogest.modules.RuoliAzioni.ui.AnagraficaRuoli import AnagraficaRuoli
            anag = AnagraficaRuoli()
            showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)
        else:
            fencemsg()
            toggleButton.set_property('active',False)

    def on_ruoli_azioni_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if ("RuoliAzioni" in Environment.modulesList) or \
                ("FULL" in Environment.modulesList):
            from promogest.modules.RuoliAzioni.ui.ManageRoleAction import ManageRuoloAzioni
            anag = ManageRuoloAzioni()
            showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)
        else:
            toggleButton.set_property('active',False)
            fencemsg()

    def on_multipli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaMultipli import AnagraficaMultipli
        anag = AnagraficaMultipli()

        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)


    def on_categorie_articoli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
        anag = AnagraficaCategorieArticoli()

        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)


    def on_famiglie_articoli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
        anag = AnagraficaFamiglieArticoli()
        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)

    def on_categorie_clienti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaCategorieClienti import AnagraficaCategorieClienti
        anag = AnagraficaCategorieClienti()
        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)


    def on_categorie_fornitori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaCategorieFornitori import AnagraficaCategorieFornitori
        anag = AnagraficaCategorieFornitori()
        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)

    def on_stadio_commessa_button_toggled(self, button):
        if toggleButton.get_property('active') is False:
            return
        from promogest.modules.GestioneCommessa.ui import AnagraficaStadioCommessa
        anag = AnagraficaStadioCommessa()

        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)

    def on_pagamenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaPagamenti import AnagraficaPagamenti
        anag = AnagraficaPagamenti()

        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)


    def on_banche_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaBanche import AnagraficaBanche
        anag = AnagraficaBanche()

        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)


    def on_categorie_contatti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from promogest.modules.Contatti.ui.AnagraficaCategorieContatti import AnagraficaCategorieContatti
        anag = AnagraficaCategorieContatti()

        showAnagrafica(self.mainWindow, anag, toggleButton, self.mainClass)

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
