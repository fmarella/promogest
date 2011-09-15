# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: JJDaNiMoTh <jjdanimoth@gmail.com>
#    Author: Dr astico <zoccolodignu@gmail.com>
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

from decimal import *
from promogest.dao.Pagamento import Pagamento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota
from promogest.modules.PrimaNota.dao.RigaPrimaNota import RigaPrimaNota
from promogest.modules.PrimaNota.dao.RigaPrimaNotaTestataDocumentoScadenza import RigaPrimaNotaTestataDocumentoScadenza
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from promogest.ui.utils import *


(
    INFO_SCADENZA_PAGE,
    PRIMA_SCADENZA_PAGE,
    SECONDA_SCADENZA_PAGE,
    TERZA_SCADENZA_PAGE,
    QUARTA_SCADENZA_PAGE,
    ACCONTO_PAGE
) = range(6)

def aggiungi_acconto_attivato(anaedit):
    """Richiamato quando c'è un acconto nel pagamento

    """
    anaedit.pagamenti_page.aggiungi_scheda_acconto_button.set_label("Rimuovi acconto")
    notebook_tab_show(anaedit.pagamenti_page.scadenze_notebook, ACCONTO_PAGE)

def aggiungi_acconto_disattivato(anaedit):
    """Richiamato quando non c'è un acconto nel pagamento

    """
    anaedit.pagamenti_page.aggiungi_scheda_acconto_button.set_label("Aggiungi acconto")
    notebook_tab_hide(anaedit.pagamenti_page.scadenze_notebook, ACCONTO_PAGE)

def IsPagamentoMultiplo(combobox):
    """
    Controlla la scadenza contenuta nel combobox, restituendo una lista con questi valori:
    valore_di_ritorno = [ 'nome_pagamento', 'giorni_prima_scad', 'separatore', ..., 'FM']
    al posto di ... ci sono 3 ulteriori valori ( fino ad un totale di quattro scadenze )
    e 3 ulteriori separatori. Il valore dell'ultimo campo e` FM se e` una scadenza da
    intendersi a fine mese o '' se non e` da intendersi a fine mese. Nel caso in cui
    il pagamento non sia riconosciuto, o non contenga scadenze, ritorna solo il nome
    del pagamento.
    """

    stringaCombobox = findStrFromCombobox(combobox, 2)
    controllascadenza = re.compile('^.* [0-9]?(.[0-9]+)+.*$')
    r = controllascadenza.match(stringaCombobox)
    finemese = re.compile('^.* [(F|f).(M|m)]*.$')
    if r:
        var = re.split('([0-9]+)', stringaCombobox)
        p = finemese.match(var[len(var)-1])
        if p:
            var[len(var)-1] = "FM"
            return var
        else:
            return var
    else:
        return stringaCombobox

def dividi_importo(anaedit):
    """ Divide l'importo passato per il numero delle scadenze. Se viene passato un argomento, che indica
    il valore di una rata, ricalcola gli altri tenendo conto del valore modificato
    TODO: Passare i valori valuta a mN
    """
    if anaedit.totale_scontato_riepiloghi_label.get_text() == '-':
        return

    importodoc = float(anaedit.totale_scontato_riepiloghi_label.get_text() or 0)
    if importodoc == 0:
        return
    acconto = float(anaedit.pagamenti_page.importo_acconto_scadenza_entry.get_text() or 0)
    importo_primo_doc = float(anaedit.pagamenti_page.importo_primo_documento_entry.get_text() or 0)
    importo_secondo_doc = float(anaedit.pagamenti_page.importo_secondo_documento_entry.get_text() or 0)
    importotot = importodoc - acconto - importo_primo_doc - importo_secondo_doc

    pagamenti = IsPagamentoMultiplo(anaedit.pagamenti_page.id_pagamento_customcombobox.combobox)
    importorate = [0, 0, 0, 0]
    if type(pagamenti) == list:
        if pagamenti != None:
            n_pagamenti = (len(pagamenti) - 1) / 2
            importorate = dividi_in_rate(importotot, n_pagamenti)
        else:
            n_pagamenti = 1
            importorate[0] = importotot
    else:
        n_pagamenti = 1
        importorate[0] = importotot

    try:
        anaedit.pagamenti_page.importo_prima_scadenza_entry.set_text("%.2f" % importorate[0])
        anaedit.pagamenti_page.importo_seconda_scadenza_entry.set_text("%.2f" % importorate[1])
        anaedit.pagamenti_page.importo_terza_scadenza_entry.set_text("%.2f" % importorate[2])
        anaedit.pagamenti_page.importo_quarta_scadenza_entry.set_text("%.2f" % importorate[3])
    except IndexError:
        pass

    if acconto != 0:
        anaedit.acconto = True
        aggiungi_acconto_attivato(anaedit)
    else:
        anaedit.acconto = False
        aggiungi_acconto_disattivato(anaedit)

    if n_pagamenti == 3:
        anaedit.pagamenti_page.importo_quarta_scadenza_entry.set_text("")
        notebook_tabs_hide(anaedit.pagamenti_page.scadenze_notebook, (INFO_SCADENZA_PAGE, QUARTA_SCADENZA_PAGE,))
        notebook_tabs_show(anaedit.pagamenti_page.scadenze_notebook, (PRIMA_SCADENZA_PAGE, SECONDA_SCADENZA_PAGE, TERZA_SCADENZA_PAGE))
    elif n_pagamenti == 2:
        anaedit.pagamenti_page.importo_terza_scadenza_entry.set_text("")
        anaedit.pagamenti_page.importo_quarta_scadenza_entry.set_text("")
        notebook_tabs_hide(anaedit.pagamenti_page.scadenze_notebook, (INFO_SCADENZA_PAGE, TERZA_SCADENZA_PAGE, QUARTA_SCADENZA_PAGE),)
        notebook_tabs_show(anaedit.pagamenti_page.scadenze_notebook, (PRIMA_SCADENZA_PAGE, SECONDA_SCADENZA_PAGE))
    elif n_pagamenti == 1:
        anaedit.pagamenti_page.importo_seconda_scadenza_entry.set_text("")
        anaedit.pagamenti_page.importo_terza_scadenza_entry.set_text("")
        anaedit.pagamenti_page.importo_quarta_scadenza_entry.set_text("")
        notebook_tabs_hide(anaedit.pagamenti_page.scadenze_notebook, (INFO_SCADENZA_PAGE, SECONDA_SCADENZA_PAGE, TERZA_SCADENZA_PAGE, QUARTA_SCADENZA_PAGE),)
        notebook_tabs_show(anaedit.pagamenti_page.scadenze_notebook, (PRIMA_SCADENZA_PAGE,))

