# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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


import AnagraficaComplessa
from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
#from promogest.dao.Dao import Dao
from AnagraficaDocumentiFilter import AnagraficaDocumentiFilter
from AnagraficaDocumentiEdit import AnagraficaDocumentiEdit
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
#from promogest.dao.MisuraPezzo import MisuraPezzo
#import promogest.dao.TestataDocumento
from promogest.dao.TestataDocumento import TestataDocumento
from utils import *


class AnagraficaDocumenti(Anagrafica):
    """ Anagrafica documenti """

    def __init__(self, idMagazzino=None, aziendaStr=None):
        self._magazzinoFissato = (idMagazzino != None)
        self._idMagazzino=idMagazzino
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Registrazione documenti',
                            recordMenuLabel='_Documenti',
                            filterElement=AnagraficaDocumentiFilter(self),
                            htmlHandler=AnagraficaDocumentiHtml(self),
                            reportHandler=AnagraficaDocumentiReport(self),
                            editElement=AnagraficaDocumentiEdit(self),
                            aziendaStr=aziendaStr)

        self.duplica_button.set_sensitive(True)
        self.record_duplicate_menu.set_property('visible', True)
        self.records_file_export.set_sensitive(True)
        self.record_fattura_button.set_sensitive(False)

#    def set_data_list(self, data):
#        rowlist=[]
#        for d in data:
#            numero = str(d.numero)
#            data = dateToString(d.data_documento)
#            totali = d.totali
#            totaleImponibile = mN(d._totaleImponibileScontato) or 0
#            totaleImposta = mN(d._totaleImpostaScontata) or 0
#            totale = mN(d._totaleScontato) or 0
#            datalist=[data, numero, d.operazione, d.intestatario,d.protocollo,d.ragione_sociale_agente, totaleImponibile, totaleImposta, totale, d.note_interne]
#            rowlist.append(datalist)
#        return rowlist

#    def set_export_data(self):
#        """
##         Raccoglie informazioni specifiche per l'anagrafica restituite all'interno di un dizionario
#        """
#        data_details = {}
#        data = datetime.datetime.now()
#        curr_date = string.zfill(str(data.day), 2) + '-' + string.zfill(str(data.month),2) + '-' + string.zfill(str(data.year),4)
#        data_details['curr_date'] = curr_date
#        data_details['currentName'] = 'Lista_Documenti_aggiornata_al_'+curr_date+'.xml'

#        FieldsList = ['Data','Numero','Tipo Documento','Cliente/Fornitore','Riferimento Doc. Fornitore','Agente', 'Imponibile','Imposta','Totale','Note Interne']
#        colData= [0,0,0,0,0,1,2,2,2,0,]
#        colWidth_Align = [('100','c'),('70','c'),('150','c'),('250','l'),('100','r'),('150','l'),('100','r'),('100','r'),('100','r'),('250','l')]
#        data_details['XmlMarkup'] = (FieldsList, colData, colWidth_Align)

#        return data_details

    def duplicate(self, dao):
        """
        Duplica le informazioni relative ad un documento scelto su uno nuovo
        """

        if dao is None:
            return

        from DuplicazioneDocumento import DuplicazioneDocumento
        anag = DuplicazioneDocumento(dao, self)
        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(), None, self.filter.refresh)

    def on_record_fattura_button_clicked(self, button=None):
        from FatturazioneDifferita import FatturazioneDifferita
        anag = FatturazioneDifferita(self.anagrafica_filter_treeview.get_selection())
        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(), button=None, callName=self.filter.refresh)

    def on_anagrafica_filter_treeview_selection_changed(self, selection):
        dao = AnagraficaComplessa.Anagrafica.on_anagrafica_filter_treeview_selection_changed(self,selection)
        if dao.__class__ != TestataDocumento:
            if dao.__class__ == list:
                if len(dao) > 1:
                    self.record_fattura_button.set_sensitive(True)
                else:
                    self.record_fattura_button.set_sensitive(False)
        else:
            self.record_fattura_button.set_sensitive(False)
            return

    def on_anagrafica_filter_treeview_cursor_changed(self,treeview):
        pass

class AnagraficaDocumentiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'documento',
                                'Documento')


class AnagraficaDocumentiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei documenti',
                                  defaultFileName='documenti',
                                  htmlTemplate='documenti',
                                  sxwTemplate='documenti')
