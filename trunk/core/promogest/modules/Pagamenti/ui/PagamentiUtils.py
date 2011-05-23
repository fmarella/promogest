# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux di Francesco Meloni snc - http://www.promotux.it/

# Author: Andrea Argiolas <andrea@promotux.it>
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
# Author: Dr astico <zoccolodignu@gmail.com>

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

from promogest.dao.Pagamento import Pagamento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from promogest.ui.utils import *

class Pagamenti(object):
    def __init__(self, anagrafica):
        self.anagrafica = anagrafica


    def attiva_acconto(self, action, disable = True):
        """
        Attiva i campi relativi alla prima scadenza nella tab Pagamenti
        Se action e` False, disattiva e pulisce i campi riguardanti la prima scadenza.
        """

        if disable:
            self.anagrafica.data_acconto_entry.set_sensitive(action)
            self.anagrafica.importo_acconto_scadenza_entry.set_sensitive(action)
        if not action:
            self.anagrafica.data_acconto_entry.set_text("")
            self.anagrafica.importo_acconto_scadenza_entry.set_text("")


    def attiva_prima_scadenza(self, action, disable = True):
        """
        Attiva i campi relativi alla prima scadenza nella tab Pagamenti
        Se action e` False, disattiva e pulisce i campi riguardanti la prima scadenza.
        """

        if disable:
            self.anagrafica.data_acconto_entry.set_sensitive(action)
            self.anagrafica.data_prima_scadenza_entry.set_sensitive(action)
#            self.anagrafica.primo_pagamento_entry.set_sensitive(action)
            self.anagrafica.data_pagamento_prima_scadenza_entry.set_sensitive(action)
            self.anagrafica.importo_acconto_scadenza_entry.set_sensitive(action)
            self.anagrafica.importo_prima_scadenza_entry.set_sensitive(action)
        if not action:
            self.anagrafica.data_acconto_entry.set_text("")
            self.anagrafica.data_prima_scadenza_entry.set_text("")
#            self.anagrafica.primo_pagamento_entry.set_text("")
            self.anagrafica.data_pagamento_prima_scadenza_entry.set_text("")
            self.anagrafica.importo_acconto_scadenza_entry.set_text("")
            self.anagrafica.importo_prima_scadenza_entry.set_text("")

    def attiva_seconda_scadenza(self, action, disable = True):
        """
        Attiva i campi relativi alla prima e alla seconda scadenza nella tab Pagamenti
        Se action e` False, disattiva e pulisce i campi riguardanti la seconda scadenza.
        """

        if disable:
            self.anagrafica.data_seconda_scadenza_entry.set_sensitive(action)
            self.anagrafica.importo_seconda_scadenza_entry.set_sensitive(action)
#            self.anagrafica.secondo_pagamento_entry.set_sensitive(action)
            self.anagrafica.data_pagamento_seconda_scadenza_entry.set_sensitive(action)
        if not action:
            self.anagrafica.data_seconda_scadenza_entry.set_text("")
            self.anagrafica.importo_seconda_scadenza_entry.set_text("")
#            self.anagrafica.secondo_pagamento_entry.set_text("")
            self.anagrafica.data_pagamento_seconda_scadenza_entry.set_text("")

    def attiva_terza_scadenza(self, action, disable = True):
        """
        Attiva i campi relativi alla prima, alla seconda e alla terza scadenza nella tab Pagamenti
        Se action e` False, disattiva e pulisce i campi riguardanti la terza scadenza.
        """

        if disable:
            self.anagrafica.data_terza_scadenza_entry.set_sensitive(action)
            self.anagrafica.importo_terza_scadenza_entry.set_sensitive(action)
#            self.anagrafica.terzo_pagamento_entry.set_sensitive(action)
            self.anagrafica.data_pagamento_terza_scadenza_entry.set_sensitive(action)
        if not action:
            self.anagrafica.data_terza_scadenza_entry.set_text("")
            self.anagrafica.importo_terza_scadenza_entry.set_text("")
#            self.anagrafica.terzo_pagamento_entry.set_text("")
            self.anagrafica.data_pagamento_terza_scadenza_entry.set_text("")

    def attiva_quarta_scadenza(self, action, disable = True):
        """
        Attiva i campi relativi alla prima, seconda, terza e quarta scadenza nella tab Pagamenti.
        Se action e` False, disattiva e pulisce i campi riguardanti la quarta scadenza.
        """

        if disable:
            self.anagrafica.data_quarta_scadenza_entry.set_sensitive(action)
            self.anagrafica.importo_quarta_scadenza_entry.set_sensitive(action)