def ricalcola_sospeso_e_pagato(anaedit):
    """ Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della quarta scadenza
        Ricalcola i totali sospeso e pagato in base alle
        scadenze ancora da saldare
    """
    if anaedit.pagamenti_page.data_pagamento_prima_scadenza_entry.get_text() != "":
        totalepagato = float(anaedit.pagamenti_page.importo_acconto_scadenza_entry.get_text() or '0')
        totalepagato = totalepagato + float(anaedit.pagamenti_page.importo_prima_scadenza_entry.get_text() or '0')
        totalesospeso = float(0)
    else:
        totalepagato = float(anaedit.pagamenti_page.importo_acconto_scadenza_entry.get_text() or '0')
        totalesospeso = float(anaedit.pagamenti_page.importo_prima_scadenza_entry.get_text() or '0')
        anaedit.pagamenti_page.stato_label.set_markup('<b><span foreground="#B40000" size="24000">APERTO</span></b>')
    if anaedit.pagamenti_page.data_pagamento_seconda_scadenza_entry.get_text() != "":
        totalepagato = totalepagato + float(anaedit.pagamenti_page.importo_seconda_scadenza_entry.get_text() or '0')
    else:
        totalesospeso = totalesospeso + float(anaedit.pagamenti_page.importo_seconda_scadenza_entry.get_text() or '0')
    if anaedit.pagamenti_page.data_pagamento_terza_scadenza_entry.get_text() != "":
        totalepagato = totalepagato + float(anaedit.pagamenti_page.importo_terza_scadenza_entry.get_text() or '0')
    else:
        totalesospeso = totalesospeso + float(anaedit.pagamenti_page.importo_terza_scadenza_entry.get_text() or '0')
    if anaedit.pagamenti_page.data_pagamento_quarta_scadenza_entry.get_text() != "":
        totalepagato = totalepagato + float(anaedit.pagamenti_page.importo_quarta_scadenza_entry.get_text() or '0')
    else:
        totalesospeso = totalesospeso + float(anaedit.pagamenti_page.importo_quarta_scadenza_entry.get_text() or '0')

    totalepagato = totalepagato + float(anaedit.pagamenti_page.importo_primo_documento_entry.get_text() or '0')
    totalepagato = totalepagato + float(anaedit.pagamenti_page.importo_secondo_documento_entry.get_text() or '0')

    anaedit.pagamenti_page.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(mN(totalepagato,2))+'</span></b>')

    if totalepagato ==0:
        totalesospeso = float(anaedit.pagamenti_page.totale_in_pagamenti_label.get_text())
    if totalesospeso == 0:
        totalesospeso = float(anaedit.pagamenti_page.totale_in_pagamenti_label.get_text()) - totalepagato
    anaedit.pagamenti_page.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(mN(totalesospeso,2))+'</span></b>')
    if totalepagato == 0 and totalesospeso == 0:
        #self.attiva_prima_scadenza(False, True)
        #self.attiva_seconda_scadenza(False, True)
        #self.attiva_terza_scadenza(False, True)
        #self.attiva_quarta_scadenza(False, True)
        anaedit.pagamenti_page.stato_label.set_markup('<b><span foreground="#B40000" size="24000">APERTO</span></b>')
    if totalepagato == float(anaedit.pagamenti_page.totale_in_pagamenti_label.get_text()) and\
                    anaedit.pagamenti_page.stato_label.get_text() == "APERTO" and \
                    anaedit.notebook.get_current_page() ==3:
        msg = """Attenzione! L'importo in sospeso è pari a 0 e
l'importo pagato è uguale al totale documento.
Procedere con la "chiusura" del Pagamento?"""
        procedi = YesNoDialog(msg=msg, transient=None)
        if procedi:
            anaedit.pagamenti_page.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')

