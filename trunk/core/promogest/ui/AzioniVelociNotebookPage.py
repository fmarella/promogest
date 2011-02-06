# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import gtk
from promogest.ui.utils import *
from promogest.dao.Setconf import SetConf
from promogest import Environment
from GladeWidget import GladeWidget

class AzioniVelociNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn, aziendaa):
        GladeWidget.__init__(self, 'azioni_veloci_frame',
                                    'azioni_veloce_notebook.glade')
#        self.placeWindow(self.getTopLevel())
        self.rowBackGround = None
        self.main_wind = mainnn
        print "SEEEEEELF MAIN;", self.main_wind, mainnn
        self.aziendaStr = aziendaa or ""

    def draw(self):
        return self

    def on_nuovo_articolo_button_clicked(self, widget):
        if not hasAction(actionID=8):return
        from AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_cliente_button_clicked(self, widget):
        if not hasAction(actionID=11):return
        from AnagraficaClienti import AnagraficaClienti
        print dir(self), self
        anag = AnagraficaClienti(self.main_wind.aziendaStr)
        showAnagrafica(self.main_wind.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_fornitore_button_clicked(self, widget):
        if not hasAction(actionID=11):return
        from AnagraficaFornitori import AnagraficaFornitori
        anag = AnagraficaFornitori(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_promemoria_button_clicked(self, widget):
        if not hasAction(actionID=11):return
        from AnagraficaPromemoria import AnagraficaPromemoria
        anag = AnagraficaPromemoria(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_contatto_button_clicked(self, widget):
        if not hasAction(actionID=11):return
        from promogest.modules.Contatti.ui.AnagraficaContatti import AnagraficaContatti
        anag = AnagraficaContatti(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_fattura_vendita_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Fattura vendita")

    def on_nuovo_fattura_acquisto_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Fattura acquisto")

    def on_nuovo_ddt_vendita_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT vendita")

    def on_nuovo_ddt_acquisto_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT acquisto")

    def on_nuovo_ddt_reso_da_cliente_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT reso da cliente")

    def on_nuovo_ddt_reso_a_fornitore_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT reso a fornitore")

    def on_nota_di_credito_a_cliente_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Nota di credito a cliente")

    def on_nota_di_credito_a_fornitore_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Nota di credito da fornitore")

    def on_fattura_accompagnatoria_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Fattura accompagnatoria")

    def on_nuovo_preventivo_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Preventivo")

    def on_nuovo_ordine_da_cliente_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Ordine da cliente")

    def on_nuovo_vendita_al_dettaglio_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Vendita dettaglio")

    def nuovoDocumento(self, kind):
        if not hasAction(actionID=2):return
        from AnagraficaDocumenti import AnagraficaDocumenti
        #from utils import findComboboxRowFromStr
#        self.aziendaStr = Environment.azienda
        anag = AnagraficaDocumenti()
        showAnagrafica(self.main_wind.getTopLevel(), anag)
        anag.on_record_new_activate()
        findComboboxRowFromStr(anag.editElement.id_operazione_combobox, kind, 1)
        anag.editElement.id_persona_giuridica_customcombobox.grab_focus()
        findComboboxRowFromStr(anag.editElement.id_persona_giuridica_customcombobox, "Altro", 1)

    def on_promotux_button_clicked(self, button):
        url ="http://www.promotux.it"
        webbrowser.open_new_tab(url)

    def on_promogest_button_clicked(self, button):
        url ="http://www.promogest.me"
        webbrowser.open_new_tab(url)

    def on_email_button_clicked(self, button):
        sendemail = SendEmail()

def showAnagrafica(window, anag, button=None, mainClass=None):
    anagWindow = anag.getTopLevel()
#    anagWindow.connect("destroy", on_anagrafica_destroyed, [window, button,mainClass])
    #anagWindow.connect("hide", on_anagrafica_destroyed, [window, button,mainClass])
#    anagWindow.set_transient_for(window)
#    setattr(anagWindow, "mainClass",mainClass)
    anagWindow.show_all()
