# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from promogest import Environment as env
from promogest.ui.GladeWidget import GladeWidget
from promogest.lib.riba import RiBa, Creditore, Debitore
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.Azienda import Azienda
from promogest.dao.Cliente import Cliente
from promogest.lib.utils import messageError, dateToString, leggiOperazione,\
    dataInizioFineMese, pbar, stringToDate, messageInfo, leggiAzienda,\
    leggiBanca, leggiCliente, mN, messageWarning

from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota
from promogest.lib.ibanlib import dividi_iban
from promogest.modules.Pagamenti.dao import TestataDocumentoScadenza
from datetime import datetime
from decimal import Decimal
from promogest.ui.gtk_compat import *
from sqlalchemy.sql import and_, or_
from promogest.lib.HtmlHandler import renderTemplate, renderHTML


def leggiCreditore():
    '''
    Ritorna le informazioni sul creditore

    @return: creditore
    '''
    # inizializziamo i dati del creditore
    creditore = Creditore()
    azienda = Azienda().getRecord(id=Environment.azienda)
    if azienda:
        creditore.codice_fiscale = azienda.codice_fiscale
        if not creditore.codice_fiscale:
            messageError('Inserire il codice fiscale nei Dati azienda.')
            return

        # provare con le banche azienda prima

        if azienda.iban:
            try:
                cc, cs, cin, creditore.abi, creditore.cab, creditore.numero_conto = dividi_iban(azienda.iban)
            except:
                pass
        elif azienda.abi and azienda.cab:
            creditore.abi = azienda.abi
            creditore.cab = azienda.cab
            if azienda.numero_conto:
                creditore.numero_conto = azienda.numero_conto
            else:
                messageError('Inserire il numero di conto nei Dati azienda.')
                return
        else:
            messageError('Inserire il codice IBAN nei Dati azienda.')
            return

        if azienda.codice_rea:
            creditore.codice_sia = str(azienda.codice_rea or ' ')
        else:
            messageError('Inserire il codice SIA in Dati azienda.')
            return

    creditore.descrizione[0] = azienda.ragione_sociale
    creditore.descrizione[1] = azienda.sede_operativa_indirizzo
    creditore.descrizione[2] = azienda.sede_operativa_localita
    creditore.descrizione[3] = azienda.codice_fiscale

    creditore.denominazione_breve = azienda.ragione_sociale

    return creditore


def pagamentoLookup(pagamento):
    return 'riba' in pagamento.lower().replace('.', '')

class PGRiBa(RiBa):

    progressbar = None

    def __init__(self, ana, creditore):
        RiBa.__init__(self, creditore)
        self.ana = ana

    def bind(self, widget):
        self.progressbar = widget

    def analizza(self, data_inizio=None, data_fine=None, pageData=None):
        if not data_inizio:
            messageError(msg='Inserire una data d\'inizio periodo.')
            return 0
        if not data_fine:
            data_inizio_, data_fine = dataInizioFineMese(data_inizio)

        documenti = TestataDocumento().select(complexFilter=(and_(or_(TestataDocumento.operazione=='Fattura differita vendita', TestataDocumento.operazione=='Fattura accompagnatoria'), TestataDocumento.data_documento.between(data_inizio, data_fine))), batchSize=None)

        if not documenti:
            messageInfo(msg="Nessun risultato.")
            return 0

        righe = []

        buff = self.recordIB()

        i = 0
        totale_importi = Decimal(0)

        for documento in documenti:

            if self.progressbar:
                pbar(self.progressbar, parziale=i, totale=len(documenti))

            ope = leggiOperazione(documento.operazione)
            if ope:
                if ope['tipoPersonaGiuridica'] != 'cliente':
                    continue

            banca = None
            if documento.id_banca:
                banca = leggiBanca(documento.id_banca)
            else:
                continue

            cli = leggiCliente(documento.id_cliente)
            cli_ente = Cliente().getRecord(id=documento.id_cliente)
            cod_fisc_piva = ''
            if cli_ente:
                cod_fisc_piva = cli_ente.codice_fiscale or cli_ente.partita_iva
            else:
                cod_fisc_piva = documento.codice_fiscale_cliente
            debitore = Debitore(cod_fisc_piva, banca['abi'], banca['cab'])
            debitore.descrizione[0] = ''
            if cli['ragioneSociale']:
                debitore.descrizione[0] = cli['ragioneSociale']
            else:
                debitore.descrizione[0] = cli['cognome'] + ' ' + cli['nome']
            debitore.indirizzo = documento.indirizzo_cliente
            debitore.CAP = documento.cap_cliente
            debitore.provincia = documento.provincia_cliente
            debitore.comune = documento.localita_cliente

            for scadenza in documento.scadenze:
                if pagamentoLookup(scadenza.pagamento):

                    row = "%s N. %s a %s del %s \nImporto: %s data scadenza: %s" % (documento.operazione,
                                                     documento.numero,
                                                     documento.intestatario,
                                                     dateToString(documento.data_documento),
                                                     # scadenza.pagamento,
                                                     mN(scadenza.importo, 2),
                                                     dateToString(scadenza.data)
                                                     )

                    progressivo = i + 1
                    totale_importi += scadenza.importo
                    buff += self.record14(progressivo, scadenza.data, scadenza.importo, debitore)
                    buff += self.record20(progressivo)
                    buff += self.record30(progressivo, debitore)
                    buff += self.record40(progressivo, debitore)
                    buff += self.record50(progressivo, debitore, row.replace('\n', ''))
                    buff += self.record51(progressivo, progressivo)
                    buff += self.record70(progressivo)

                    riga = {
                        'destinatario': debitore.descrizione[0],
                        'indirizzo': debitore.indirizzo,
                        'CAP': debitore.CAP,
                        'comune': debitore.comune,
                        'provincia': debitore.provincia,
                        'cod_fisc_piva': cod_fisc_piva,
                        'banca_abi': banca['abi'],
                        'banca_cab': banca['cab'],
                        'importo': scadenza.importo,
                        'data_scadenza': scadenza.data,
                        'rif_debito': row
                    }
                    righe.append(riga)

                    i = i + 1

        buff += self.recordEF(i, totale_importi)

        pageData['righe'] = righe
        pageData['totale_importi'] = totale_importi
        pageData['disposizioni'] = i

        if self.progressbar:
            pbar(self.progressbar, stop=True)

        self._buffer = buff