def controlla_rate_scadenza(anaedit, messaggio):
    """
    Controlla che gli importi inseriti nelle scadenze siano corrispondenti
    al totale del documento. Ritorna False se c'e` un errore,
    True se e` tutto corretto.
    """

    importotot = float(anaedit.totale_scontato_riepiloghi_label.get_text() or 0)
    if importotot == 0:
        return
    importo_immesso_acconto = float(anaedit.importo_acconto_scadenza_entry.get_text() or 0)
    importo_immesso_prima = float(anaedit.importo_prima_scadenza_entry.get_text() or 0)
    importo_immesso_seconda = float(anaedit.importo_seconda_scadenza_entry.get_text() or 0)
    importo_immesso_terza = float(anaedit.importo_terza_scadenza_entry.get_text() or 0)
    importo_immesso_quarta = float(anaedit.importo_quarta_scadenza_entry.get_text() or 0)

    importo_primo_riferimento = float(anaedit.importo_primo_documento_entry.get_text() or 0)
    importo_secondo_riferimento = float(anaedit.importo_secondo_documento_entry.get_text() or 0)

    differenza_importi = (importo_immesso_acconto + importo_immesso_prima + importo_immesso_seconda +
        importo_immesso_terza + importo_immesso_quarta + importo_primo_riferimento +
        importo_secondo_riferimento) - importotot
    if differenza_importi == 0 - importotot:
        if messaggio:
            messageInfo(msg="Importo delle rate non inserite")
        return True

    elif differenza_importi != 0:
        if messaggio:
            messageInfo(msg="""ATTENZIONE!
La somma degli importi che Lei ha inserito come rate nelle scadenze
non corrisponde al totale del documento. La invitiamo a ricontrollare.
Ricordiamo inoltre che allo stato attuale e` impossibile salvare il documento.
Per l'esattezza, l'errore e` di %.2f""" % differenza_importi)
        return False
    else:
        if messaggio:
            messageInfo(msg="Gli importi inseriti come rate corrispondono con il totale del documento")
        return True

def getDocumentoCollegato(anaedit, numerodocumento):
    """
    Trova il documento in base al numero e ritorna un cursore al documento stesso.
    """

    if anaedit._tipoPersonaGiuridica == "cliente":
        idCliente = anaedit.id_persona_giuridica_customcombobox.getId()
        idFornitore = None
        tipoDocumento = "Nota di credito a cliente"
    elif anaedit._tipoPersonaGiuridica == "fornitore":
        idCliente = None
        idFornitore = anaedit.id_persona_giuridica_customcombobox.getId()
        tipoDocumento = "Nota di credito da fornitore"

    result = TestataDocumento().select(daNumero=numerodocumento,
                                        aNumero=numerodocumento,
                                        daParte=None,
                                        aParte=None,
                                        daData=None,
                                        aData=None,
                                        protocollo=None,
                                        idOperazione=tipoDocumento,
                                        idMagazzino=None,
                                        idCliente=idCliente,
                                        idFornitore=idFornitore)

    if len(result) > 1:
        messageInfo(msg= "Sono stati trovati piu` di un documento. Hai scovato un bug :D")
        return False
    elif len(result) == 0:
        messageInfo(msg="Non e' stato trovato nessun documento con il numero specificato")
        return False
    else:
        return result

def impostaDocumentoCollegato(numerodocumento):
    """
    Imposta il documento indicato dall'utente come collegato al documento
    in creazione.
    """

    documento = getDocumentoCollegato(numerodocumento)
    if documento == False:
        return False
    daoTestata = TestataDocumento().getRecord(id=documento[0].id)
    tipo_documento = daoTestata.operazione
    totale_pagato = daoTestata.totale_pagato
    totale_sospeso = daoTestata.totale_sospeso
    numero_documento = daoTestata.numero
    data_documento = daoTestata.data_documento

    if totale_sospeso != 0:
        messageError(msg="""Attenzione. Risulta che il documento da Lei scelto abbia ancora
un importo in sospeso. Il documento, per poter essere collegato, deve essere completamente saldato""")
        return False

    return totale_pagato