#            self.anagrafica.quarto_pagamento_entry.set_sensitive(action)
            self.anagrafica.data_pagamento_quarta_scadenza_entry.set_sensitive(action)
        if not action:
            self.anagrafica.data_quarta_scadenza_entry.set_text("")
            self.anagrafica.importo_quarta_scadenza_entry.set_text("")
#            self.anagrafica.quarto_pagamento_entry.set_text("")
            self.anagrafica.data_pagamento_quarta_scadenza_entry.set_text("")

    def dividi_importo(self):
        """
        Divide l'importo passato per il numero delle scadenze. Se viene passato un argomento, che indica
        il valore di una rata, ricalcola gli altri tenendo conto del valore modificato
        TODO: Passare i valori valuta a mN
        """

        importodoc = float(self.anagrafica.totale_scontato_riepiloghi_label.get_text() or 0)
        if importodoc == 0:
            return
        acconto = float(self.anagrafica.importo_acconto_scadenza_entry.get_text() or 0)
        importo_primo_doc = float(self.anagrafica.importo_primo_documento_entry.get_text() or 0)
        importo_secondo_doc = float(self.anagrafica.importo_secondo_documento_entry.get_text() or 0)
        importotot = importodoc - acconto - importo_primo_doc - importo_secondo_doc

        pagamenti = self.IsPagamentoMultiplo(self.anagrafica.id_pagamento_customcombobox.combobox)
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

        self.anagrafica.importo_prima_scadenza_entry.set_text("%.2f" % importorate[0])
        self.anagrafica.importo_seconda_scadenza_entry.set_text("%.2f" % importorate[1])
        self.anagrafica.importo_terza_scadenza_entry.set_text("%.2f" % importorate[2])
        self.anagrafica.importo_quarta_scadenza_entry.set_text("%.2f" % importorate[3])

        if n_pagamenti == 3:
            self.anagrafica.importo_quarta_scadenza_entry.set_text("")
        elif n_pagamenti == 2:
            self.anagrafica.importo_terza_scadenza_entry.set_text("")
            self.anagrafica.importo_quarta_scadenza_entry.set_text("")
        elif n_pagamenti == 1:
            self.anagrafica.importo_seconda_scadenza_entry.set_text("")
            self.anagrafica.importo_terza_scadenza_entry.set_text("")
            self.anagrafica.importo_quarta_scadenza_entry.set_text("")

    def controlla_rate_scadenza(self, messaggio):
        """
        Controlla che gli importi inseriti nelle scadenze siano corrispondenti
        al totale del documento. Ritorna False se c'e` un errore,
        True se e` tutto corretto.
        """

        importotot = float(self.anagrafica.totale_scontato_riepiloghi_label.get_text() or 0)
        if importotot == 0:
            return
        importo_immesso_acconto = float(self.anagrafica.importo_acconto_scadenza_entry.get_text() or 0)
        importo_immesso_prima = float(self.anagrafica.importo_prima_scadenza_entry.get_text() or 0)
        importo_immesso_seconda = float(self.anagrafica.importo_seconda_scadenza_entry.get_text() or 0)
        importo_immesso_terza = float(self.anagrafica.importo_terza_scadenza_entry.get_text() or 0)
        importo_immesso_quarta = float(self.anagrafica.importo_quarta_scadenza_entry.get_text() or 0)

        importo_primo_riferimento = float(self.anagrafica.importo_primo_documento_entry.get_text() or 0)
        importo_secondo_riferimento = float(self.anagrafica.importo_secondo_documento_entry.get_text() or 0)

        differenza_importi = (importo_immesso_acconto + importo_immesso_prima + importo_immesso_seconda +
            importo_immesso_terza + importo_immesso_quarta + importo_primo_riferimento +
            importo_secondo_riferimento) - importotot
        if differenza_importi == 0 - importotot:
            if messaggio:
                self.anagrafica.showMessage("Importo delle rate non inserite")
            return True

        elif differenza_importi != 0:
            if messaggio:
                self.anagrafica.showMessage("""ATTENZIONE!
La somma degli importi che Lei ha inserito come rate nelle scadenze
non corrisponde al totale del documento. La invitiamo a ricontrollare.
Ricordiamo inoltre che allo stato attuale e` impossibile salvare il documento.
Per l'esattezza, l'errore e` di %.2f""" % differenza_importi)
            return False
        else:
            if messaggio:
                self.anagrafica.showMessage("Gli importi inseriti come rate corrispondono con il totale del documento")
            return True

    def getDocumentoCollegato(self, numerodocumento):
        """
        Trova il documento in base al numero e ritorna un cursore al documento stesso.
        """

        if self.anagrafica._tipoPersonaGiuridica == "cliente":
            idCliente = self.anagrafica.id_persona_giuridica_customcombobox.getId()
            idFornitore = None
            tipoDocumento = "Nota di credito a cliente"
        elif self.anagrafica._tipoPersonaGiuridica == "fornitore":
            idCliente = None
            idFornitore = self.anagrafica.id_persona_giuridica_customcombobox.getId()
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
            self.anagrafica.showMessage("Sono stati trovati piu` di un documento. Hai scovato un bug :D")
            return False
        elif len(result) == 0:
            self.anagrafica.showMessage("Non e' stato trovato nessun documento con il numero specificato")
            return False
        else:
            return result

    def impostaDocumentoCollegato(self, numerodocumento):
        """
        Imposta il documento indicato dall'utente come collegato al documento
        in creazione.
        """

        documento = self.getDocumentoCollegato(numerodocumento)
        if documento == False:
            return False
        daoTestata = TestataDocumento().getRecord(id=documento[0].id)
        tipo_documento = daoTestata.operazione
        totale_pagato = daoTestata.totale_pagato
        totale_sospeso = daoTestata.totale_sospeso
        numero_documento = daoTestata.numero
        data_documento = daoTestata.data_documento

        if totale_sospeso != 0:
            self.anagrafica.showMessage("""Attenzione. Risulta che il documento da Lei scelto abbia ancora
un importo in sospeso. Il documento, per poter essere collegato, deve essere completamente saldato""")
            return False

        return totale_pagato

    def ricalcola_sospeso_e_pagato(self):
        """
        Ricalcola i totali sospeso e pagato in base alle
        scadenze ancora da saldare
        """

        if self.anagrafica.data_pagamento_prima_scadenza_entry.get_text() != "":
            totalepagato = float(self.anagrafica.importo_acconto_scadenza_entry.get_text() or '0')
            totalepagato = totalepagato + float(self.anagrafica.importo_prima_scadenza_entry.get_text() or '0')
            totalesospeso = float(0)
        else:
            totalepagato = float(self.anagrafica.importo_acconto_scadenza_entry.get_text() or '0')
            totalesospeso = float(self.anagrafica.importo_prima_scadenza_entry.get_text() or '0')
            self.anagrafica.stato_label.set_markup('<b><span foreground="#B40000" size="24000">APERTO</span></b>')
        if self.anagrafica.data_pagamento_seconda_scadenza_entry.get_text() != "":
            totalepagato = totalepagato + float(self.anagrafica.importo_seconda_scadenza_entry.get_text() or '0')
        else:
            totalesospeso = totalesospeso + float(self.anagrafica.importo_seconda_scadenza_entry.get_text() or '0')
        if self.anagrafica.data_pagamento_terza_scadenza_entry.get_text() != "":
            totalepagato = totalepagato + float(self.anagrafica.importo_terza_scadenza_entry.get_text() or '0')
        else:
            totalesospeso = totalesospeso + float(self.anagrafica.importo_terza_scadenza_entry.get_text() or '0')
        if self.anagrafica.data_pagamento_quarta_scadenza_entry.get_text() != "":
            totalepagato = totalepagato + float(self.anagrafica.importo_quarta_scadenza_entry.get_text() or '0')
        else:
            totalesospeso = totalesospeso + float(self.anagrafica.importo_quarta_scadenza_entry.get_text() or '0')

        totalepagato = totalepagato + float(self.anagrafica.importo_primo_documento_entry.get_text() or '0')
        totalepagato = totalepagato + float(self.anagrafica.importo_secondo_documento_entry.get_text() or '0')

        self.anagrafica.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(mN(totalepagato,2))+'</span></b>')

        if totalepagato ==0:
            totalesospeso = float(self.anagrafica.totale_in_pagamenti_label.get_text())
        if totalesospeso == 0:
            totalesospeso = float(self.anagrafica.totale_in_pagamenti_label.get_text()) - totalepagato
        self.anagrafica.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(mN(totalesospeso,2))+'</span></b>')
        if totalepagato == 0 and totalesospeso == 0:
            self.attiva_prima_scadenza(False, True)
            self.attiva_seconda_scadenza(False, True)
            self.attiva_terza_scadenza(False, True)
            self.attiva_quarta_scadenza(False, True)
            self.anagrafica.stato_label.set_markup('<b><span foreground="#B40000" size="24000">APERTO</span></b>')
        if totalepagato == float(self.anagrafica.totale_in_pagamenti_label.get_text()) and\
                        self.anagrafica.stato_label.get_text() == "APERTO" and \
                        self.anagrafica.notebook.get_current_page() ==3:
            msg = """Attenzione! L'importo in sospeso è pari a 0 e
l'importo pagato è uguale al totale documento.
Procedere con la "chiusura" del Pagamento?"""
            procedi = YesNoDialog(msg=msg, transient=None)
            if procedi:
                self.anagrafica.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')

    def attiva_scadenze(self):
        """
        Attiva le scadenze necessarie in base alle scadenze passate; il valore passato
        deve essere necessariamente ottenuto dalla funzione IsPagamentoMultiplo.
        Chiama inoltre apposite istanze di dividi_importo() per suddividere
        l'importo totale nelle varie rate.
        """

        if self.anagrafica.totale_scontato_riepiloghi_label.get_text() == "-":
            return 1

        scadenze = self.IsPagamentoMultiplo(self.anagrafica.id_pagamento_customcombobox.combobox)
        data_doc = stringToDate(self.anagrafica.data_documento_entry.get_text())
        importotot = float(self.anagrafica.totale_scontato_riepiloghi_label.get_text())


        if type(scadenze) == list:
            numeroscadenze = (len(scadenze) - 1) / 2 # Trovo il numero delle scadenze contando gli elementi
                                                     # della variabile passata, sottraendo il caratteee di
                                                     # Fine Mese e dividendo per due ( vedere la doc di
                                                     # IsPagamentoMultiplo per maggiori informazioni )
            paga = findStrFromCombobox(self.anagrafica.id_pagamento_customcombobox.combobox,2)
            if scadenze[len(scadenze)-1] != "FM":
                fine_mese = False
            else:
                fine_mese = True

