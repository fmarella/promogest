# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Dr astico <zoccolodignu@gmail.com>

import os
import gtk
import datetime
#from decimal import *
from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit
from AnagraficaMovimentiEdit import AnagraficaMovimentiEdit
from AnagraficaMovimentiFilter import AnagraficaMovimentiFilter
from AnagraficaDocumentiEditUtils import *
from promogest import Environment
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.dao.Articolo import Articolo
from promogest.dao.Fornitore import Fornitore
from utils import *
from utilsCombobox import *

if "PromoWear" in Environment.modulesList:
    from promogest.modules.PromoWear.ui import AnagraficaDocumentiEditPromoWearExt

class AnagraficaMovimenti(Anagrafica):

    def __init__(self, idMagazzino=None, aziendaStr=None):
        """
        FIXME
        """
        self._magazzinoFissato = (idMagazzino <> None)
        self._idMagazzino=idMagazzino
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Registrazione movimenti',
                            recordMenuLabel='_Movimenti',
                            filterElement=AnagraficaMovimentiFilter(self),
                            htmlHandler=AnagraficaMovimentiHtml(self),
                            reportHandler=AnagraficaMovimentiReport(self),
                            editElement=AnagraficaMovimentiEdit(self),
                            aziendaStr=aziendaStr)
        self.record_duplicate_menu.set_property('visible', True)
        self.records_file_export.set_sensitive(True)

    def LoadFieldsListData(self):
        """
        Returns a tuple wich contains  a list of headers of the xls spreadsheet table fields,
        a flag that indicates what kind of source of data we are messing with and
        width and alignment values to complete cells markup.
        """
        return (FieldsList, colData, colWidth_Align)

    def set_data_list(self, data):
        """
        FIXME
        @param data:
        @type data:
        """
        rowlist=[]
        for d in data:
            soggetto = ''
            if d.id_cliente is not None:
                soggetto = d.ragione_sociale_cliente or ''
                if soggetto == '':
                    soggetto = (d.cognome_cliente or '') + ' ' + (d.nome_cliente or '')
            elif d.id_fornitore is not None:
                soggetto = d.ragione_sociale_fornitore or ''
                if soggetto == '':
                    soggetto = (d.cognome_fornitore or '') + ' ' + (d.nome_fornitore or '')
            data = dateToString(d.data_movimento)
            numero = str(d.numero or 0)
            operazione = d.operazione or ''
            note_interne = d.note_interne or ''
            lista_articoli = d.righe

            if lista_articoli:
                for riga in lista_articoli:
                    codice_articolo = riga.codice_articolo or ''
                    descrizione = riga.descrizione or ''
                    id_testata_movimento = str(riga.id_testata_movimento) or ''
                    magazzino = riga.magazzino or ''
                    moltiplicatore = str(('%.2f') % float(riga.moltiplicatore)) or ''
                    percentuale_iva = str(('%.2f') % float(riga.percentuale_iva)) or ''
                    quantita = str(('%.2f') % float(riga.quantita)) or ''
                    if riga.sconti:
                        sconti = ''
                        for s in riga.sconti:
                            if s.tipo_sconto == 'percentuale':
                                sconti = sconti+str(('%.2f') % float(s.valore))+'%, '
                            elif s.tipo_sconto == 'valore':
                                sconti = sconti+str(('%.2f') % float(s.valore))+u'�'+', '
                        sconti = sconti[:-2]
                    else:
                        sconti = ''
                    valore_unitario_lordo = ('%.2f') % float(riga.valore_unitario_lordo or 0)
                    valore_unitario_netto = ('%.2f') % float(riga.valore_unitario_netto or 0)
                    datalist=[data,operazione,soggetto, codice_articolo,
                             descrizione, magazzino, moltiplicatore,
                             percentuale_iva, quantita, sconti,
                             valore_unitario_lordo, valore_unitario_netto]
                             #lista dei campi del dao da caricare. esempio: d.nome_campo
                    rowlist.append(datalist)
            else:
                codice_articolo = ''
                descrizione = ''
                id = ''
                id_articolo = ''
                id_magazzino = ''
                id_testata_movimento = ''
                magazzino = ''
                moltiplicatore = ''
                percentuale_iva = ''
                quantita = ''
                sconti = ''
                valore_unitario_lordo = 0
                valore_unitario_netto = 0
                datalist=[data,operazione,soggetto, codice_articolo, descrizione,
                         magazzino, moltiplicatore, percentuale_iva, quantita,
                         sconti, valore_unitario_lordo, valore_unitario_netto]
                         #lista dei campi del dao da caricare. esempio: d.nome_campo
                rowlist.append(datalist)
        return rowlist

    def set_export_data(self):
        """
        Raccoglie informazioni specifiche per l'anagrafica
        restituite all'interno di un dizionario
        """
        data_details = {}
        data = datetime.datetime.today()
        curr_date = string.zfill(str(data.day), 2) + \
                            '-' + string.zfill(str(data.month),2) + \
                            '-' + string.zfill(str(data.year),4)
        data_details['curr_date'] = curr_date
        data_details['currentName'] = 'Lista_Movimenti_aggiornata_al_'+curr_date+'.xml'

        FieldsList = ['Data Movimento','Causale Movimento','Cliente/Fornitore',
                        'Codice Articolo','Descrizione','Magazzino',
                        'Moltiplicatore','% IVA','Quantità',
                        'Sconti','Valore Unitario Lordo','Valore Unitario Netto']
        colData = [0,0,0,0,0,0,0,0,0,1,2,2]# 0=None, 1=Totali, 2=valore_somma
        colWidth_Align = [('100','c'),('150','l'),('150','l'),('100','c'),
                            ('250','l'),('150','c'),('100','c'),('70','c'),
                            ('70','c'),('70','c'),('140','r'),('140','r')]
                             # (larghezza colonna, allineamento)__c=center,l=left,r=right
        data_details['XmlMarkup'] = (FieldsList, colData, colWidth_Align)

        return data_details

    def duplicate(self, dao):
        """ Duplica le informazioni relative ad un movimento scelto su uno nuovo """
        if dao is None:
            return

        from DuplicazioneMovimento import DuplicazioneMovimento
        anag = DuplicazioneMovimento(dao,self)
        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(), None, self.filter.refresh)

class AnagraficaMovimentiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        """
        FIXME
        """
        AnagraficaHtml.__init__(self, anagrafica, 'movimento',
                                'Informazioni sul movimento merce')



class AnagraficaMovimentiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        """
        FIXME
        """
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei movimenti',
                                  defaultFileName='movimenti',
                                  htmlTemplate='movimenti',
                                  sxwTemplate='movimenti')