def attiva_scadenze(anaedit):
    """
    Attiva le scadenze necessarie in base alle scadenze passate; il valore passato
    deve essere necessariamente ottenuto dalla funzione IsPagamentoMultiplo.
    Chiama inoltre apposite istanze di dividi_importo() per suddividere
    l'importo totale nelle varie rate.
    """

    if anaedit.totale_scontato_riepiloghi_label.get_text() == "-":
        return 1

    scadenze = IsPagamentoMultiplo(anaedit.pagamenti_page.id_pagamento_customcombobox.combobox)
    data_doc = stringToDate(anaedit.data_documento_entry.get_text())
    importotot = float(anaedit.totale_scontato_riepiloghi_label.get_text())


    if type(scadenze) == list:
        numeroscadenze = (len(scadenze) - 1) / 2 # Trovo il numero delle scadenze contando gli elementi
                                                 # della variabile passata, sottraendo il caratteee di
                                                 # Fine Mese e dividendo per due ( vedere la doc di
                                                 # IsPagamentoMultiplo per maggiori informazioni )
        paga = findStrFromCombobox(anaedit.pagamenti_page.id_pagamento_customcombobox.combobox, 2)
        if scadenze[len(scadenze)-1] != "FM":
            fine_mese = False
        else:
            fine_mese = True

#            anaedit.primo_pagamento_entry.set_text(scadenze[0] + scadenze[1] + " gg")

        findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_prima_scadenza_customcombobox.combobox, paga, 2)
        if numeroscadenze == 1:
            anaedit.pagamenti_page.data_prima_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[1]), fine_mese)))
        elif numeroscadenze == 2:
            anaedit.pagamenti_page.data_prima_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[1]), fine_mese)))
            anaedit.pagamenti_page.data_seconda_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[3]), fine_mese)))
#                anaedit.secondo_pagamento_entry.set_text(scadenze[0] + scadenze[3] + " gg")
            findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_seconda_scadenza_customcombobox.combobox, paga,2)
        elif numeroscadenze == 3:
            anaedit.pagamenti_page.data_prima_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[1]), fine_mese)))
            anaedit.pagamenti_page.data_seconda_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[3]), fine_mese)))
            anaedit.pagamenti_page.data_terza_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[5]), fine_mese)))
#                anaedit.secondo_pagamento_entry.set_text(scadenze[0] + scadenze[3] + " gg")
            findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_seconda_scadenza_customcombobox.combobox, paga,2)
#                anaedit.terzo_pagamento_entry.set_text(scadenze[0] + scadenze[5] + " gg")
            findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_terza_scadenza_customcombobox.combobox, paga,2)
        elif numeroscadenze == 4:
            anaedit.pagamenti_page.data_quarta_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[7]), fine_mese)))
            anaedit.pagamenti_page.data_terza_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[5]), fine_mese)))
            anaedit.pagamenti_page.data_prima_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[1]), fine_mese)))
            anaedit.pagamenti_page.data_seconda_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[3]), fine_mese)))
#                anaedit.secondo_pagamento_entry.set_text(scadenze[0] + scadenze[3] + " gg")
            findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_seconda_scadenza_customcombobox.combobox, paga,2)
#                anaedit.terzo_pagamento_entry.set_text(scadenze[0] + scadenze[5] + " gg")
            findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_terza_scadenza_customcombobox.combobox, paga,2)
#                anaedit.quarto_pagamento_entry.set_text(scadenze[0] + scadenze[7] + " gg")
            findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_quarta_scadenza_customcombobox.combobox, paga,2)
        else:
            print "Numero troppo alto di scadenze; Funzione non ancora implementata. Manda un bug report"
    else:
        anaedit.pagamenti_page.data_prima_scadenza_entry.set_text(dateToString(data_doc))
        findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_prima_scadenza_customcombobox.combobox, scadenze,2)
#            anaedit.primo_pagamento_entry.set_text(scadenze)

