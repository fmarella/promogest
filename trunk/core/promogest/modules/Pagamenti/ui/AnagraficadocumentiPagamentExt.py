# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010
#    by Promotux di Francesco Meloni snc - http://www.promotux.it/

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

from decimal import *
from PagamentiUtils import Pagamenti
from promogest.dao.Pagamento import Pagamento
from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota
from promogest.modules.PrimaNota.dao.RigaPrimaNota import RigaPrimaNota
from promogest.modules.PrimaNota.dao.RigaPrimaNotaTestataDocumentoScadenza import RigaPrimaNotaTestataDocumentoScadenza
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from promogest.ui.utils import *

def on_pulisci_scadenza_button_clicked(anaedit,button):
    """
    Pulisce tutti i campi relativi alla tab pagamenti
    """
    msg = 'Attenzione! Stai per rimuovere i riferimenti già inseriti. Continuare?'
    procedi = YesNoDialog(msg=msg, transient=self.getTopLevel())
    if procedi:
        Pagamenti(anaedit).attiva_prima_scadenza(False,False)
        Pagamenti(anaedit).attiva_seconda_scadenza(False,False)
        Pagamenti(anaedit).attiva_terza_scadenza(False,False)
        Pagamenti(anaedit).attiva_quarta_scadenza(False,False)
        anaedit.numero_primo_documento_entry.set_text('')
        anaedit.numero_secondo_documento_entry.set_text('')
        anaedit.importo_primo_documento_entry.set_text('')
        anaedit.importo_secondo_documento_entry.set_text('')

def on_seleziona_prima_nota_button_clicked(anaedit, button):
    if anaedit.numero_primo_documento_entry.get_text() != "":
            response = Pagamenti(anaedit).impostaDocumentoCollegato(
                    int(anaedit.numero_primo_documento_entry.get_text()))
    else:
        anaedit.showMessage("Inserisci il numero del documento")
        response = False

    if response != False:
        anaedit.importo_primo_documento_entry.set_text(str(response))
        Pagamenti(anaedit).dividi_importo()
        Pagamenti(anaedit).ricalcola_sospeso_e_pagato()
        anaedit.numero_secondo_documento_entry.set_sensitive(True)
        anaedit.seleziona_seconda_nota_button.set_sensitive(True)
        anaedit.importo_secondo_documento_entry.set_sensitive(True)

def on_seleziona_seconda_nota_button_clicked(anaedit, button):
    if anaedit.numero_secondo_documento_entry.get_text() != "":
        response = Pagamenti(anaedit).impostaDocumentoCollegato(
                int(anaedit.numero_secondo_documento_entry.get_text()))
    else:
        anaedit.showMessage("Inserisci il numero del documento")
        response = False
    if response != False:
        Pagamenti(anaedit).importo_primo_documento_entry.set_text(str(response))
        Pagamenti(anaedit).dividi_importo()
        Pagamenti(anaedit).ricalcola_sospeso_e_pagato()

def nuovaRiga(anaedit):
    Pagamenti(anaedit).attiva_prima_scadenza(False, True)
    Pagamenti(anaedit).attiva_seconda_scadenza(False, True)
    Pagamenti(anaedit).attiva_terza_scadenza(False, True)
    Pagamenti(anaedit).attiva_quarta_scadenza(False, True)

def getScadenze(anaedit):
    return Pagamenti(anaedit).getScadenze()

def attiva_prima_scadenza(anaedit,False, True):
    Pagamenti(anaedit).attiva_prima_scadenza(False, True)

def attiva_seconda_scadenza(anaedit,False, True):
    """ Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della seconda scadenza """
    Pagamenti(anaedit).attiva_seconda_scadenza(False, True)

def attiva_terza_scadenza(anaedit,False, True):
    """ Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della terza scadenza """
    Pagamenti(anaedit).attiva_terza_scadenza(False, True)

def attiva_quarta_scadenza(anaedit,False, True):
    Pagamenti(anaedit).attiva_quarta_scadenza(False, True)

def saveScadenze(anaedit):
    Pagamenti(anaedit).saveScadenze()

def controlla_rate_scadenza(anaedit,True):
    Pagamenti(anaedit).controlla_rate_scadenza(True)

def attiva_scadenze(anaedit):
    """ Bottone (ri) calcola importi attiva"""
    Pagamenti(anaedit).attiva_scadenze()

def dividi_importo(anaedit):
    Pagamenti(anaedit).dividi_importo()

def ricalcola_sospeso_e_pagato(anaedit):
    """ Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della quarta scadenza """
    Pagamenti(anaedit).ricalcola_sospeso_e_pagato()

def connectEntryPag(anaedit):
    #come sempre c'è questo inutile palleggiamento
    anaedit.data_pagamento_prima_scadenza_entry.entry.connect('changed',
            anaedit.on_data_pagamento_prima_scadenza_entry_changed)
    anaedit.data_pagamento_seconda_scadenza_entry.entry.connect('changed',
            anaedit.on_data_pagamento_seconda_scadenza_entry_changed)
    anaedit.data_pagamento_terza_scadenza_entry.entry.connect('changed',
            anaedit.on_data_pagamento_terza_scadenza_entry_changed)
    anaedit.data_pagamento_quarta_scadenza_entry.entry.connect('changed',
            anaedit.on_data_pagamento_quarta_scadenza_entry_changed)

    anaedit.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(
        0)+'</span></b>')
    anaedit.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(
        0)+'</span></b>')
    anaedit.importo_primo_documento_entry.set_text('')
    anaedit.importo_secondo_documento_entry.set_text('')
    anaedit.numero_primo_documento_entry.set_text('')
    anaedit.numero_secondo_documento_entry.set_text('')

    fillComboboxPagamenti(anaedit.id_pagamento_acconto_customcombobox.combobox)
    fillComboboxPagamenti(anaedit.id_pagamento_prima_scadenza_customcombobox.combobox)
    fillComboboxPagamenti(anaedit.id_pagamento_seconda_scadenza_customcombobox.combobox)
    fillComboboxPagamenti(anaedit.id_pagamento_terza_scadenza_customcombobox.combobox)
    fillComboboxPagamenti(anaedit.id_pagamento_quarta_scadenza_customcombobox.combobox)