#            self.anagrafica.primo_pagamento_entry.set_text(scadenze[0] + scadenze[1] + " gg")

            findComboboxRowFromStr(self.anagrafica.id_pagamento_prima_scadenza_customcombobox.combobox, paga,2)
            if numeroscadenze == 1:
                self.attiva_prima_scadenza(True, True)
                self.attiva_seconda_scadenza(False, True)
                self.attiva_terza_scadenza(False, True)
                self.attiva_quarta_scadenza(False, True)
                self.anagrafica.data_prima_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[1]), fine_mese)))
            elif numeroscadenze == 2:
                self.attiva_seconda_scadenza(True, True)
                self.attiva_prima_scadenza(True, True)
                self.attiva_terza_scadenza(False, True)
                self.attiva_quarta_scadenza(False, True)
                self.anagrafica.data_prima_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[1]), fine_mese)))
                self.anagrafica.data_seconda_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[3]), fine_mese)))
#                self.anagrafica.secondo_pagamento_entry.set_text(scadenze[0] + scadenze[3] + " gg")
                findComboboxRowFromStr(self.anagrafica.id_pagamento_seconda_scadenza_customcombobox.combobox, paga,2)
            elif numeroscadenze == 3:
                self.attiva_terza_scadenza(True, True)
                self.attiva_seconda_scadenza(True, True)
                self.attiva_prima_scadenza(True, True)
                self.attiva_quarta_scadenza(False, True)
                self.anagrafica.data_prima_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[1]), fine_mese)))
                self.anagrafica.data_seconda_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[3]), fine_mese)))
                self.anagrafica.data_terza_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[5]), fine_mese)))