def getScadenze(anaedit):
    notebook_tabs_hide(anaedit.pagamenti_page.scadenze_notebook, (PRIMA_SCADENZA_PAGE, SECONDA_SCADENZA_PAGE, TERZA_SCADENZA_PAGE, QUARTA_SCADENZA_PAGE, ACCONTO_PAGE,))
    aggiungi_acconto_disattivato(anaedit)
    if anaedit.dao.scadenze:
        notebook_tabs_hide(anaedit.pagamenti_page.scadenze_notebook, (INFO_SCADENZA_PAGE,))
        for scadenza in anaedit.dao.scadenze:
            if scadenza.numero_scadenza == 0:
                anaedit.pagamenti_page.data_acconto_entry.set_text(dateToString(scadenza.data) or '')
                anaedit.pagamenti_page.importo_acconto_scadenza_entry.set_text(str(scadenza.importo or ''))
                findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_acconto_customcombobox.combobox, scadenza.pagamento, 2)
                findComboboxRowFromStr(anaedit.pagamenti_page.id_banca_acconto_ccb.combobox, scadenza.id_banca, 1)
                textview_set_text(anaedit.pagamenti_page.note_acconto_textview, scadenza.note_per_primanota)
                anaedit.pagamenti_page.data_pagamento_acconto_entry.set_text(dateToString
                    (scadenza.data_pagamento or ''))
                anaedit.acconto = True
                aggiungi_acconto_attivato(anaedit)
            elif scadenza.numero_scadenza == 1:
                anaedit.pagamenti_page.data_prima_scadenza_entry.set_text(dateToString(scadenza.data) or '')
                anaedit.pagamenti_page.importo_prima_scadenza_entry.set_text(str(scadenza.importo or ''))
                findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_prima_scadenza_customcombobox.combobox, scadenza.pagamento,2)
                findComboboxRowFromStr(anaedit.pagamenti_page.id_banca_prima_scadenza_ccb.combobox, scadenza.id_banca, 1)
                textview_set_text(anaedit.pagamenti_page.note_prima_scadenza_textview, scadenza.note_per_primanota)
                anaedit.pagamenti_page.data_pagamento_prima_scadenza_entry.set_text(dateToString
                    (scadenza.data_pagamento or ''))
                notebook_tab_show(anaedit.pagamenti_page.scadenze_notebook, PRIMA_SCADENZA_PAGE)
            elif scadenza.numero_scadenza == 2:
                anaedit.pagamenti_page.data_seconda_scadenza_entry.set_text(dateToString
                    (scadenza.data or ''))
                anaedit.pagamenti_page.importo_seconda_scadenza_entry.set_text(str(scadenza.importo or ''))
                findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_seconda_scadenza_customcombobox.combobox, scadenza.pagamento,2)
                findComboboxRowFromStr(anaedit.pagamenti_page.id_banca_seconda_scadenza_ccb.combobox, scadenza.id_banca, 1)
                textview_set_text(anaedit.pagamenti_page.note_seconda_scadenza_textview, scadenza.note_per_primanota)
                anaedit.pagamenti_page.data_pagamento_seconda_scadenza_entry.set_text(dateToString
                    (scadenza.data_pagamento or ''))
                notebook_tab_show(anaedit.pagamenti_page.scadenze_notebook, SECONDA_SCADENZA_PAGE)
            elif scadenza.numero_scadenza == 3:
                anaedit.pagamenti_page.data_terza_scadenza_entry.set_text(dateToString
                    (scadenza.data or ''))
                anaedit.pagamenti_page.importo_terza_scadenza_entry.set_text(str(scadenza.importo or ''))
                findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_terza_scadenza_customcombobox.combobox, scadenza.pagamento,2)
                findComboboxRowFromStr(anaedit.pagamenti_page.id_banca_terza_scadenza_ccb.combobox, scadenza.id_banca, 1)
                textview_set_text(anaedit.pagamenti_page.note_terza_scadenza_textview, scadenza.note_per_primanota)
                anaedit.pagamenti_page.data_pagamento_terza_scadenza_entry.set_text(dateToString
                    (scadenza.data_pagamento or ''))
                notebook_tab_show(anaedit.pagamenti_page.scadenze_notebook, TERZA_SCADENZA_PAGE)
            elif scadenza.numero_scadenza == 4:
                anaedit.pagamenti_page.data_quarta_scadenza_entry.set_text(dateToString
                    (scadenza.data or ''))
                anaedit.pagamenti_page.importo_quarta_scadenza_entry.set_text(str(scadenza.importo or ''))
                findComboboxRowFromStr(anaedit.pagamenti_page.id_pagamento_quarta_scadenza_customcombobox.combobox, scadenza.pagamento,2)
                findComboboxRowFromStr(anaedit.pagamenti_page.id_banca_quarta_scadenza_ccb.combobox, scadenza.id_banca, 1)
                textview_set_text(anaedit.pagamenti_page.note_quarta_scadenza_textview, scadenza.note_per_primanota)
                anaedit.pagamenti_page.data_pagamento_quarta_scadenza_entry.set_text(dateToString
                    (scadenza.data_pagamento or ''))
                notebook_tab_show(anaedit.pagamenti_page.scadenze_notebook, QUARTA_SCADENZA_PAGE)
    else:
        notebook_tabs_show(anaedit.pagamenti_page.scadenze_notebook, (INFO_SCADENZA_PAGE,))

    if anaedit.dao.documento_saldato:
        anaedit.pagamenti_page.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')
    else:
        anaedit.pagamenti_page.stato_label.set_markup('<b><span foreground="#B40000" size="24000">APERTO</span></b>')
    anaedit.pagamenti_page.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(
        anaedit.dao.totale_pagato or 0)+'</span></b>')

    if (anaedit.dao.totale_sospeso is None)  or (anaedit.dao.totale_sospeso == 0):
        totaleSospeso = Decimal(str(anaedit.totale_scontato_riepiloghi_label.get_text() or 0)) - Decimal(str(anaedit.dao.totale_pagato or 0))
    else:
        totaleSospeso = anaedit.dao.totale_sospeso

    anaedit.pagamenti_page.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(
        totaleSospeso)+'</span></b>')
    if anaedit.dao.id_primo_riferimento != None:
        doc = TestataDocumento().getRecord(id=anaedit.dao.id_primo_riferimento)
        anaedit.pagamenti_page.importo_primo_documento_entry.set_text(str(doc.totale_pagato) or '')
        anaedit.pagamenti_page.numero_primo_documento_entry.set_text(str(doc.numero) or '')
        anaedit.pagamenti_page.importo_secondo_documento_entry.set_sensitive(True)
        anaedit.pagamenti_page.numero_secondo_documento_entry.set_sensitive(True)
        anaedit.pagamenti_page.seleziona_seconda_nota_button.set_sensitive(True)
        if anaedit.dao.id_secondo_riferimento != None:
            doc = TestataDocumento().getRecord(id=anaedit.dao.id_secondo_riferimento)
            anaedit.pagamenti_page.importo_secondo_documento_entry.set_text(str(doc.totale_pagato) or '')
            anaedit.pagamenti_page.numero_secondo_documento_entry.set_text(str(doc.numero) or '')
        else:
            anaedit.pagamenti_page.importo_secondo_documento_entry.set_text('')
            anaedit.pagamenti_page.numero_secondo_documento_entry.set_text('')
    else:
        anaedit.pagamenti_page.importo_primo_documento_entry.set_text('')
        anaedit.pagamenti_page.importo_secondo_documento_entry.set_text('')
        anaedit.pagamenti_page.numero_primo_documento_entry.set_text('')
        anaedit.pagamenti_page.numero_secondo_documento_entry.set_text('')

