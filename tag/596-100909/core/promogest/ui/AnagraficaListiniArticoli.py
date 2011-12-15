# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>


import os
import gtk
import gobject
import datetime
import string
from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport,  AnagraficaEdit, AnagraficaLabel

from promogest import Environment
from promogest.dao.Articolo import Articolo
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
from promogest.dao.ListinoComplessoListino import ListinoComplessoListino
from utils import *
from utilsCombobox import fillComboboxListini,findIdFromCombobox,findComboboxRowFromId

if "PromoWear" in Environment.modulesList:
    from promogest.modules.PromoWear.ui.AnagraficaListinoArticoliExpand import *

class AnagraficaListiniArticoli(Anagrafica):
    """ Anagrafica listini vendita articoli """

    def __init__(self, idArticolo=None, idListino=None,aziendaStr=None):
        """
        FIXME
        """
        self._articoloFissato = (idArticolo <> None)
        self._listinoFissato = (idListino <> None)
        self._idArticolo=idArticolo
        self._idListino=idListino
        if "PromoWear" in Environment.modulesList:
            from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica listini di vendita',
                            recordMenuLabel='_Listini',
                            filterElement=AnagraficaListiniArticoliFilter(self),
                            htmlHandler=AnagraficaListiniArticoliHtml(self),
                            reportHandler=AnagraficaListiniArticoliReport(self),
                            labelHandler=AnagraficaListiniArticoliLabel(self),
                            editElement=AnagraficaListiniArticoliEdit(self),
                            aziendaStr=aziendaStr)

        self.Stampa_Frontaline.set_visible_horizontal(True)
        #if "Label" not in Environment.modulesList:
            #self.Stampa_Frontaline.set_sensitive(False)
        self.records_file_export.set_sensitive(True)

    def set_data_list(self, data):
        """
        FIXME
        @param data:
        @type data:
        """
        rowlist=[]
        for d in data:
            #print "DDDDDDDDDDDD", dir(d.arti),
            denominazione = d.denominazione or ''
            codice_articolo = d.codice_articolo or ''
            articolo = d.articolo or ''
            data = dateToString(d.data_listino_articolo)
            prezzo_dettaglio = mN(str(d.prezzo_dettaglio)) or 0
            sconto_dettaglio = []
            for sconto_det in d.sconto_vendita_dettaglio:
                sconto_dettaglio.append(str(mN(str(sconto_det.valore))) or 0)
            sconto_dettagliostr = string.join( sconto_dettaglio, '' )
            #sconto_dettaglio = mN(d.sconto_vendita_dettaglio) or 0
            prezzo_ingrosso = mN(str(d.prezzo_ingrosso)) or 0
            sconto_ingrosso = []
            for sconto_ing in d.sconto_vendita_ingrosso:
                sconto_ingrosso.append(str(mN(str(sconto_ing.valore))) or 0)
            sconto_ingrossostr = string.join( sconto_ingrosso, '' )
            if sconto_dettagliostr == "[]":
                sconto_dettagliostr == ""
            if sconto_ingrossostr == "[]":
                sconto_ingrossostr = ""
            try:
                categoria = d.arti.denominazione_categoria
            except:
                categoria = ""
            try:
                famiglia = d.arti.denominazione_famiglia
            except:
                famiglia =""
            try:
                percentuale_iva = d.percentuale_iva
            except:
                percentuale_iva =""
            #sconto_ingrosso = mN(d.sconto_vendita_ingrosso[0]) or 0
            datalist=[denominazione,codice_articolo,articolo,data,prezzo_dettaglio,
                        sconto_dettagliostr,prezzo_ingrosso,sconto_ingrossostr,
                        categoria, famiglia, percentuale_iva
]
            rowlist.append(datalist)
        return rowlist

    def set_export_data(self):
        """
        Raccoglie informazioni specifiche per l'anagrafica restituite all'interno di un dizionario
        """
        data_details = {}
        data = datetime.datetime.today()
        curr_date = string.zfill(str(data.day), 2) + '-' + string.zfill(str(data.month),2) + '-' + string.zfill(str(data.year),4)
        data_details['curr_date'] = curr_date
        data_details['currentName'] = 'Listino_Articoli_aggiornato_al_'+curr_date+'.xml'

        FieldsList = ['Listino','Codice Articolo','Articolo','Data Variazione','Prezzo Dettaglio', 'Sconto Dettaglio',
                            'Prezzo Ingrosso', 'Sconto Ingrosso', "Categoria", "Famiglia", "Iva"
]
        colData= [0,0,0,1,2,0,2,0]
        colWidth_Align = [('130','l'),('100','c'),('250','l'),('100','c'),('100','r'),('100','r'),
                            ('100','r'),('100','r'),('100','r'),('100','r'),('100','r')
]
        data_details['XmlMarkup'] = (FieldsList, colData, colWidth_Align)
        return data_details


class AnagraficaListiniArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei listini """

    def __init__(self, anagrafica):
        """
        FIXME
        @param anagrafica:
        @type anagrafica:
        """
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_listini_articoli_filter_table',
                                  gladeFile='_anagrafica_listini_articoli_elements.glade')
        self._widgetFirstFocus = self.id_listino_filter_combobox


    def draw(self):
        """
        FIXME
        """
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'id_listino'))
        column.set_resizable(False)
        column.set_expand(True)
        column.set_min_width(250)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'codice_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'id_articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data variazione', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'data_listino_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'prezzo_dettaglio')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso', rendererDx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'prezzo_ingrosso')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)
        if "PromoWear" in Environment.modulesList:
            drawPromoWearExpand1(self)
        else:
            self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)
        self.isComplexPriceList=None
        if self._anagrafica._idListino:
            self.isComplexPriceList = ListinoComplessoListino().select(idListinoComplesso = self._anagrafica._idListino, batchSize=None)
        if self.isComplexPriceList:
            self.sotto_listini_label.set_sensitive(True)
            self.id_sotto_listino_filter_combobox.set_sensitive(True)
            fillComboboxListiniComplessi(self.id_sotto_listino_filter_combobox,
                                        idListinoComplesso = self._anagrafica._idListino,filter=True)
        fillComboboxListini(self.id_listino_filter_combobox, True)

        if self._anagrafica._articoloFissato:
            self.id_articolo_filter_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_filter_customcombobox.set_sensitive(False)
            if not (self._anagrafica._listinoFissato):
                column = self._anagrafica.anagrafica_filter_treeview.get_column(1)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(2)
                column.set_property('visible', False)
                if "PromoWear" in Environment.modulesList:
                    drawPromoWearExpand2(self)
        if self._anagrafica._listinoFissato:
            findComboboxRowFromId(self.id_listino_filter_combobox, self._anagrafica._idListino)
            Environment.listinoFissato = self._anagrafica._idListino
            self.id_listino_filter_combobox.set_sensitive(False)
            if not (self._anagrafica._articoloFissato):
                column = self._anagrafica.anagrafica_filter_treeview.get_column(0)
                column.set_property('visible', False)
        self.clear()

    def clear(self):
        """
        FIXME
        """
        # Annullamento filtro
        if not(self._anagrafica._articoloFissato):
            self.id_articolo_filter_customcombobox.set_active(0)
        if not(self._anagrafica._listinoFissato):
            self.id_listino_filter_combobox.set_active(0)
            self.id_sotto_listino_filter_combobox.set_active(0)
        self.refresh()


    def refresh(self):
        """
        Allora, si è resa necessaria una soluzione tampone per la ricerca
        avanzata, non avendo più la tabella d'appoggio come prima
        viaggia una lista di id che deve essere gestita poi in una query
        il risultato è minore pulizia ma maggiore velocità
        """
        #if not self.isComplexPriceList:
        listcount = 0
        multilistCount = 0
        multilist = []
        idArticolo = self.id_articolo_filter_customcombobox.getId()
        idListino = findIdFromCombobox(self.id_listino_filter_combobox)
        idSottoListino = findIdFromCombobox(self.id_sotto_listino_filter_combobox)

        if not idSottoListino and self.isComplexPriceList:
            for sottolist in self.isComplexPriceList:
                multilist.append(sottolist.id_listino)
            idListino=multilist
        elif idSottoListino and self.isComplexPriceList :
            idListino=idSottoListino

        def filterCountClosure():
            """
            FIXME
            """
            return ListinoArticolo().count(idListino=idListino,
                                            idArticolo=idArticolo,
                                            listinoAttuale=True)

        self._filterCountClosure = filterCountClosure
        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            """
            """
            return ListinoArticolo().select(orderBy=self.orderBy,
                                            idListino=idListino,
                                            idArticolo=idArticolo,
                                            listinoAttuale=True,
                                            offset=offset,
                                            batchSize=batchSize)

        self._filterClosure = filterClosure
        self.liss = self.runFilter()
        self.xptDaoList = self.runFilter(offset=None, batchSize=None)
        modelRow = []
        modelRowPromoWear = []
        self._treeViewModel.clear()
        for l in self.liss:
            modelRow = [l,
                        (l.denominazione or ''),
                        (l.codice_articolo or ''),
                        (l.articolo or ''),
                        dateToString(l.data_listino_articolo),
                        str(mN(l.prezzo_dettaglio) or 0),
                        str(mN(l.prezzo_ingrosso) or 0)]

            if "PromoWear" in Environment.modulesList:
                modelRowPromoWear=[(l.denominazione_gruppo_taglia or ''),
                                        (l.denominazione_taglia or ''),
                                        (l.denominazione_colore or ''),
                                        (l.anno or ''),
                                        (l.stagione or ''),
                                        (l.genere or '')]

            if modelRowPromoWear:
                self._treeViewModel.append(modelRow +modelRowPromoWear)
            else:
                self._treeViewModel.append(modelRow)
        #Environment.listinoFissato =  None
class AnagraficaListiniArticoliHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        """
        Gestisce l'anteprima html dei listini articolo
        """
        AnagraficaHtml.__init__(self, anagrafica, 'listino_articolo',
                                'Informazioni articolo/listino')


class AnagraficaListiniArticoliReport(AnagraficaReport):

    def __init__(self, anagrafica):
        """
        Gestisce i report dei listini articolo
        """
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei listini',
                                  defaultFileName='listini_articolo',
                                  htmlTemplate='listini_articolo',
                                  sxwTemplate='listini_articolo')


class AnagraficaListiniArticoliLabel(AnagraficaLabel):

    def __init__(self, anagrafica):
        """
        Gestisce la creazione delle frontaline o label
        """
        AnagraficaLabel.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei listini',
                                  htmlTemplate='label',
                                  sxwTemplate='label',
                                  defaultFileName='label')


class AnagraficaListiniArticoliEdit(AnagraficaEdit):
    """
    Modifica un record dell'anagrafica degli articoli dei listini
    """
    def __init__(self, anagrafica):
        """
        Gestione la modifica e l'editing dei listino articolo
        """
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_listini_articoli_detail_table',
                                'Dati articolo nel listino',
                                gladeFile='_anagrafica_listini_articoli_elements.glade')
        self._widgetFirstFocus = self.id_articolo_customcombobox
        self._percentualeIva = 0
        if "PromoWear" not in Environment.modulesList:
            self.taglia_colore_table.hide()
            self.taglia_colore_table.set_no_show_all(True)
        self.sconti_dettaglio_widget.button.connect('toggled',
                                        self.on_sconti_dettaglio_widget_button_toggled)
        self.sconti_ingrosso_widget.button.connect('toggled',
                                        self.on_sconti_ingrosso_widget_button_toggled)
        #ListinoArticolo().cleann()


    def on_sconti_dettaglio_widget_button_toggled(self, button):
        """
        Gestione sconti dettaglio  con custom Widget
        FIXME: trovare alternativa a custom widget
        """
        if button.get_property('active') is True:
            return
        _scontoDettaglio= self.sconti_dettaglio_widget.getSconti()

    def on_sconti_ingrosso_widget_button_toggled(self, button):
        """
        Gestione sconti dettaglio  con custom Widget
        FIXME: trovare alternativa a custom widget
        """
        if button.get_property('active') is True:
            return

        _scontoIngrosso= self.sconti_ingrosso_widget.getSconti()

    def calcolaPercentualiDettaglio(self, widget=None, event=None):
        """
        calcolaPercentualiDettaglio
        """
        self.percentuale_ricarico_dettaglio_entry.set_text('%-6.3f' % calcolaRicarico(float(self.ultimo_costo_entry.get_text()),
                                                                                      float(self.prezzo_dettaglio_entry.get_text()),
                                                                                      float(self._percentualeIva)))
        self.percentuale_margine_dettaglio_entry.set_text('%-6.3f' % calcolaMargine(float(self.ultimo_costo_entry.get_text()),
                                                                                    float(self.prezzo_dettaglio_entry.get_text()),
                                                                                    float(self._percentualeIva)))


    def confermaCalcolaPercentualiDettaglio(self, widget=None, event=None):
        """
        confermaCalcolaPercentualiDettaglio
        """
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaPercentualiDettaglio()


    def calcolaPercentualiIngrosso(self, widget=None, event=None):
        """
        calcolaPercentualiIngrosso
        """
        self.percentuale_ricarico_ingrosso_entry.set_text('%-6.3f' % calcolaRicarico(float(self.ultimo_costo_entry.get_text()),
                                                                                     float(self.prezzo_ingrosso_entry.get_text())))
        self.percentuale_margine_ingrosso_entry.set_text('%-6.3f' % calcolaMargine(float(self.ultimo_costo_entry.get_text()),
                                                                                   float(self.prezzo_ingrosso_entry.get_text())))


    def confermaCalcolaPercentualiIngrosso(self, widget=None, event=None):
        """
        FIXME
        """
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaPercentualiIngrosso()


    def aggiornaCostoIvato(self, widget=None, event=None):
        """

        """
        self.ultimo_costo_ivato_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(float(self.ultimo_costo_entry.get_text()),
                                                                                                 float(self._percentualeIva)))
        return False


    def aggiornaDaCosto(self, widget=None, event=None):
        """
        FIXME
        """
        self.aggiornaCostoIvato()


    def confermaAggiornaDaCosto(self, widget=None, event=None):
        """
        FIXME
        """
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.aggiornaDaCosto()

    def calcolaDettaglioDaRicarico(self, widget=None, event=None):
        """
        FIXME
        """
        prezzoDettaglio=Environment.conf.number_format % calcolaListinoDaRicarico(float(self.ultimo_costo_entry.get_text()),
                                                                                            float(self.percentuale_ricarico_dettaglio_entry.get_text()),
                                                                                            float(self._percentualeIva))
        self.prezzo_dettaglio_entry.set_text(prezzoDettaglio)
        self.prezzo_dettaglio_noiva_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(float(prezzoDettaglio),
                                                                                    float(- self._percentualeIva)))
        self.percentuale_margine_dettaglio_entry.set_text('%-6.3f' % calcolaMargine(float(self.ultimo_costo_entry.get_text()),
                                                                                    float(prezzoDettaglio),
                                                                                    float(self._percentualeIva)))


    def confermaCalcolaDettaglioDaRicarico(self, widget=None, event=None):
        """
        FIXME
        """
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaDettaglioDaRicarico()

    def calcolaDettaglioDaMargine(self, widget=None, event=None):
        """
        FIXME
        """
        self.prezzo_dettaglio_entry.set_text(Environment.conf.number_format % calcolaListinoDaMargine(float(self.ultimo_costo_entry.get_text()),
                                                                                                      float(self.percentuale_margine_dettaglio_entry.get_text()),
                                                                                                      float(self._percentualeIva)))
        self.prezzo_dettaglio_noiva_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(float(self.prezzo_dettaglio_entry.get_text()),
                                                                                                     float(- self._percentualeIva)))
        self.percentuale_ricarico_dettaglio_entry.set_text('%-6.3f' % calcolaRicarico(float(self.ultimo_costo_entry.get_text()),
                                                                                      float(self.prezzo_dettaglio_entry.get_text()),
                                                                                      float(self._percentualeIva)))

    def confermaCalcolaDettaglioDaMargine(self, widget=None, event=None):
        """
        FIXME
        """
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaDettaglioDaMargine()

    def aggiornaDaDettaglio(self, widget=None, event=None):
        """
        FIXME
        """
        self.prezzo_dettaglio_noiva_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(float(self.prezzo_dettaglio_entry.get_text()),
                                                                                                     float(- self._percentualeIva)))
        przD = float(self.prezzo_dettaglio_noiva_label.get_text())
        przI = float(self.prezzo_ingrosso_entry.get_text())
        if przI == float(0):
            self.prezzo_ingrosso_entry.set_text(Environment.conf.number_format % przD)
            self.prezzo_ingrosso_ivato_label.set_text(self.prezzo_dettaglio_entry.get_text())
        else:
            if przD != przI:
                msg = 'Attenzione! Aggiornare anche il listino ingrosso ?'
                dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                           gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
                response = dialog.run()
                dialog.destroy()
                if response == gtk.RESPONSE_YES:
                    self.prezzo_ingrosso_entry.set_text(Environment.conf.number_format % przD)
                    self.prezzo_ingrosso_ivato_label.set_text(self.prezzo_dettaglio_entry.get_text())
        return False

    def calcolaIngrossoDaRicarico(self, widget=None, event=None):
        """
        FIXME
        """
        self.prezzo_ingrosso_entry.set_text(Environment.conf.number_format % calcolaListinoDaRicarico(float(self.ultimo_costo_entry.get_text()),
                                                                                                      float(self.percentuale_ricarico_ingrosso_entry.get_text())))
        self.prezzo_ingrosso_ivato_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(float(self.prezzo_ingrosso_entry.get_text()),
                                                                                                    float(self._percentualeIva)))
        self.percentuale_margine_ingrosso_entry.set_text('%-6.3f' % calcolaMargine(float(self.ultimo_costo_entry.get_text()),
                                                                                   float(self.prezzo_ingrosso_entry.get_text())))

    def confermaCalcolaIngrossoDaRicarico(self, widget=None, event=None):
        """
        FIXME
        """
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaIngrossoDaRicarico()

    def calcolaIngrossoDaMargine(self, widget=None, event=None):
        """
        FIXME
        """
        self.prezzo_ingrosso_entry.set_text(Environment.conf.number_format % calcolaListinoDaMargine(float(self.ultimo_costo_entry.get_text()),
                                                                                                     float(self.percentuale_margine_ingrosso_entry.get_text())))
        self.prezzo_ingrosso_ivato_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(float(self.prezzo_ingrosso_entry.get_text()),
                                                                                                    float(self._percentualeIva)))
        self.percentuale_ricarico_ingrosso_entry.set_text('%-6.3f' % calcolaRicarico(float(self.ultimo_costo_entry.get_text()),
                                                                                     float(self.prezzo_ingrosso_entry.get_text())))

    def confermaCalcolaIngrossoDaMargine(self, widget=None, event=None):
        """
        FIXME
        """
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaIngrossoDaMargine()

    def aggiornaDaIngrosso(self, widget=None, event=None):
        """
        FIXME
        """
        self.prezzo_ingrosso_ivato_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(float(self.prezzo_ingrosso_entry.get_text()),
                                                                                                    float(self._percentualeIva)))
        przI = float(self.prezzo_ingrosso_ivato_label.get_text())
        przD = float(self.prezzo_dettaglio_entry.get_text())
        if przD == float(0):
            self.prezzo_dettaglio_entry.set_text(Environment.conf.number_format % przI)
            self.prezzo_dettaglio_noiva_label.set_text(self.prezzo_ingrosso_entry.get_text())
        else:
            if przI != przD:
                msg = 'Attenzione! Aggiornare anche il listino dettaglio ?'
                dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                           gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
                response = dialog.run()
                dialog.destroy()
                if response == gtk.RESPONSE_YES:
                    self.prezzo_dettaglio_entry.set_text(Environment.conf.number_format % przI)
                    self.prezzo_dettaglio_noiva_label.set_text(self.prezzo_ingrosso_entry.get_text())
        return False

    def draw(self):
        """
        FIXME
        """
        self.id_articolo_customcombobox.setSingleValue()
        self.id_articolo_customcombobox.setOnChangedCall(self.on_id_articolo_customcombobox_changed)

        fillComboboxListini(self.id_listino_customcombobox.combobox)
        self.id_listino_customcombobox.connect('clicked',
                                               on_id_listino_customcombobox_clicked,
                                               None, None)

        if self._anagrafica._articoloFissato:
            self.id_articolo_customcombobox.setId(self._anagrafica._idArticolo)
            res = self.id_articolo_customcombobox.getData()
            self.id_articolo_customcombobox.set_sensitive(False)
            self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
            self._percentualeIva = res["percentualeAliquotaIva"]
            self.percentuale_aliquota_iva_label.set_text(('%5.' + Environment.conf.decimals + 'f') % self._percentualeIva + ' %')
        if self._anagrafica._listinoFissato:
            findComboboxRowFromId(self.id_listino_customcombobox.combobox, self._anagrafica._idListino)
            self.id_listino_customcombobox.set_sensitive(False)

        self.sconti_dettaglio_widget.setValues()
        self.sconti_ingrosso_widget.setValues()

        self.ultimo_costo_entry.connect('focus_out_event',
                                        self.aggiornaDaCosto)
        self.ultimo_costo_entry.connect('key_press_event',
                                        self.confermaAggiornaDaCosto)
        self.prezzo_dettaglio_entry.connect('focus_out_event',
                                            self.aggiornaDaDettaglio)
        self.prezzo_dettaglio_entry.connect('key_press_event',
                                            self.confermaCalcolaPercentualiDettaglio)
        self.percentuale_ricarico_dettaglio_entry.connect('key_press_event',
                                                          self.confermaCalcolaDettaglioDaRicarico)
        self.calcola_dettaglio_da_ricarico_button.connect('clicked',
                                                          self.calcolaDettaglioDaRicarico)
        self.percentuale_margine_dettaglio_entry.connect('key_press_event',
                                                         self.confermaCalcolaDettaglioDaMargine)
        self.calcola_dettaglio_da_margine_button.connect('clicked',
                                                         self.calcolaDettaglioDaMargine)
        self.calcola_percentuali_dettaglio_button.connect('clicked',
                                                          self.calcolaPercentualiDettaglio)
        self.prezzo_ingrosso_entry.connect('focus_out_event',
                                           self.aggiornaDaIngrosso)
        self.prezzo_ingrosso_entry.connect('key_press_event',
                                           self.confermaCalcolaPercentualiIngrosso)
        self.percentuale_ricarico_ingrosso_entry.connect('key_press_event',
                                                         self.confermaCalcolaIngrossoDaRicarico)
        self.calcola_ingrosso_da_ricarico_button.connect('clicked',
                                                         self.calcolaIngrossoDaRicarico)
        self.percentuale_margine_ingrosso_entry.connect('key_press_event',
                                                        self.confermaCalcolaIngrossoDaMargine)
        self.calcola_ingrosso_da_margine_button.connect('clicked',
                                                        self.calcolaIngrossoDaMargine)
        self.calcola_percentuali_ingrosso_button.connect('clicked',
                                                         self.calcolaPercentualiIngrosso)


    def on_id_articolo_customcombobox_changed(self):
        """
        FIXME
        """
        res = self.id_articolo_customcombobox.getData()
        self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
        self._percentualeIva = res["percentualeAliquotaIva"]
        self.percentuale_aliquota_iva_label.set_text(('%5.' + Environment.conf.decimals + 'f') % self._percentualeIva + ' %')

        fornitura = leggiFornitura(self.id_articolo_customcombobox.getId())
        self.ultimo_costo_entry.set_text(Environment.conf.number_format % float(fornitura["prezzoNetto"]))

        self.aggiornaCostoIvato()
        self.calcolaDettaglioDaRicarico()
        self.calcolaIngrossoDaRicarico()


    def setDao(self, dao):
        """
        FIXME
        @param dao:
        @type dao:
        """
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = ListinoArticolo()
            if Environment.listinoFissato and self._anagrafica._idListino:
                Environment.listinoFissato = None
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = ListinoArticolo().select(idListino=dao.id_listino,
                                    idArticolo=dao.id_articolo,
                                    orderBy="id_articolo")[0]
        self._refresh()


    def _refresh(self):
        """
        FIXME
        """
        self.id_articolo_customcombobox.refresh(clear=True, filter=False)
        self.id_articolo_customcombobox.set_sensitive(True)
        if self.dao.id_articolo is None:
            if self._anagrafica._articoloFissato:
                self.dao.id_articolo = self._anagrafica._idArticolo
                self.id_articolo_customcombobox.set_sensitive(False)
        else:
            self.id_articolo_customcombobox.set_sensitive(False)
        self.sconti_dettaglio_widget.setValues(sco=self.dao.sconto_vendita_dettaglio)
        self.sconti_ingrosso_widget.setValues(sco=self.dao.sconto_vendita_ingrosso)
        self.id_articolo_customcombobox.setId(self.dao.id_articolo)
        res = self.id_articolo_customcombobox.getData()
        self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
        self._percentualeIva = res["percentualeAliquotaIva"]
        self.percentuale_aliquota_iva_label.set_text(Environment.conf.number_format % self._percentualeIva + ' %')
        self.id_listino_customcombobox.combobox.set_active(-1)
        self.id_listino_customcombobox.set_sensitive(True)
        if self.dao.id_listino is None:
            if self._anagrafica._listinoFissato:
                self.dao.id_listino = self._anagrafica._idListino
                self.id_listino_customcombobox.set_sensitive(False)
        else:
            self.id_listino_customcombobox.set_sensitive(False)
        findComboboxRowFromId(self.id_listino_customcombobox.combobox, self.dao.id_listino)

        if self.dao.ultimo_costo is None:
            fornitura = leggiFornitura(self.id_articolo_customcombobox.getId())
            self.ultimo_costo_entry.set_text(Environment.conf.number_format % float(fornitura["prezzoNetto"]))
        else:
            self.ultimo_costo_entry.set_text(Environment.conf.number_format % float(self.dao.ultimo_costo or 0))
        self.data_listino_articolo_label.set_text(dateToString(self.dao.data_listino_articolo))
        self.prezzo_dettaglio_entry.set_text(Environment.conf.number_format % float(self.dao.prezzo_dettaglio or 0))
        self.prezzo_ingrosso_entry.set_text(Environment.conf.number_format % float(self.dao.prezzo_ingrosso or 0))
        self.percentuale_ricarico_dettaglio_entry.set_text('%-6.3f' % calcolaRicarico(self.dao.ultimo_costo,
                                                                                      self.dao.prezzo_dettaglio,
                                                                                      self._percentualeIva))
        self.percentuale_margine_dettaglio_entry.set_text('%-6.3f' % calcolaMargine(self.dao.ultimo_costo,
                                                                                    self.dao.prezzo_dettaglio,
                                                                                    self._percentualeIva))
        self.percentuale_ricarico_ingrosso_entry.set_text('%-6.3f' % calcolaRicarico(self.dao.ultimo_costo,
                                                                                     self.dao.prezzo_ingrosso))
        self.percentuale_margine_ingrosso_entry.set_text('%-6.3f' % calcolaMargine(self.dao.ultimo_costo,
                                                                                   self.dao.prezzo_ingrosso))

        self.ultimo_costo_ivato_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(self.dao.ultimo_costo,
                                                                                                 self._percentualeIva))
        a = calcolaPrezzoIva(self.dao.prezzo_dettaglio,((-1)*self._percentualeIva))
        self.prezzo_dettaglio_noiva_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(self.dao.prezzo_dettaglio,
                                                                                                    - self._percentualeIva))

        self.prezzo_ingrosso_ivato_label.set_text(Environment.conf.number_format % calcolaPrezzoIva(self.dao.prezzo_ingrosso,
                                                                                                    self._percentualeIva))

        self.sconti_dettaglio_widget.setValues(self.dao.sconto_vendita_dettaglio, self.dao.applicazione_sconti_dettaglio)
        self.sconti_ingrosso_widget.setValues(self.dao.sconto_vendita_ingrosso, self.dao.applicazione_sconti_ingrosso)

        if "PromoWear" in Environment.modulesList:
            self._refreshTagliaColore(self.dao.id_articolo)

    def _refreshTagliaColore(self, idArticolo):
        """
        FIXME
        @param idArticolo:
        @type idArticolo:
        """
        articoloTagliaColore = Articolo().getRecord(id=idArticolo)
        self.taglia_colore_table.hide()
        if articoloTagliaColore is not None:
            gruppoTaglia = articoloTagliaColore.denominazione_gruppo_taglia or ''
            taglia = articoloTagliaColore.denominazione_taglia or ''
            colore = articoloTagliaColore.denominazione_colore or ''
            anno = articoloTagliaColore.anno or ''
            stagione = articoloTagliaColore.stagione or ''
            genere = articoloTagliaColore.genere or ''
            self.taglia_label.set_markup('<span weight="bold">%s (%s)  %s</span>'
                                         % (taglia, gruppoTaglia, genere))
            self.colore_label.set_markup('<span weight="bold">%s</span>'
                                         % (colore))
            self.stagione_label.set_markup('<span weight="bold">%s  %s</span>'
                                           % (stagione, anno))
            self.taglia_colore_table.show()

    def saveDao(self):
        """
        FIXME
        """
        creaentryvarianti = False
        articolo = None
        if findIdFromCombobox(self.id_listino_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel, self.id_listino_customcombobox.combobox)

        if self.id_articolo_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel, self.id_articolo_customcombobox)

        listin = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        self.dao.id_listino = listin
        self.dao.id_articolo = self.id_articolo_customcombobox.getId()

        if "PromoWear" in Environment.modulesList:
            articolo = Articolo().getRecord(id=self.dao.id_articolo)
            if articleType(articolo) == "father":
                msg = 'Attenzione! Si sta aggiungengo un Articolo Padre, creare le voci listino anche delle varianti?'
                dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                           gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
                response = dialog.run()
                dialog.destroy()
                if response == gtk.RESPONSE_YES:
                    Environment.pg2log.info("CREO LE ENTRY DELLE VARIANTI DI LISTINO PERCHE' SI STA INSERENDO UN PADRE")
                    for art in articolo.articoliVarianti:
                        daoVariante = ListinoArticolo().select(idListino=listin,
                                                        idArticolo=art.id)
                        if daoVariante:
                            #daoVariante[0].delete()
                            daoVariante =daoVariante[0]
                        else:
                            daoVariante = ListinoArticolo()
                        if Environment.listinoFissato and self._anagrafica._idListino:
                            Environment.listinoFissato = None
                        daoVariante.id_articolo = art.id

                        daoVariante.id_listino = findIdFromCombobox(self.id_listino_customcombobox.combobox)
                        daoVariante.listino_attuale = True
                        daoVariante.ultimo_costo = float(self.ultimo_costo_entry.get_text())
                        daoVariante.prezzo_dettaglio = float(self.prezzo_dettaglio_entry.get_text())
                        daoVariante.prezzo_ingrosso = float(self.prezzo_ingrosso_entry.get_text())
                        daoVariante.data_listino_articolo = datetime.datetime.today()


                        sconti_dettaglio = []
                        daoVariante.applicazione_sconti = "scalare"
                        for s in self.sconti_dettaglio_widget.getSconti():
                            daoSconto = ScontoVenditaDettaglio()
                            daoSconto.valore = s["valore"]
                            daoSconto.tipo_sconto = s["tipo"]
                            sconti_dettaglio.append(daoSconto)

                        sconti_ingrosso = []
                        daoVariante.applicazione_sconti = "scalare"
                        for s in self.sconti_ingrosso_widget.getSconti():
                            daoSconto = ScontoVenditaIngrosso()
                            daoSconto.valore = s["valore"]
                            daoSconto.tipo_sconto = s["tipo"]
                            sconti_ingrosso.append(daoSconto)
                        daoVariante.persist(sconti={"dettaglio":sconti_dettaglio,"ingrosso":sconti_ingrosso})
                            #self.articolo_padre = articolo
                            #creaentryvarianti = True

        self.dao.listino_attuale = True
        self.dao.ultimo_costo = float(self.ultimo_costo_entry.get_text())
        self.dao.prezzo_dettaglio = float(self.prezzo_dettaglio_entry.get_text())
        self.dao.prezzo_ingrosso = float(self.prezzo_ingrosso_entry.get_text())
        self.dao.data_listino_articolo = datetime.datetime.today()

        sconti_dettaglio = []
        self.dao.applicazione_sconti = "scalare"
        for s in self.sconti_dettaglio_widget.getSconti():
            daoSconto = ScontoVenditaDettaglio()
            daoSconto.valore = s["valore"]
            daoSconto.tipo_sconto = s["tipo"]
            sconti_dettaglio.append(daoSconto)

        sconti_ingrosso = []
        self.dao.applicazione_sconti = "scalare"
        for s in self.sconti_ingrosso_widget.getSconti():
            daoSconto = ScontoVenditaIngrosso()
            daoSconto.valore = s["valore"]
            daoSconto.tipo_sconto = s["tipo"]
            sconti_ingrosso.append(daoSconto)
        #TODO :riportarlo alle property , risulta molto più pulito
        self.dao.persist(sconti={"dettaglio":sconti_dettaglio,"ingrosso":sconti_ingrosso})