#                self.anagrafica.secondo_pagamento_entry.set_text(scadenze[0] + scadenze[3] + " gg")
                findComboboxRowFromStr(self.anagrafica.id_pagamento_seconda_scadenza_customcombobox.combobox, paga,2)
#                self.anagrafica.terzo_pagamento_entry.set_text(scadenze[0] + scadenze[5] + " gg")
                findComboboxRowFromStr(self.anagrafica.id_pagamento_terza_scadenza_customcombobox.combobox, paga,2)
            elif numeroscadenze == 4:
                self.attiva_quarta_scadenza(True, True)
                self.attiva_seconda_scadenza(True, True)
                self.attiva_terza_scadenza(True, True)
                self.attiva_prima_scadenza(True, True)
                self.anagrafica.data_quarta_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[7]), fine_mese)))
                self.anagrafica.data_terza_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[5]), fine_mese)))
                self.anagrafica.data_prima_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[1]), fine_mese)))
                self.anagrafica.data_seconda_scadenza_entry.set_text(dateToString(getScadenza(data_doc, int(scadenze[3]), fine_mese)))
#                self.anagrafica.secondo_pagamento_entry.set_text(scadenze[0] + scadenze[3] + " gg")
                findComboboxRowFromStr(self.anagrafica.id_pagamento_seconda_scadenza_customcombobox.combobox, paga,2)
