# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

import datetime


from promogest.ui.gtk_compat import *
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget

from promogest.modules.Pagamenti.ui import AnagraficadocumentiPagamentExt
from promogest.ui.widgets.PagamentoWidget import PagamentoWidget

from promogest.dao.Pagamento import Pagamento
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza


class PagamentiNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn):
        GladeWidget.__init__(self, 'pagamenti_vbox',
                             'Pagamenti/gui/pagamenti_notebook.glade',
                             isModule=True)
        self.ana = mainnn
        # lista di scadenze
        self.rate = []
        # assegno un'istanza di PagamentoWidget se ho un acconto, None altrimenti
        self.acconto = None
        self.draw()

    def draw(self):
        fillComboboxPagamenti(self.id_pagamento_customcombobox.combobox)
        self.id_pagamento_customcombobox.connect('clicked',
            on_id_pagamento_customcombobox_clicked)
        self.id_pagamento_customcombobox.combobox.connect('changed',
            self.id_pagamento_customcombobox_changed)
        fillComboboxBanche(self.id_banca_customcombobox.combobox)
        self.id_banca_customcombobox.connect('clicked',
            on_id_banca_customcombobox_clicked)
        self.clear()

    def id_pagamento_customcombobox_changed(self, combobox):
        if self.ana._loading:
            return
        self.on_calcola_importi_scadenza_button_clicked(None)

    def clear(self):
        """

        """
        self.id_pagamento_customcombobox.combobox.set_active(-1)
        self.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">0</span></b>')
        self.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">0</span></b>')
        self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')
        self.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+_("NESSUNO?")+'</span></b>')
        self.importo_primo_documento_entry.set_text('')
        self.importo_secondo_documento_entry.set_text('')
        self.numero_primo_documento_entry.set_text('')
        self.numero_secondo_documento_entry.set_text('')
        if self.acconto:
            self.acconto_scheda_togglebutton.set_active(False)
        if len(self.rate) > 0:
            for i in self.rate:
                self.scadenze_notebook.remove_page(0)
            self.rate = []

    def on_aggiungi_rate_button_clicked(self, button):
        """

        """
        numero = len(self.rate) + 1
        pag_w = PagamentoWidget(self.ana, 'rata ' + str(numero))
        dao = pag_w.get()
        dao.data = datetime.datetime.now()
        pag_w.fill(dao)
        self.rate.append(pag_w)
        self.scadenze_notebook.insert_page(pag_w.getTopLevel(), gtk.Label(pag_w.label), -1)
        self.scadenze_notebook.set_current_page(-1)

    def on_rimuovi_rate_button_clicked(self, button):
        ''' Elimina una scheda di pagamento e la relativa rata
        '''
        if len(self.rate) > 0:
            if YesNoDialog(msg='Rimuovere la scadenza?'):
                self.rate.pop()
                self.scadenze_notebook.remove_page(-1)
        else:
            messageInfo('Non ci sono altre scadenze da rimuovere.')

    def on_aggiorna_pagamenti_button_clicked(self, button):
        """
        Aggiorna la parte dei pagamenti
        """
        self.ricalcola_sospeso_e_pagato()

    def on_seleziona_prima_nota_button_clicked(self, button):
        """
        Seleziona la prima nota da utilizzare come riferimento
        """
        if self.ana.numero_primo_documento_entry.get_text() != "":
            response = AnagraficadocumentiPagamentExt.impostaDocumentoCollegato(int(self.ana.numero_primo_documento_entry.get_text()))
        else:
            messageInfo(msg="Inserisci il numero del documento")
            response = False

        if response:
            self.ana.importo_primo_documento_entry.set_text(str(response))
            AnagraficadocumentiPagamentExt.dividi_importo(self.ana)
            AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)
            self.ana.numero_secondo_documento_entry.set_sensitive(True)
            self.ana.seleziona_seconda_nota_button.set_sensitive(True)
            self.ana.importo_secondo_documento_entry.set_sensitive(True)

    def on_seleziona_seconda_nota_button_clicked(self, button):
        if self.ana.numero_secondo_documento_entry.get_text() != "":
            response = AnagraficadocumentiPagamentExt.impostaDocumentoCollegato(int(self.ana.numero_secondo_documento_entry.get_text()))
        else:
            messageInfo(msg="Inserisci il numero del documento")
            response = False
        if response:
            self.ana.importo_primo_documento_entry.set_text(str(response))
            AnagraficadocumentiPagamentExt.dividi_importo(self.ana)
            AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)

    def on_calcola_importi_scadenza_button_clicked(self, button):
        """
        Calcola importi scadenza pagamenti
        """
        id_pag = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
        if id_pag == -1 or id_pag==0 or id_pag==None:
            messageInfo(msg=_("NESSUN METODO DI PAGAMENTO SELEZIONATO\n NON POSSO AGIRE"))
            return
        pago = Pagamento().getRecord(id=id_pag)
        if pago:
            self.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str(pago.denominazione)+'</span></b>')
        else:
            self.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str(_("NESSUNO?"))+'</span></b>')
        if self.ana.dao.documento_saldato:
            msg = _('Attenzione! Stai per riaprire un documento già saldato.\n Continuare ?')
            if YesNoDialog(msg=msg, transient=self.ana.dialogTopLevel):
                self.stato_label.set_markup(_('<b><span foreground="#B40000" size="24000">APERTO</span></b>'))
            else:
                return
        self.attiva_scadenze()
        self.dividi_importo()
        self.ricalcola_sospeso_e_pagato()

    def on_chiudi_pagamento_documento_button_clicked(self, button):
        """
        Chiude un pagamento
        """
        acconto = 0
        importo_immesso = 0
        for rata in self.rate:
            daoTDS = rata.get()
            importo_immesso += daoTDS.importo

        if self.acconto:
            daoAcconto = self.acconto.get()
            acconto = daoAcconto.importo

        if acconto == 0 or importo_immesso == 0 or importo_immesso < float(self.totale_in_pagamenti_label.get_text()):
            msg = _('Chiusura di un documento con pagamenti nulli o parziali.\n Continuare?')
            if YesNoDialog(msg=msg, transient=None):
                self.stato_label.set_markup('<b><span foreground="#338000" size="24000">'+_('PAGATO')+'</span></b>')
                self.chiudi_pagamento_documento_button.set_sensitive(False)
                self.apri_pagamento_documento_button.set_sensitive(True)
        else:
            self.stato_label.set_markup('<b><span foreground="#338000" size="24000">'+_('PAGATO')+'</span></b>')

    def on_apri_pagamento_documento_button_clicked(self, button):
        ''' Apre il pagamento
        '''
        msg=_('Attenzione! Stai per riaprire un documento considerato già pagato.\n Continuare?')
        if YesNoDialog(msg=msg):
            self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')
            self.apri_pagamento_documento_button.set_sensitive(False)
            self.chiudi_pagamento_documento_button.set_sensitive(True)

    def on_acconto_scheda_togglebutton_toggled(self, button):
        """

        """
        if not self.acconto:
            self.acconto_scheda_togglebutton.set_label(_('Acconto'))
            self.acconto = PagamentoWidget(self.ana, 'Acconto')
            dao = self.acconto.get()
            dao.data = datetime.datetime.now()
            self.acconto.fill(dao)
            self.scadenze_notebook.insert_page(self.acconto.getTopLevel(), gtk.Label(self.acconto.label), 0)
            self.scadenze_notebook.set_current_page(0)
        else:
            self.acconto_scheda_togglebutton.set_label(_('Acconto'))
            self.scadenze_notebook.remove_page(0)
            self.scadenze_notebook.set_current_page(-1)
            self.acconto = None

    def on_pulisci_scadenza_button_clicked(self, button):
        """
        Pulisce tutti i campi relativi alla scheda pagamenti
        """
        msg = _('Stai per rimuovere i riferimenti già inseriti. Continuare?')
        if YesNoDialog(msg=msg):
            self.clear()
            self.ricalcola_sospeso_e_pagato()

    def on_controlla_rate_scadenza_button_clicked(self, button):
        """ bottone che controlla le rate scadenza """
        self.controlla_rate_scadenza(self, True)

    def getScadenze(self):
        if self.ana.dao.scadenze:
            for scadenza in self.ana.dao.scadenze:
                if scadenza.numero_scadenza == 0:
                    self.acconto = None
                    self.acconto_scheda_togglebutton.set_active(True)
                    self.acconto.fill(scadenza)
                else:
                    self.on_aggiungi_rate_button_clicked(None)
                    self.rate[-1].fill(scadenza)

            if self.ana.dao.documento_saldato:
                self.stato_label.set_markup('<b><span foreground="#338000" size="24000">'+_('PAGATO')+'</span></b>')
            else:
            self.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(
                mN(self.ana.dao.totale_pagato) or 0)+'</span></b>')
                self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')

            if (self.ana.dao.totale_sospeso is None)  or (self.ana.dao.totale_sospeso == 0):
                totaleSospeso = Decimal(str(self.ana.totale_scontato_riepiloghi_label.get_text() or 0)) - Decimal(str(self.ana.dao.totale_pagato or 0))
            else:
                totaleSospeso = self.ana.dao.totale_sospeso

            self.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(
                mN(totaleSospeso))+'</span></b>')
            if self.ana.dao.id_primo_riferimento != None:
                doc = TestataDocumento().getRecord(id=self.ana.dao.id_primo_riferimento)
                self.importo_primo_documento_entry.set_text(str(doc.totale_pagato) or '')
                self.numero_primo_documento_entry.set_text(str(doc.numero) or '')
                self.importo_secondo_documento_entry.set_sensitive(True)
                self.numero_secondo_documento_entry.set_sensitive(True)
                self.seleziona_seconda_nota_button.set_sensitive(True)
                if self.ana.dao.id_secondo_riferimento != None:
                    doc = TestataDocumento().getRecord(id=self.ana.dao.id_secondo_riferimento)
                    self.importo_secondo_documento_entry.set_text(str(doc.totale_pagato) or '')
                    self.numero_secondo_documento_entry.set_text(str(doc.numero) or '')
                else:
                    self.importo_secondo_documento_entry.set_text('')
                    self.numero_secondo_documento_entry.set_text('')
            else:
                self.importo_primo_documento_entry.set_text('')
                self.importo_secondo_documento_entry.set_text('')
                self.numero_primo_documento_entry.set_text('')
                self.numero_secondo_documento_entry.set_text('')

    def saveScadenze(self):
        ''' Gestione del salvataggio dei dati di pagamento
        '''
        #TODO: aggiungere la cancellazione se vengono trovate più righe?
        self.ana.dao.totale_pagato = float(self.totale_pagato_scadenza_label.get_text())
        self.ana.dao.totale_sospeso = float(self.totale_sospeso_scadenza_label.get_text())
        if self.stato_label.get_text() == 'PAGATO':
            self.ana.dao.documento_saldato = True
        else:
            self.ana.dao.documento_saldato = False
        self.ana.dao.ripartire_importo =  self.primanota_check.get_active()
        scadenze = []
        if self.acconto:
            daoTestataDocumentoScadenza = self.acconto.get()
            daoTestataDocumentoScadenza.id_testata_documento = self.ana.dao.id
            daoTestataDocumentoScadenza.numero_scadenza = 0
            daoTestataDocumentoScadenza.data_pagamento = daoTestataDocumentoScadenza.data
            scadenze.append(daoTestataDocumentoScadenza)
        i = 1
        for rata in self.rate:
            daoTestataDocumentoScadenza = rata.get()
            daoTestataDocumentoScadenza.id_testata_documento = self.ana.dao.id
            daoTestataDocumentoScadenza.numero_scadenza = i
            i += 1
            scadenze.append(daoTestataDocumentoScadenza)

        self.ana.dao.scadenze = scadenze

        #TODO: finire di sistemare questa parte ......

        doc = self.numero_primo_documento_entry.get_text()
        if doc != "" and doc != "0":
            documentocollegato = AnagraficadocumentiPagamentExt.getDocumentoCollegato(int(doc))
            self.ana.dao.id_primo_riferimento = documentocollegato[0].id
            doc2 = self.numero_secondo_documento_entry.get_text()
            if doc2 != "" and doc2 != "0":
                documentocollegato = AnagraficadocumentiPagamentExt.getDocumentoCollegato(int(doc2))
                self.ana.dao.id_secondo_riferimento = documentocollegato[0].id

    def attiva_scadenze(self):
        scadenze = AnagraficadocumentiPagamentExt.IsPagamentoMultiplo(self.id_pagamento_customcombobox.combobox)
        data_doc = stringToDate(self.ana.data_documento_entry.get_text())
        importotot = float(self.ana.totale_scontato_riepiloghi_label.get_text())

        if type(scadenze) == list:
            numeroscadenze = (len(scadenze) - 1) / 2
        else:
            numeroscadenze = 1

        if scadenze[len(scadenze)-1] != "FM":
            fine_mese = False
        else:
            fine_mese = True

        # Rimuovo le rate in eccesso e le relative tabs dall'interfaccia
        y = len(self.rate) - numeroscadenze
        if y > 0:
            for i in range(abs(y)):
                self.rate.pop()
                self.scadenze_notebook.remove_page(-1)

        # Aggiungo le rate necessarie per il tipo di pagamento scelto
        i = 1
        for j in range(numeroscadenze):
            daoTDS = TestataDocumentoScadenza()
            idpag = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
            if idpag:
                p = Pagamento().getRecord(id=idpag)
                daoTDS.pagamento = p.denominazione
            if type(scadenze) == list:
                daoTDS.data = dateToString(getScadenza(data_doc, int(scadenze[i]), fine_mese))
                i += 2
            else:
                daoTDS.data = data_doc
            try:
                self.rate[j].fill(daoTDS)
            except IndexError:
                self.on_aggiungi_rate_button_clicked(None)
                self.rate[-1].fill(daoTDS)

    def dividi_importo(self):
        """ Divide l'importo passato per il numero delle scadenze. Se viene passato un argomento, che indica
        il valore di una rata, ricalcola gli altri tenendo conto del valore modificato
        TODO: Passare i valori valuta a mN
        """
        importodoc = float(self.ana.totale_scontato_riepiloghi_label.get_text() or 0)
        if importodoc == float(0):
            return

        acconto = float(0)
        if self.acconto:
            daoAcconto = self.acconto.get()
            acconto = float(daoAcconto.importo or 0)

        importo_primo_doc = float(self.importo_primo_documento_entry.get_text() or 0)
        importo_secondo_doc = float(self.importo_secondo_documento_entry.get_text() or 0)
        importotot = importodoc - acconto - importo_primo_doc - importo_secondo_doc

        pagamenti = AnagraficadocumentiPagamentExt.IsPagamentoMultiplo(self.id_pagamento_customcombobox.combobox)
        importorate = None
        if type(pagamenti) == list:
            n_pagamenti = (len(pagamenti) - 1) / 2
            importorate = dividi_in_rate(importotot, n_pagamenti)
        else:
            n_pagamenti = 1
            importorate = importotot

        i = 0
        for rata in self.rate:
            daoTDS = rata.get()
            if type(importorate) == list:
                daoTDS.importo = importorate[i]
                i += 1
            else:
                daoTDS.importo = importorate
            rata.fill(daoTDS)

        #TODO: mostrare o nascondere l'acconto ?

    def controlla_rate_scadenza(self, messaggio):
        """
        Controlla che gli importi inseriti nelle scadenze siano corrispondenti
        al totale del documento. Ritorna False se c'e` un errore,
        True se e` tutto corretto.
        """

        importotot = float(self.ana.totale_scontato_riepiloghi_label.get_text() or 0)
        if importotot == float(0):
            return

        importo_immesso = float(0)
        for rata in self.rate:
            daoTDS = rata.get()
            importo_immesso += daoTDS.importo

        if self.acconto:
            daoAcconto = self.acconto.get()
            importo_immesso += daoAcconto.importo

        importo_primo_riferimento = float(self.ana.importo_primo_documento_entry.get_text() or 0)
        importo_secondo_riferimento = float(self.ana.importo_secondo_documento_entry.get_text() or 0)

        differenza_importi = (importo_immesso + importo_primo_riferimento +
            importo_secondo_riferimento) - importotot
        if differenza_importi == - importotot:
            if messaggio:
                messageInfo(msg="Importo delle rate non inserite")
            return True

        elif differenza_importi != float(0):
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

    def ricalcola_sospeso_e_pagato(self):
        """ Reimposta i totali saldato e da saldare alla modifica della data di pagamento
            della quarta scadenza
            Ricalcola i totali sospeso e pagato in base alle
            scadenze ancora da saldare
        """
        totale_in_pagamenti_label = float(self.totale_in_pagamenti_label.get_text() or '0')

        acconto = float(0)
        if self.acconto:
            daoAcconto = self.acconto.get()
            acconto = daoAcconto.importo

        totalepagato = acconto
        totalesospeso = float(0)

        for rata in self.rate:
            daoTDS = rata.get()
            if daoTDS.data_pagamento:
                totalepagato += daoTDS.importo
            else:
                totalesospeso += daoTDS.importo

        totalepagato += float(self.importo_primo_documento_entry.get_text() or '0')
        totalepagato += float(self.importo_secondo_documento_entry.get_text() or '0')

        if totalepagato == float(0):
            totalesospeso = totale_in_pagamenti_label
        if totalesospeso == float(0):
            totalesospeso = abs(totale_in_pagamenti_label - totalepagato)

        if totalesospeso > float(0):
            self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')

        self.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(mN(totalepagato, 2))+'</span></b>')
        self.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(mN(totalesospeso, 2))+'</span></b>')

        if totalepagato == float(0) and totalesospeso == float(0):
            self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')

        if str(totalepagato) == str(totale_in_pagamenti_label) and \
                        self.stato_label.get_text() == "APERTO" and \
                        self.ana.notebook.get_current_page() == 3:
            msg = """Attenzione! L'importo in sospeso è pari a 0 e
l'importo pagato è uguale al totale documento.
Procedere con la "chiusura" del Pagamento?"""
            if YesNoDialog(msg=msg, transient=None):
                self.stato_label.set_markup('<b><span foreground="#338000" size="24000">'+_('PAGATO')+'</span></b>')
                self.chiudi_pagamento_documento_button.set_sensitive(False)
                self.apri_pagamento_documento_button.set_sensitive(True)