def on_chiudi_pagamento_documento_button_clicked(anaedit, button):
    "chiudi pagamento"
    if (anaedit.importo_prima_scadenza_entry.get_text() =="" or \
    anaedit.importo_prima_scadenza_entry.get_text() ==str(0)) and\
    (anaedit.importo_seconda_scadenza_entry.get_text() =="" or \
    anaedit.importo_seconda_scadenza_entry.get_text() ==str(0)) and\
    (anaedit.importo_terza_scadenza_entry.get_text() =="" or \
    anaedit.importo_terza_scadenza_entry.get_text() ==str(0)) and\
    (anaedit.importo_quarta_scadenza_entry.get_text() =="" or \
    anaedit.importo_quarta_scadenza_entry.get_text() ==str(0)) and\
    (anaedit.importo_acconto_scadenza_entry.get_text() =="" or \
    anaedit.importo_acconto_scadenza_entry.get_text() ==str(0)):
        msg = 'Attenzione! Stai per chiudere un documento dove non figura incassato niente.\n Continuare ?'
        procedi = YesNoDialog(msg=msg, transient=self.getTopLevel())
        if procedi:
            anaedit.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')
            anaedit.chiudi_pagamento_documento_button.set_sensitive(False)
            anaedit.apri_pagamento_documento_button.set_sensitive(True)
    else:
        anaedit.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')


def on_apri_pagamento_documento_button_clicked(anaedit, button):
    """ Riapri o apri il pagamento"""
    msg = 'Attenzione! Stai per riaprire un documento considerato già pagato.\n Continuare ?'
    procedi = YesNoDialog(msg=msg, transient=self.getTopLevel())
    if procedi:
        anaedit.stato_label.set_markup('<b><span foreground="#B40000" size="24000">APERTO</span></b>')
        anaedit.apri_pagamento_documento_button.set_sensitive(False)
        anaedit.chiudi_pagamento_documento_button.set_sensitive(True)

def on_edit_prima_rata_button_clicked(anaedit, button):
    """Attiva prima rata forando"""
    Pagamenti(anaedit).attiva_prima_scadenza(True, True)

def on_edit_seconda_rata_button_clicked(anaedit, button):
    """ Attiva seconda rata"""
    Pagamenti(anaedit).attiva_seconda_scadenza(True, True)

def on_edit_terza_rata_button_clicked(anaedit, button):
    """ Attiva terza rata"""
    Pagamenti(anaedit).attiva_terza_scadenza(True, True)

def on_edit_quarta_rata_button_clicked(anaedit, button):
    """ Attiva terza rata"""
    Pagamenti(anaedit).attiva_quarta_scadenza(True, True)

def on_edit_acconto_button_clicked(anaedit, button):
    """ Attiva terza rata"""
    Pagamenti(anaedit).attiva_acconto(True, True)

def on_pulisci_acconto_button_clicked(anaedit, button):
    anaedit.data_acconto_entry.set_text("")
    anaedit.importo_acconto_scadenza_entry.set_text("")
    anaedit.id_pagamento_acconto_customcombobox.combobox.set_active(-1)
    anaedit.data_pagamento_acconto_entry.set_text("")

def on_pulisci_prima_rata_button_clicked(anaedit, button):
    anaedit.data_prima_scadenza_entry.set_text("")
    anaedit.id_pagamento_prima_scadenza_customcombobox.combobox.set_active(-1)
    anaedit.data_pagamento_prima_scadenza_entry.set_text("")
    anaedit.importo_prima_scadenza_entry.set_text("")

def on_pulisci_seconda_rata_button_clicked(anaedit, button):
    anaedit.data_seconda_scadenza_entry.set_text("")
    anaedit.importo_seconda_scadenza_entry.set_text("")
    anaedit.id_pagamento_seconda_scadenza_customcombobox.combobox.set_active(-1)
    anaedit.data_pagamento_seconda_scadenza_entry.set_text("")

def on_pulisci_terza_rata_button_clicked(anaedit, button):
    anaedit.data_terza_scadenza_entry.set_text("")
    anaedit.importo_terza_scadenza_entry.set_text("")
    anaedit.id_pagamento_terza_scadenza_customcombobox.combobox.set_active(-1)
    anaedit.data_pagamento_terza_scadenza_entry.set_text("")

def on_pulisci_quarta_rata_button_clicked(anaedit, button):
    anaedit.data_quarta_scadenza_entry.set_text("")
    anaedit.importo_quarta_scadenza_entry.set_text("")
    anaedit.id_pagamento_quarta_scadenza_customcombobox.combobox.set_active(-1)
    anaedit.data_pagamento_quarta_scadenza_entry.set_text("")