#                self.anagrafica.terzo_pagamento_entry.set_text(scadenze[0] + scadenze[5] + " gg")
                findComboboxRowFromStr(self.anagrafica.id_pagamento_terza_scadenza_customcombobox.combobox, paga,2)
#                self.anagrafica.quarto_pagamento_entry.set_text(scadenze[0] + scadenze[7] + " gg")
                findComboboxRowFromStr(self.anagrafica.id_pagamento_quarta_scadenza_customcombobox.combobox, paga,2)
            else:
                print "Numero troppo alto di scadenze; Funzione non ancora implementata. Manda un bug report"
        else:
            self.attiva_prima_scadenza(True, True)
            self.anagrafica.data_prima_scadenza_entry.set_text(dateToString(data_doc))
            findComboboxRowFromStr(self.anagrafica.id_pagamento_prima_scadenza_customcombobox.combobox, scadenze,2)
#            self.anagrafica.primo_pagamento_entry.set_text(scadenze)

    def IsPagamentoMultiplo(self, combobox):
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

    def getScadenze(self):
        if  self.anagrafica.dao.scadenze:
            for scadenza in self.anagrafica.dao.scadenze:
                if scadenza.numero_scadenza == 0:
                    self.anagrafica.data_acconto_entry.set_text(dateToString(scadenza.data) or '')
                    self.anagrafica.importo_acconto_scadenza_entry.set_text(str(scadenza.importo or ''))
                    findComboboxRowFromStr(self.anagrafica.id_pagamento_acconto_customcombobox.combobox, scadenza.pagamento,2)
                    self.anagrafica.data_pagamento_acconto_entry.set_text(dateToString
                        (scadenza.data_pagamento or ''))
                elif scadenza.numero_scadenza == 1:
                    self.anagrafica.data_prima_scadenza_entry.set_text(dateToString(scadenza.data) or '')
                    self.anagrafica.importo_prima_scadenza_entry.set_text(str(scadenza.importo or ''))
                    findComboboxRowFromStr(self.anagrafica.id_pagamento_prima_scadenza_customcombobox.combobox, scadenza.pagamento,2)
                    self.anagrafica.data_pagamento_prima_scadenza_entry.set_text(dateToString
                        (scadenza.data_pagamento or ''))
                elif scadenza.numero_scadenza == 2:
                    self.anagrafica.data_seconda_scadenza_entry.set_text(dateToString
                        (scadenza.data or ''))
                    self.anagrafica.importo_seconda_scadenza_entry.set_text(str(scadenza.importo or ''))
                    findComboboxRowFromStr(self.anagrafica.id_pagamento_seconda_scadenza_customcombobox.combobox, scadenza.pagamento,2)
                    self.anagrafica.data_pagamento_seconda_scadenza_entry.set_text(dateToString
                        (scadenza.data_pagamento or ''))
                elif scadenza.numero_scadenza == 3:
                    self.anagrafica.data_terza_scadenza_entry.set_text(dateToString
                        (scadenza.data or ''))
                    self.anagrafica.importo_terza_scadenza_entry.set_text(str(scadenza.importo or ''))
                    findComboboxRowFromStr(self.anagrafica.id_pagamento_terza_scadenza_customcombobox.combobox, scadenza.pagamento,2)
                    self.anagrafica.data_pagamento_terza_scadenza_entry.set_text(dateToString
                        (scadenza.data_pagamento or ''))
                elif scadenza.numero_scadenza == 4:
                    self.anagrafica.data_quarta_scadenza_entry.set_text(dateToString
                        (scadenza.data or ''))
                    self.anagrafica.importo_quarta_scadenza_entry.set_text(str(scadenza.importo or ''))
                    findComboboxRowFromStr(self.anagrafica.id_pagamento_quarta_scadenza_customcombobox.combobox, scadenza.pagamento,2)
                    self.anagrafica.data_pagamento_quarta_scadenza_entry.set_text(dateToString
                        (scadenza.data_pagamento or ''))

        if self.anagrafica.importo_acconto_scadenza_entry.get_text() != '':
            self.attiva_prima_scadenza(True,True)
        if self.anagrafica.importo_prima_scadenza_entry.get_text() != '':
            self.attiva_prima_scadenza(True,True)
        if self.anagrafica.importo_seconda_scadenza_entry.get_text() != '':
            self.attiva_seconda_scadenza(True,True)
        if self.anagrafica.importo_terza_scadenza_entry.get_text() != '':
            self.attiva_terza_scadenza(True,True)
        if self.anagrafica.importo_quarta_scadenza_entry.get_text() != '':
            self.attiva_quarta_scadenza(True,True)
        if self.anagrafica.dao.documento_saldato:
            self.anagrafica.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')
        else:
            self.anagrafica.stato_label.set_markup('<b><span foreground="#B40000" size="24000">APERTO</span></b>')
        self.anagrafica.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(
            self.anagrafica.dao.totale_pagato or 0)+'</span></b>')

        if (self.anagrafica.dao.totale_sospeso is None)  or (self.anagrafica.dao.totale_sospeso == 0):
            totaleSospeso = Decimal(self.anagrafica.totale_scontato_riepiloghi_label.get_text()) - Decimal(self.anagrafica.dao.totale_pagato or 0)
        else:
            totaleSospeso = self.anagrafica.dao.totale_sospeso

        self.anagrafica.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(
            totaleSospeso)+'</span></b>')
        if self.anagrafica.dao.id_primo_riferimento != None:
            doc = TestataDocumento().getRecord(id=self.anagrafica.dao.id_primo_riferimento)
            self.anagrafica.importo_primo_documento_entry.set_text(str(doc.totale_pagato) or '')
            self.anagrafica.numero_primo_documento_entry.set_text(str(doc.numero) or '')
            self.anagrafica.importo_secondo_documento_entry.set_sensitive(True)
            self.anagrafica.numero_secondo_documento_entry.set_sensitive(True)
            self.anagrafica.seleziona_seconda_nota_button.set_sensitive(True)
            if self.anagrafica.dao.id_secondo_riferimento != None:
                doc = TestataDocumento().getRecord(id=self.anagrafica.dao.id_secondo_riferimento)
                self.anagrafica.importo_secondo_documento_entry.set_text(str(doc.totale_pagato) or '')
                self.anagrafica.numero_secondo_documento_entry.set_text(str(doc.numero) or '')
            else:
                self.anagrafica.importo_secondo_documento_entry.set_text('')
                self.anagrafica.numero_secondo_documento_entry.set_text('')
        else:
            self.anagrafica.importo_primo_documento_entry.set_text('')
            self.anagrafica.importo_secondo_documento_entry.set_text('')
            self.anagrafica.numero_primo_documento_entry.set_text('')
            self.anagrafica.numero_secondo_documento_entry.set_text('')

    def saveScadenze(self):
        """ Di fatto è la parte che gestisce il salvataggio dei dati
        di pagamento
        TODO: aggiungere la cancellazione se vengono trovate più righe?"""
        self.anagrafica.dao.totale_pagato = float(self.anagrafica.totale_pagato_scadenza_label.get_text())
        self.anagrafica.dao.totale_sospeso = float(self.anagrafica.totale_sospeso_scadenza_label.get_text())
        if self.anagrafica.stato_label.get_text() == "PAGATO":
            self.anagrafica.dao.documento_saldato = True
        else:
            self.anagrafica.dao.documento_saldato = False
        self.anagrafica.dao.ripartire_importo =  self.anagrafica.primanota_check.get_active()
        scadenze = []
