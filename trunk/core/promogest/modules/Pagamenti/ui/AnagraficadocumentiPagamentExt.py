# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/

# Author: Francesco Meloni  <francesco@promotux.it>

from PagamentiUtils import Pagamenti

def on_pulisci_scadenza_button_clicked(anaedit,button):
    """
    Pulisce tutti i campi relativi alla tab pagamenti
    """
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
            print "on_seleziona_prima_nota: response = ", response
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
    Pagamenti(anaedit).attiva_scadenze()

def dividi_importo(anaedit):
    Pagamenti(anaedit).dividi_importo()

def ricalcola_sospeso_e_pagato(anaedit):
    """ Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della quarta scadenza """
    Pagamenti(anaedit).ricalcola_sospeso_e_pagato()

def connectEntryPag(anaedit):
    Pagamenti(anaedit).connectEntryPag()
