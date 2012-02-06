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
from promogest.ui.utils import messageError, dateToString, leggiOperazione,\
    dataInizioFineMese, pbar, stringToDate, messageInfo, leggiAzienda,\
    leggiBanca, leggiCliente, mN, messageWarning

from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota
from promogest.lib.iban import check_iban, IBANError
from promogest.modules.Pagamenti.dao import TestataDocumentoScadenza
from datetime import datetime
from decimal import Decimal
from promogest.ui.gtk_compat import *
from sqlalchemy.sql import and_, or_


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
        if azienda.iban:
            try:
                cc, cs, cin, creditore.abi, creditore.cab, creditore.numero_conto = check_iban(azienda.iban)
            except IBANError:
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
    creditore.descrizione[2] = azienda.sede_operativa_provincia
    creditore.descrizione[3] = azienda.codice_fiscale
    
    creditore.descrizione_breve = azienda.codice_fiscale 

    return creditore


def pagamentoLookup(pagamento):
    return 'riba' in pagamento.lower().replace('.', '')

class PGRiBa(RiBa):
    
    def __init__(self, ana, creditore):
        RiBa.__init__(self, creditore)
        self.ana = ana
    
    def analizza(self, data_inizio=None):
        if not data_inizio:
            messageError(msg='Inserire una data d\'inizio periodo.')
            return 0
        
        data_inizio, data_fine = dataInizioFineMese(data_inizio)

        documenti = TestataDocumento().select(complexFilter=(and_(TestataDocumento.data_documento.between(data_inizio, data_fine))), batchSize=None)

        if not documenti:
            messageInfo(msg="Nessun risultato.")
            return 0

        numero_disposizioni = 0
        for documento in documenti:

            if documento.operazione not in ['Fattura differita vendita', 'Fattura accompagnatoria']:
                continue
    
            ope = leggiOperazione(documento.operazione)
            if ope:
                if ope['tipoPersonaGiuridica'] != 'cliente':
                    continue

            # banca = None
            # if documento.id_banca:
                # banca = leggiBanca(documento.id_banca)
            # else:
                # continue
                
            for scadenza in documento.scadenze:
                pbar(self.ana.progressbar1, pulse=True, text='')
                if pagamentoLookup(scadenza.pagamento):

                    numero_disposizioni += 1
                    
                    cliente = leggiCliente(documento.id_cliente)
                    banca = leggiBanca(cliente['id_banca'])
                    
                    debitore = Debitore(documento.codice_fiscale_cliente, banca['abi'], banca['cab'])
                    debitore.descrizione[0]= documento.intestatario
                    debitore.descrizione[1] = banca['abi'] + banca['cab']
                    
                    self.ana.liststore1.append((
                                 (True),
                                 ("%s N. %s a %s del %s \nImporto: %s data scadenza: %s" % (documento.operazione,
                                                     documento.numero,
                                                     documento.intestatario,
                                                     dateToString(documento.data_documento),
                                                     # scadenza.pagamento,
                                                     mN(scadenza.importo, 2),
                                                     dateToString(scadenza.data)
                                                     )),
                                 (scadenza),
                                 (debitore)
                                 ))
        pbar(self.ana.progressbar1, stop=True)
        return numero_disposizioni
    
    def genera(self, rows):
        disposizioni = len(rows)
        buff = self.recordIB()
        i = 0
        totale_importi = Decimal(0)
        for row in rows:
            scadenza = row[1]
            debitore = row[2]
            progressivo = i + 1
            totale_importi += scadenza.importo
            buff += self.record14(progressivo, scadenza.data, scadenza.importo, debitore)
            buff += self.record20(progressivo)
            buff += self.record30(progressivo, debitore)
            buff += self.record40(progressivo, debitore)
            buff += self.record50(progressivo, debitore, row[0].replace('\n', ''))
            buff += self.record51(progressivo, progressivo)
            buff += self.record70(progressivo)
            i = i + 1
        buff += self.recordEF(disposizioni, totale_importi)
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
        GladeWidget.__init__(self, 'riba_window', fileName='riba_window.glade')
        self.__parent = parent
        self.getTopLevel()
        self.placeWindow(self.getTopLevel()) 
        self.draw()
        
        try:
            self.__creditore = leggiCreditore()
        except RuntimeError as e:
            messageError(msg=str(e))
        self.show_all()
        
    def show_all(self):
        self.data_entry.show_all()

    def on_aggiorna_button_clicked(self, button):
        self.liststore1.clear()
        self.generatore = PGRiBa(self, self.__creditore)
        data = stringToDate(self.data_entry.get_text())
        num = 0
        try:
            num = self.generatore.analizza(data)
        except RuntimeError as e:
            messageError(msg=str(e))
        if num > 0:
            self.genera_button.set_sensitive(True)

    def search(self):
        
        def match_func(model, path, iter, data):
            pbar(self.progressbar1, pulse=True, text='')
            if model.get_value(iter, 0) == True:
                data.append([model.get_value(iter, 1),
                             model.get_value(iter, 2),
                             model.get_value(iter, 3)])
            return False
        
        pathlist = []
        self.liststore1.foreach(match_func, pathlist)
        return pathlist
    
    def salvaFile(self):
        data = stringToDate(self.data_entry.get_text())
        nome_file = 'estratto_riba_' + data.strftime('%m_%y') + ".txt"
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
        
    def on_genera_button_clicked(self, button):
        selected = self.search()
        pbar(self.progressbar1, stop=True)
        if selected:
            self.generatore.genera(selected)
            pbar(self.progressbar1, stop=True)
            self.salvaFile()

    def on_stato_cellrendertoggle_toggled(self, widget, model):
        sel = self.treeview1.get_selection()
        sel.select_path(model)
        model, _iter = sel.get_selected()
        if not _iter:
            return
        if model.get_value(_iter, 0):
            model.set_value(_iter, 0, 0)
        else:
            model.set_value(_iter, 0, 1)

    def on_chiudi_button_clicked(self, button):
        self.destroy()
        #return None
    
    def draw(self):
        self.data_entry.show_all()
        #self.data_entry.set_text(dateToString(dataInizioFineMese(datetime.now())[0]))
        self.genera_button.set_sensitive(False)