#        accontoDao0= TestataDocumentoScadenza().select(idTestataDocumento=self.anagrafica.dao.id, numeroScadenza=0)
        if self.anagrafica.data_acconto_entry.get_text() != "":
#            if accontoDao0:
#                daoTestataDocumentoScadenza = accontoDao0[0]
#            else:
            daoTestataDocumentoScadenza = TestataDocumentoScadenza()
            daoTestataDocumentoScadenza.id_testata_documento = self.anagrafica.dao.id
            if stringToDate(self.anagrafica.data_acconto_entry.get_text()) =="":
                obligatoryField(self.anagrafica.dialogTopLevel,
                    self.anagrafica.data_acconto_entry,
                    'Inserire una data acconto!')
            daoTestataDocumentoScadenza.data = stringToDate(self.anagrafica.data_acconto_entry.get_text())
            daoTestataDocumentoScadenza.importo = float(self.anagrafica.importo_acconto_scadenza_entry.get_text() or '0')
            idpag0 = findIdFromCombobox(self.anagrafica.id_pagamento_acconto_customcombobox.combobox)
            if idpag0:
                p0 = Pagamento().getRecord(id=idpag0)
                daoTestataDocumentoScadenza.pagamento = p0.denominazione
            else:
                obligatoryField(self.anagrafica.dialogTopLevel,
                        self.anagrafica.id_pagamento_acconto_customcombobox.combobox,
                        'Inserire una forma di pagamento!')
            daoTestataDocumentoScadenza.data_pagamento = daoTestataDocumentoScadenza.data
            daoTestataDocumentoScadenza.numero_scadenza = 0
            scadenze.append(daoTestataDocumentoScadenza)
        if self.anagrafica.data_prima_scadenza_entry.get_text() != "":
            daoTestataDocumentoScadenza = TestataDocumentoScadenza()
            daoTestataDocumentoScadenza.id_testata_documento = self.anagrafica.dao.id
            if stringToDate(self.anagrafica.data_prima_scadenza_entry.get_text()) =="":
                obligatoryField(self.anagrafica.dialogTopLevel,
                    self.anagrafica.data_prima_scadenza_entry,
                    'Inserire una data!')
            daoTestataDocumentoScadenza.data = stringToDate(self.anagrafica.data_prima_scadenza_entry.get_text())
            daoTestataDocumentoScadenza.importo = float(self.anagrafica.importo_prima_scadenza_entry.get_text() or '0')
            idpag1 = findIdFromCombobox(self.anagrafica.id_pagamento_prima_scadenza_customcombobox.combobox)
            if idpag1:
                p1 = Pagamento().getRecord(id=idpag1)
                daoTestataDocumentoScadenza.pagamento = p1.denominazione
            else:
                obligatoryField(self.anagrafica.dialogTopLevel,
                    self.anagrafica.id_pagamento_acconto_customcombobox.combobox,
                    'Inserire una forma di pagamento!')
            daoTestataDocumentoScadenza.data_pagamento = stringToDate(
                    self.anagrafica.data_pagamento_prima_scadenza_entry.get_text())
            daoTestataDocumentoScadenza.numero_scadenza = 1
            scadenze.append(daoTestataDocumentoScadenza)
        if self.anagrafica.data_seconda_scadenza_entry.get_text() != "":
            daoTestataDocumentoScadenza = TestataDocumentoScadenza()
            daoTestataDocumentoScadenza.id_testata_documento = self.anagrafica.dao.id
            if stringToDate(self.anagrafica.data_seconda_scadenza_entry.get_text()) =="":
                obligatoryField(self.anagrafica.dialogTopLevel,
                    self.anagrafica.data_seconda_scadenza_entry,
                    'Inserire una data!')
            daoTestataDocumentoScadenza.data = stringToDate(
                    self.anagrafica.data_seconda_scadenza_entry.get_text())
            daoTestataDocumentoScadenza.importo = float(
                    self.anagrafica.importo_seconda_scadenza_entry.get_text() or '0')
            idpag2 = findIdFromCombobox(self.anagrafica.id_pagamento_seconda_scadenza_customcombobox.combobox)
            if idpag2:
                p2 = Pagamento().getRecord(id=idpag2)
                daoTestataDocumentoScadenza.pagamento = p2.denominazione
            else:
                obligatoryField(self.anagrafica.dialogTopLevel,
                    self.anagrafica.id_pagamento_acconto_customcombobox.combobox,
                    'Inserire una forma di pagamento!')
            daoTestataDocumentoScadenza.data_pagamento = stringToDate(
                    self.anagrafica.data_pagamento_seconda_scadenza_entry.get_text())
            daoTestataDocumentoScadenza.numero_scadenza = 2
            scadenze.append(daoTestataDocumentoScadenza)
        if self.anagrafica.data_terza_scadenza_entry.get_text() != "":
            daoTestataDocumentoScadenza = TestataDocumentoScadenza()
            daoTestataDocumentoScadenza.id_testata_documento = self.anagrafica.dao.id
            if stringToDate(self.anagrafica.data_terza_scadenza_entry.get_text()) =="":
                obligatoryField(self.anagrafica.dialogTopLevel,
                    self.anagrafica.data_terza_scadenza_entry,
                    'Inserire una data!')
            daoTestataDocumentoScadenza.data = stringToDate(
                    self.anagrafica.data_terza_scadenza_entry.get_text())
            daoTestataDocumentoScadenza.importo = float(
                    self.anagrafica.importo_terza_scadenza_entry.get_text() or '0')
            idpag3 = findIdFromCombobox(self.anagrafica.id_pagamento_terza_scadenza_customcombobox.combobox)
            if idpag3:
                p3 = Pagamento().getRecord(id=idpag3)
                daoTestataDocumentoScadenza.pagamento = p3.denominazione
            else:
                obligatoryField(self.anagrafica.dialogTopLevel,
                    self.anagrafica.id_pagamento_acconto_customcombobox.combobox,
                    'Inserire una forma di pagamento!')
            daoTestataDocumentoScadenza.data_pagamento = stringToDate(
                    self.anagrafica.data_pagamento_terza_scadenza_entry.get_text())
            daoTestataDocumentoScadenza.numero_scadenza = 3
            scadenze.append(daoTestataDocumentoScadenza)
        if self.anagrafica.data_quarta_scadenza_entry.get_text() != "":
            daoTestataDocumentoScadenza = TestataDocumentoScadenza()
            daoTestataDocumentoScadenza.id_testata_documento = self.anagrafica.dao.id
            if stringToDate(self.anagrafica.data_quarta_scadenza_entry.get_text()) =="":
                obligatoryField(self.anagrafica.dialogTopLevel,
                    self.anagrafica.data_quarta_scadenza_entry,
                    'Inserire una data!')
            daoTestataDocumentoScadenza.data = stringToDate(
                    self.anagrafica.data_quarta_scadenza_entry.get_text())
            daoTestataDocumentoScadenza.importo = float(
                    self.anagrafica.importo_quarta_scadenza_entry.get_text() or '0')
            idpag4 = findIdFromCombobox(self.anagrafica.id_pagamento_quarta_scadenza_customcombobox.combobox)
            if idpag4:
                p4 = Pagamento().getRecord(id=idpag4)
                daoTestataDocumentoScadenza.pagamento = p4.denominazione
            else:
                obligatoryField(self.anagrafica.dialogTopLevel,
                    self.anagrafica.id_pagamento_acconto_customcombobox.combobox,
                    'Inserire una forma di pagamento!')
            daoTestataDocumentoScadenza.data_pagamento = stringToDate(
                    self.anagrafica.data_pagamento_quarta_scadenza_entry.get_text())
            daoTestataDocumentoScadenza.numero_scadenza = 4
            scadenze.append(daoTestataDocumentoScadenza)
        self.anagrafica.dao.scadenze = scadenze

        #TODO: finire di sistemare questa parte ......

        doc = self.anagrafica.numero_primo_documento_entry.get_text()
        if doc != "" and doc != "0":
            documentocollegato = self.getDocumentoCollegato(int(doc))
            self.anagrafica.dao.id_primo_riferimento = documentocollegato[0].id
            doc2 = self.anagrafica.numero_secondo_documento_entry.get_text()
            if doc2 != "" and doc2 != "0":
                documentocollegato = self.getDocumentoCollegato(int(doc2))
                self.anagrafica.dao.id_secondo_riferimento = documentocollegato[0].id
