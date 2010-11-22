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

import gtk
from decimal import *
from PagamentiUtils import Pagamenti
from promogest.dao.Pagamento import Pagamento
from promogest.dao.TestataPrimaNota import TestataPrimaNota
from promogest.dao.RigaPrimaNota import RigaPrimaNota
from promogest.dao.RigaPrimaNotaTestataDocumentoScadenza import RigaPrimaNotaTestataDocumentoScadenza
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from promogest.ui.utils import leggiOperazione, dateToString, stringToDate, messageInfo, pbar

def on_pulisci_scadenza_button_clicked(anaedit,button):
    """
    Pulisce tutti i campi relativi alla tab pagamenti
    """
    msg = 'Attenzione! Stai per rimuovere i riferimenti già inseriti. Continuare?'
    dialog = gtk.MessageDialog(anaedit.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_YES:
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
    """ Bottone (ri) calcola importi attiva"""
    Pagamenti(anaedit).attiva_scadenze()

def dividi_importo(anaedit):
    Pagamenti(anaedit).dividi_importo()

def ricalcola_sospeso_e_pagato(anaedit):
    """ Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della quarta scadenza """
    Pagamenti(anaedit).ricalcola_sospeso_e_pagato()

def connectEntryPag(anaedit):
    Pagamenti(anaedit).connectEntryPag()

def on_primanota_button_clicked(anaedit, button):
    """ Funzione un po' complessa per l'nserimento dei dati pagamento in
    in prima nota cassa """
    #preleviamo i dati e controlliamo se esistono righe di prima nota
    msg = """ATTENZIONE, si sta per salvare le informazioni dei pagamenti
nella prima nota cassa.
E' meglio fare questa operazione dopo aver premuto "APPLICA"
per salvare il documento o le sue modifiche.
Il processo non "aggiorna" le precedenti "parti di pagamento"
eventualmente già inserite in prima nota ma aggiunge solo le nuove, per cui
se si son variate delle informazioni di pagamento rate o acconti
e si vuole aggiornare la prima nota si deve andare nella prima nota
che le contiene e rimuoverle manualmente e poi rilanciare questa procedura.
CONTINUARE?"""
    dialog = gtk.MessageDialog(anaedit.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_YES:
#        pbar(anaedit.pbar,parziale=1, totale=5)

        if anaedit.importo_acconto_scadenza_entry.get_text() and \
                            anaedit.data_pagamento_acconto_entry.get_text():
            accontoDao0= TestataDocumentoScadenza().select(idTestataDocumento=anaedit.dao.id, numeroScadenza=0)
            if accontoDao0:
                idpag0=  accontoDao0[0].id
                r = RigaPrimaNotaTestataDocumentoScadenza().select(idTestataDocumentoScadenza = idpag0)
                if r:
                    rpn = RigaPrimaNota().getRecord(id= r[0].id_riga_prima_nota)
                    if rpn:
                        messageInfo(msg = "RIGA ACCONTO GIA' INSERITA CORRETTAMENTE")
                else:
                    idrigapn = creaRigaPrimaNota(anaedit,numero_paga=0)
                    creaRigaPrimaNotaTestataDocScad(idrigapn,idpag0)
            else:
                messageInfo(msg= "PREMERE PRIMA APPLICA PER SALVARE IL DOCUMENTO ED I PAGAMENTI")
#        pbar(anaedit.pbar,parziale=2, totale=5)
        if anaedit.importo_prima_scadenza_entry.get_text() and \
                            anaedit.data_pagamento_prima_scadenza_entry.get_text():
            accontoDao1= TestataDocumentoScadenza().select(idTestataDocumento=anaedit.dao.id, numeroScadenza=1)
            if accontoDao1:
                idpag1=  accontoDao1[0].id
                r = RigaPrimaNotaTestataDocumentoScadenza().select(idTestataDocumentoScadenza = idpag1)
                if r:
                    rpn = RigaPrimaNota().getRecord(id= r[0].id_riga_prima_nota)
                    if rpn:
                        messageInfo(msg = "RIGA PRIMA RATA GIA' INSERITA CORRETTAMENTE")
                else:
                    idrigapn = creaRigaPrimaNota(anaedit,numero_paga=1)
                    creaRigaPrimaNotaTestataDocScad(idrigapn,idpag1)
            else:
                messageInfo(msg= "PREMERE PRIMA APPLICA PER SALVARE IL DOCUMENTO ED I PAGAMENTI")
#        pbar(anaedit.pbar,parziale=3, totale=5)
        if anaedit.importo_seconda_scadenza_entry.get_text() and \
                            anaedit.data_pagamento_seconda_scadenza_entry.get_text():
            accontoDao2= TestataDocumentoScadenza().select(idTestataDocumento=anaedit.dao.id, numeroScadenza=2)
            if accontoDao2:
                idpag2=  accontoDao2[0].id
                r = RigaPrimaNotaTestataDocumentoScadenza().select(idTestataDocumentoScadenza = idpag2)
                if r:
                    rpn = RigaPrimaNota().getRecord(id= r[0].id_riga_prima_nota)
                    if rpn:
                        messageInfo(msg = "RIGA SECONDA RATA GIA' INSERITA CORRETTAMENTE")
                else:
                    idrigapn = creaRigaPrimaNota(anaedit,numero_paga=2)
                    creaRigaPrimaNotaTestataDocScad(idrigapn,idpag2)
            else:
                messageInfo(msg= "PREMERE PRIMA APPLICA PER SALVARE IL DOCUMENTO ED I PAGAMENTI")

#        pbar(anaedit.pbar,parziale=4, totale=5)
        if anaedit.importo_terza_scadenza_entry.get_text() and \
                            anaedit.data_pagamento_terza_scadenza_entry.get_text():
            accontoDao3= TestataDocumentoScadenza().select(idTestataDocumento=anaedit.dao.id, numeroScadenza=3)
            if accontoDao3:
                idpag3=  accontoDao3[0].id
                r = RigaPrimaNotaTestataDocumentoScadenza().select(idTestataDocumentoScadenza = idpag3)
                if r:
                    rpn = RigaPrimaNota().getRecord(id= r[0].id_riga_prima_nota)
                    if rpn:
                        messageInfo(msg = "RIGA TERZA RATA GIA' INSERITA CORRETTAMENTE")
                else:
                    idrigapn = creaRigaPrimaNota(anaedit,numero_paga=3)
                    creaRigaPrimaNotaTestataDocScad(idrigapn,idpag3)
            else:
                messageInfo(msg= "PREMERE PRIMA APPLICA PER SALVARE IL DOCUMENTO ED I PAGAMENTI")
#        pbar(anaedit.pbar,parziale=5, totale=5)
        if anaedit.importo_quarta_scadenza_entry.get_text() and \
                            anaedit.data_pagamento_quarta_scadenza_entry.get_text():
            accontoDao4= TestataDocumentoScadenza().select(idTestataDocumento=anaedit.dao.id, numeroScadenza=4)
            if accontoDao4:
                idpag4 =  accontoDao4[0].id
                r = RigaPrimaNotaTestataDocumentoScadenza().select(idTestataDocumentoScadenza = idpag4)
                if r:
                    rpn = RigaPrimaNota().getRecord(id= r[0].id_riga_prima_nota)
                    if rpn:
                        messageInfo(msg = "RIGA QUARTA RATA GIA' INSERITA CORRETTAMENTE")
                else:
                    idrigapn = creaRigaPrimaNota(anaedit,numero_paga=4)
                    creaRigaPrimaNotaTestataDocScad(idrigapn,idpag4)
            else:
                messageInfo(msg= "PREMERE PRIMA APPLICA PER SALVARE IL DOCUMENTO ED I PAGAMENTI")
#        pbar(anaedit.pbar,stop=True)
        messageInfo(msg = "FINITO")

def creaRigaPrimaNotaTestataDocScad(idrigapn, idpag):
    a = RigaPrimaNotaTestataDocumentoScadenza()
    a.id_riga_prima_nota = idrigapn
    a.id_testata_documento_scadenza = idpag
    a.persist()


def creaRigaPrimaNota(anaedit, numero_paga):
    ope= leggiOperazione(anaedit.dao.operazione)
    for n in anaedit.dao.scadenze:
        if numero_paga == n.numero_scadenza:
            if n.numero_scadenza == 0:
                tipo = Pagamento().select(denominazione=n.pagamento)[0].tipo
                valore = Decimal(anaedit.importo_acconto_scadenza_entry.get_text())
                data_registrazione = stringToDate(anaedit.data_pagamento_acconto_entry.get_text())
                tipo_pag =  " ACCONTO "
            elif n.numero_scadenza == 1:
                tipo = Pagamento().select(denominazione=n.pagamento)[0].tipo
                valore = Decimal(anaedit.importo_prima_scadenza_entry.get_text())
                data_registrazione = stringToDate(anaedit.data_pagamento_prima_scadenza_entry.get_text())
                tipo_pag = "PRIMA RATA"
            elif n.numero_scadenza == 2:
                tipo = Pagamento().select(denominazione=n.pagamento)[0].tipo
                valore = Decimal(anaedit.importo_seconda_scadenza_entry.get_text())
                data_registrazione = stringToDate(anaedit.data_pagamento_seconda_scadenza_entry.get_text())
                tipo_pag = "SECONDA RATA"
            elif n.numero_scadenza == 3:
                tipo = Pagamento().select(denominazione=n.pagamento)[0].tipo
                valore = Decimal(anaedit.importo_terza_scadenza_entry.get_text())
                data_registrazione = stringToDate(anaedit.data_pagamento_terza_scadenza_entry.get_text())
                tipo_pag = "TERZA RATA"
            elif n.numero_scadenza == 4:
                tipo = Pagamento().select(denominazione=n.pagamento)[0].tipo
                valore = Decimal(anaedit.importo_quarta_scadenza_entry.get_text())
                data_registrazione = stringToDate(anaedit.data_pagamento_quarta_scadenza_entry.get_text())
                tipo_pag = "QUARTA RATA"
    if ope["segno"] == "-":
        stringa = "%s N.%s del. %s a %s ,  %s"    %(anaedit.dao.operazione, str(anaedit.dao.numero), dateToString(anaedit.dao.data_documento), anaedit.dao.intestatario, tipo_pag)
        segno = "entrata"
    else:
        stringa = "%s N.%s del. %s da %s, %s"    %(anaedit.dao.operazione, str(anaedit.dao.numero), dateToString(anaedit.dao.data_documento), anaedit.dao.intestatario, tipo_pag)
        segno = "uscita"
    tpn = TestataPrimaNota().select(datafinecheck = True)
    try:
        numero = max(a.numero for a in RigaPrimaNota().select(idTestataPrimaNota=tpn[0].id, batchSize=None))
    except:
        numero = 0
    rigaprimanota = RigaPrimaNota()
    rigaprimanota.denominazione = stringa
    rigaprimanota.id_testata_prima_nota = tpn[0].id
#        rigaprimanota.id_banca = #trovare
    rigaprimanota.numero = numero+1
    rigaprimanota.data_registrazione = data_registrazione
    rigaprimanota.tipo = tipo.lower()
    rigaprimanota.segno = segno
    rigaprimanota.valore = valore
    rigaprimanota.persist()
    return rigaprimanota.id


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
        dialog = gtk.MessageDialog(anaedit.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            anaedit.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')
            anaedit.chiudi_pagamento_documento_button.set_sensitive(False)
            anaedit.apri_pagamento_documento_button.set_sensitive(True)
    else:
        anaedit.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')


def on_apri_pagamento_documento_button_clicked(anaedit, button):
    """ Riapri o apri il pagamento"""
    msg = 'Attenzione! Stai per riaprire un documento considerato già pagato.\n Continuare ?'
    dialog = gtk.MessageDialog(anaedit.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_YES:
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