class RiBaExportWindow(GladeWidget):
    '''
    Finestra per l'estrazione dei tracciati Ri.Ba
    '''
    __parent = None
    __pgriba = None
    __creditore = Creditore()
    generatore = None


    def __init__(self, parent):
        '''
        Constructor
        '''
        GladeWidget.__init__(self, root='riba_window', path='riba_window.glade')
        self.__parent = parent
        self.placeWindow(self.getTopLevel())
        self.__setup_webview()
        self.draw()

        try:
            self.__creditore = leggiCreditore()
        except RuntimeError as e:
            messageError(msg=str(e))
        self.show_all()

    def __setup_webview(self):
        from webkit import WebView
        self.view = WebView()
        self.webview_scrolledwindow.add(self.view)

    def show_all(self):
        self.data_inizio_entry.show_all()
        self.data_fine_entry.show_all()

    def on_salva_file_button_clicked(self, button):
        self.salvaFile()

    def on_genera_report_button_clicked(self, button):
        self.generatore = PGRiBa(self, self.__creditore)
        self.generatore.bind(self.progressbar1)
        data_inizio = stringToDate(self.data_inizio_entry.get_text())
        data_fine = stringToDate(self.data_fine_entry.get_text())

        pageData = {
            'file': 'riba_export.html',
            'creditore': self.__creditore,
            'data_inizio': data_inizio,
            'data_fine': data_fine,
        }
        res = 0
        try:
            res = self.generatore.analizza(data_inizio, data_fine, pageData=pageData)
        except RuntimeError as e:
            messageError(msg=str(e))
        if res != 0:
            self.salva_file_button.set_sensitive(True)
            renderHTML(self.view, renderTemplate(pageData))

    def on_stampa_report_button_clicked(self, widget):
        #TODO: implementare la stampa del report.
        pass

    def salvaFile(self):
        data_inizio = stringToDate(self.data_inizio_entry.get_text())
        nome_file = 'ESTRATTO_RIBA_' + data_inizio.strftime('%m_%y') + ".txt"
        fileDialog = gtk.FileChooserDialog(title='Salvare il file',
                                           parent=self.getTopLevel(),
                                           action= GTK_FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    GTK_RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    GTK_RESPONSE_OK),
                                           backend=None)
        fileDialog.set_current_name(nome_file)
        fileDialog.set_current_folder(Environment.documentsDir)

        response = fileDialog.run()

        if ( (response == GTK_RESPONSE_CANCEL) or ( response == GTK_RESPONSE_DELETE_EVENT)) :
            fileDialog.destroy()
        elif response == GTK_RESPONSE_OK:
            filename = fileDialog.get_filename()
            if not filename:
                messageInfo(msg="Nessun nome scelto per il file")
            else:
                fileDialog.destroy()
                self.generatore.write(filename)

    def draw(self):
        self.data_inizio_entry.show_all()
        self.data_fine_entry.show_all()