def saveScadenze(anaedit):
    """ Di fatto è la parte che gestisce il salvataggio dei dati
    di pagamento
    TODO: aggiungere la cancellazione se vengono trovate più righe?"""
    anaedit.dao.totale_pagato = float(anaedit.pagamenti_page.totale_pagato_scadenza_label.get_text())
    anaedit.dao.totale_sospeso = float(anaedit.pagamenti_page.totale_sospeso_scadenza_label.get_text())
    if anaedit.pagamenti_page.stato_label.get_text() == "PAGATO":
        anaedit.dao.documento_saldato = True
    else:
        anaedit.dao.documento_saldato = False
    anaedit.dao.ripartire_importo =  anaedit.pagamenti_page.primanota_check.get_active()
    scadenze = []
#        accontoDao0= TestataDocumentoScadenza().select(idTestataDocumento=anaedit.dao.id, numeroScadenza=0)
    if anaedit.pagamenti_page.data_acconto_entry.get_text() != "":
#            if accontoDao0:
#                daoTestataDocumentoScadenza = accontoDao0[0]
#            else:
        daoTestataDocumentoScadenza = TestataDocumentoScadenza()
        daoTestataDocumentoScadenza.id_testata_documento = anaedit.dao.id
        if stringToDate(anaedit.pagamenti_page.data_acconto_entry.get_text()) =="":
            obligatoryField(anaedit.dialogTopLevel,
                anaedit.pagamenti_page.data_acconto_entry,
                'Inserire una data acconto!')
        daoTestataDocumentoScadenza.data = stringToDate(anaedit.pagamenti_page.data_acconto_entry.get_text())
        daoTestataDocumentoScadenza.importo = float(anaedit.pagamenti_page.importo_acconto_scadenza_entry.get_text() or '0')
        idpag0 = findIdFromCombobox(anaedit.pagamenti_page.id_pagamento_acconto_customcombobox.combobox)
        if idpag0:
            p0 = Pagamento().getRecord(id=idpag0)
            daoTestataDocumentoScadenza.pagamento = p0.denominazione
        else:
            obligatoryField(anaedit.dialogTopLevel,
                    anaedit.pagamenti_page.id_pagamento_acconto_customcombobox.combobox,
                    'Inserire una forma di pagamento!')
        daoTestataDocumentoScadenza.data_pagamento = daoTestataDocumentoScadenza.data
        daoTestataDocumentoScadenza.numero_scadenza = 0
        idbanca = findIdFromCombobox(anaedit.pagamenti_page.id_banca_acconto_ccb.combobox)
        if idbanca:
            daoTestataDocumentoScadenza.id_banca = idbanca
        note_acconto_PN = textview_get_text(anaedit.pagamenti_page.note_acconto_textview)
        if note_acconto_PN:
            daoTestataDocumentoScadenza.note_per_primanota = note_acconto_PN
        scadenze.append(daoTestataDocumentoScadenza)
    if anaedit.pagamenti_page.data_prima_scadenza_entry.get_text() != "":
        daoTestataDocumentoScadenza = TestataDocumentoScadenza()
        daoTestataDocumentoScadenza.id_testata_documento = anaedit.dao.id
        if stringToDate(anaedit.pagamenti_page.data_prima_scadenza_entry.get_text()) =="":
            obligatoryField(anaedit.dialogTopLevel,
                anaedit.pagamenti_page.data_prima_scadenza_entry,
                'Inserire una data!')
        daoTestataDocumentoScadenza.data = stringToDate(anaedit.pagamenti_page.data_prima_scadenza_entry.get_text())
        daoTestataDocumentoScadenza.importo = float(anaedit.pagamenti_page.importo_prima_scadenza_entry.get_text() or '0')
        idpag1 = findIdFromCombobox(anaedit.pagamenti_page.id_pagamento_prima_scadenza_customcombobox.combobox)
        if idpag1:
            p1 = Pagamento().getRecord(id=idpag1)
            daoTestataDocumentoScadenza.pagamento = p1.denominazione
        else:
            obligatoryField(anaedit.dialogTopLevel,
                anaedit.pagamenti_page.id_pagamento_acconto_customcombobox.combobox,
                'Inserire una forma di pagamento!')
        daoTestataDocumentoScadenza.data_pagamento = stringToDate(
                anaedit.pagamenti_page.data_pagamento_prima_scadenza_entry.get_text())
        daoTestataDocumentoScadenza.numero_scadenza = 1
        idbanca = findIdFromCombobox(anaedit.pagamenti_page.id_banca_prima_scadenza_ccb.combobox)
        if idbanca:
            daoTestataDocumentoScadenza.id_banca = idbanca
        note_acconto_PN = textview_get_text(anaedit.pagamenti_page.note_prima_scadenza_textview)
        if note_acconto_PN:
            daoTestataDocumentoScadenza.note_per_primanota = note_acconto_PN
        scadenze.append(daoTestataDocumentoScadenza)
    if anaedit.pagamenti_page.data_seconda_scadenza_entry.get_text() != "":
        daoTestataDocumentoScadenza = TestataDocumentoScadenza()
        daoTestataDocumentoScadenza.id_testata_documento = anaedit.dao.id
        if stringToDate(anaedit.pagamenti_page.data_seconda_scadenza_entry.get_text()) =="":
            obligatoryField(anaedit.dialogTopLevel,
                anaedit.pagamenti_page.data_seconda_scadenza_entry,
                'Inserire una data!')
        daoTestataDocumentoScadenza.data = stringToDate(
                anaedit.pagamenti_page.data_seconda_scadenza_entry.get_text())
        daoTestataDocumentoScadenza.importo = float(
                anaedit.pagamenti_page.importo_seconda_scadenza_entry.get_text() or '0')
        idpag2 = findIdFromCombobox(anaedit.pagamenti_page.id_pagamento_seconda_scadenza_customcombobox.combobox)
        if idpag2:
            p2 = Pagamento().getRecord(id=idpag2)
            daoTestataDocumentoScadenza.pagamento = p2.denominazione
        else:
            obligatoryField(anaedit.dialogTopLevel,
                anaedit.pagamenti_page.id_pagamento_acconto_customcombobox.combobox,
                'Inserire una forma di pagamento!')
        daoTestataDocumentoScadenza.data_pagamento = stringToDate(
                anaedit.pagamenti_page.data_pagamento_seconda_scadenza_entry.get_text())
        daoTestataDocumentoScadenza.numero_scadenza = 2
        idbanca = findIdFromCombobox(anaedit.pagamenti_page.id_banca_seconda_scadenza_ccb.combobox)
        if idbanca:
            daoTestataDocumentoScadenza.id_banca = idbanca
        note_acconto_PN = textview_get_text(anaedit.pagamenti_page.note_seconda_scadenza_textview)
        if note_acconto_PN:
            daoTestataDocumentoScadenza.note_per_primanota = note_acconto_PN
        scadenze.append(daoTestataDocumentoScadenza)
    if anaedit.pagamenti_page.data_terza_scadenza_entry.get_text() != "":
        daoTestataDocumentoScadenza = TestataDocumentoScadenza()
        daoTestataDocumentoScadenza.id_testata_documento = anaedit.dao.id
        if stringToDate(anaedit.pagamenti_page.data_terza_scadenza_entry.get_text()) =="":
            obligatoryField(anaedit.dialogTopLevel,
                anaedit.pagamenti_page.data_terza_scadenza_entry,
                'Inserire una data!')
        daoTestataDocumentoScadenza.data = stringToDate(
                anaedit.pagamenti_page.data_terza_scadenza_entry.get_text())
        daoTestataDocumentoScadenza.importo = float(
                anaedit.pagamenti_page.importo_terza_scadenza_entry.get_text() or '0')
        idpag3 = findIdFromCombobox(anaedit.pagamenti_page.id_pagamento_terza_scadenza_customcombobox.combobox)
        if idpag3:
            p3 = Pagamento().getRecord(id=idpag3)
            daoTestataDocumentoScadenza.pagamento = p3.denominazione
        else:
            obligatoryField(anaedit.dialogTopLevel,
                anaedit.pagamenti_page.id_pagamento_acconto_customcombobox.combobox,
                'Inserire una forma di pagamento!')
        daoTestataDocumentoScadenza.data_pagamento = stringToDate(
                anaedit.pagamenti_page.data_pagamento_terza_scadenza_entry.get_text())
        daoTestataDocumentoScadenza.numero_scadenza = 3
        idbanca = findIdFromCombobox(anaedit.pagamenti_page.id_banca_terza_scadenza_ccb.combobox)
        if idbanca:
            daoTestataDocumentoScadenza.id_banca = idbanca
        note_acconto_PN = textview_get_text(anaedit.pagamenti_page.note_terza_scadenza_textview)
        if note_acconto_PN:
            daoTestataDocumentoScadenza.note_per_primanota = note_acconto_PN
        scadenze.append(daoTestataDocumentoScadenza)
    if anaedit.pagamenti_page.data_quarta_scadenza_entry.get_text() != "":
        daoTestataDocumentoScadenza = TestataDocumentoScadenza()
        daoTestataDocumentoScadenza.id_testata_documento = anaedit.dao.id
        if stringToDate(anaedit.pagamenti_page.data_quarta_scadenza_entry.get_text()) =="":
            obligatoryField(anaedit.dialogTopLevel,
                anaedit.pagamenti_page.data_quarta_scadenza_entry,
                'Inserire una data!')
        daoTestataDocumentoScadenza.data = stringToDate(
                anaedit.pagamenti_page.data_quarta_scadenza_entry.get_text())
        daoTestataDocumentoScadenza.importo = float(
                anaedit.pagamenti_page.importo_quarta_scadenza_entry.get_text() or '0')
        idpag4 = findIdFromCombobox(anaedit.pagamenti_page.id_pagamento_quarta_scadenza_customcombobox.combobox)
        if idpag4:
            p4 = Pagamento().getRecord(id=idpag4)
            daoTestataDocumentoScadenza.pagamento = p4.denominazione
        else:
            obligatoryField(anaedit.dialogTopLevel,
                anaedit.pagamenti_page.id_pagamento_acconto_customcombobox.combobox,
                'Inserire una forma di pagamento!')
        daoTestataDocumentoScadenza.data_pagamento = stringToDate(
                anaedit.pagamenti_page.data_pagamento_quarta_scadenza_entry.get_text())
        daoTestataDocumentoScadenza.numero_scadenza = 4
        idbanca = findIdFromCombobox(anaedit.pagamenti_page.id_banca_quarta_scadenza_ccb.combobox)
        if idbanca:
            daoTestataDocumentoScadenza.id_banca = idbanca
        note_acconto_PN = textview_get_text(anaedit.pagamenti_page.note_quarta_scadenza_textview)
        if note_acconto_PN:
            daoTestataDocumentoScadenza.note_per_primanota = note_acconto_PN
        scadenze.append(daoTestataDocumentoScadenza)
    anaedit.dao.scadenze = scadenze

    #TODO: finire di sistemare questa parte ......

    doc = anaedit.pagamenti_page.numero_primo_documento_entry.get_text()
    if doc != "" and doc != "0":
        documentocollegato = getDocumentoCollegato(int(doc))
        anaedit.dao.id_primo_riferimento = documentocollegato[0].id
        doc2 = anaedit.pagamenti_page.numero_secondo_documento_entry.get_text()
        if doc2 != "" and doc2 != "0":
            documentocollegato = getDocumentoCollegato(int(doc2))
            anaedit.dao.id_secondo_riferimento = documentocollegato[0].id
