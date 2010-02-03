# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Andrea Argiolas <andrea@promotux.it>
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
 """

import gtk
import gobject

from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
#from promogest.dao.Dao import Dao
#import promogest.dao.Fornitura
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Fornitore import Fornitore
#import promogest.dao.ScontoFornitura
from promogest.dao.ScontoFornitura import ScontoFornitura
#import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo
from utils import *
from utilsCombobox import *


class AnagraficaForniture(Anagrafica):
    """ Anagrafica forniture articoli """

    def __init__(self, idArticolo=None, idFornitore=None, aziendaStr=None):
        self._articoloFissato = (idArticolo <> None)
        self._fornitoreFissato = (idFornitore <> None)
        self._idArticolo=idArticolo
        self._idFornitore=idFornitore
        if "PromoWear" in Environment.modulesList:
            import promogest.modules.PromoWear.dao.ArticoloTagliaColore
            from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica forniture articoli',
                            recordMenuLabel='_Forniture',
                            filterElement=AnagraficaFornitureFilter(self),
                            htmlHandler=AnagraficaFornitureHtml(self),
                            reportHandler=AnagraficaFornitureReport(self),
                            editElement=AnagraficaFornitureEdit(self),
                            aziendaStr=aziendaStr)


class AnagraficaFornitureFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle forniture """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_forniture_filter_table',
                                  gladeFile='_ricerca_forniture.glade')
        self._widgetFirstFocus = self.id_articolo_filter_customcombobox
        persona_giuridica=Table('persona_giuridica', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        #self.fornitore=Table('fornitore', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        #self.joinT = join(self.fornitore, persona_giuridica)
        fornitura=Table('fornitura',Environment.params['metadata'],schema = Environment.params['schema'],autoload=True)
        articolo=Table('articolo', Environment.params['metadata'],schema = Environment.params['schema'],autoload=True)
        self.joinT2 = join(articolo, fornitura)

    def draw(self):
        """Colonne della Treeview per il filtro
            Attenzione, alcuni order_by non funzionano, indagare ...relazione con fornitura
            non molto pulita
        """
        treeview = self._anagrafica.anagrafica_filter_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Fornitore', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, (self.joinT,Fornitore.ragione_sociale))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,Fornitura.codice_articolo_fornitore))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, (self.joinT2,Articolo.codice))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy,(self.joinT2,Articolo.denominazione))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data fornitura', rendererSx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,Fornitura.data_fornitura))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo lordo', rendererDx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,Fornitura.prezzo_lordo))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo netto', rendererDx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,Fornitura.prezzo_netto))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)
        if "PromoWear" in Environment.modulesList:
            column = gtk.TreeViewColumn('Gruppo taglia', rendererSx, text=8)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'denominazione_gruppo_taglia')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Taglia', rendererSx, text=9)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'denominazione_taglia')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(70)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Colore', rendererSx, text=10)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'denominazione_colore')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(70)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Anno', rendererSx, text=11)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'anno')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(50)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Stagione', rendererSx, text=12)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'stagione')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Genere', rendererSx, text=13)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'genere')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(50)
            treeview.append_column(column)
            self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str, str, str)
        else:
           self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str)

        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        if self._anagrafica._articoloFissato:
            self.id_articolo_filter_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_filter_customcombobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(2)
            column.set_property('visible', False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(3)
            column.set_property('visible', False)
            if "PromoWear" in Environment.modulesList:
                column = self._anagrafica.anagrafica_filter_treeview.get_column(7)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(8)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(9)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(10)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(11)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(12)
                column.set_property('visible', False)
        if self._anagrafica._fornitoreFissato:
            self.id_fornitore_filter_customcombobox.setId(self._anagrafica._idFornitore)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(0)
            column.set_property('visible', False)

        self.clear()


    def clear(self):
        # Annullamento filtro
        if not(self._anagrafica._articoloFissato):
            self.id_articolo_filter_customcombobox.set_active(0)
        if not(self._anagrafica._fornitoreFissato):
            self.id_fornitore_filter_customcombobox.set_active(0)
        self.da_data_fornitura_filter_entry.set_text('')
        self.a_data_fornitura_filter_entry.set_text('')
        self.da_data_prezzo_filter_entry.set_text('')
        self.a_data_prezzo_filter_entry.set_text('')
        self.codice_articolo_fornitore_filter_entry.set_text('')
        self.refresh()


    def refresh(self, join=None):
        # Aggiornamento TreeView
        idArticolo = self.id_articolo_filter_customcombobox.getId()
        idFornitore = self.id_fornitore_filter_customcombobox.getId()
        daDataFornitura = stringToDate(self.da_data_fornitura_filter_entry.get_text())
        aDataFornitura = stringToDate(self.a_data_fornitura_filter_entry.get_text())
        daDataPrezzo = stringToDate(self.da_data_prezzo_filter_entry.get_text())
        aDataPrezzo = stringToDate(self.a_data_prezzo_filter_entry.get_text())
        codiceArticoloFornitore = prepareFilterString(self.codice_articolo_fornitore_filter_entry.get_text())

        def filterCountClosure():
            return Fornitura().count(join = join,
                                    idArticolo=idArticolo,
                                    idFornitore=idFornitore,
                                    daDataFornitura=daDataFornitura,
                                    aDataFornitura=aDataFornitura,
                                    daDataPrezzo=daDataPrezzo,
                                    aDataPrezzo=aDataPrezzo,
                                    codiceArticoloFornitore=codiceArticoloFornitore)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Fornitura().select(join = join,
                                        orderBy=self.orderBy,
                                        idArticolo=idArticolo,
                                        idFornitore=idFornitore,
                                        daDataFornitura=daDataFornitura,
                                        aDataFornitura=aDataFornitura,
                                        daDataPrezzo=daDataPrezzo,
                                        aDataPrezzo=aDataPrezzo,
                                        codiceArticoloFornitore=codiceArticoloFornitore,
                                        offset=offset,
                                        batchSize=batchSize)

        self._filterClosure = filterClosure

        fors = self.runFilter()

        self._treeViewModel.clear()

        for f in fors:
            if "PromoWear" in Environment.modulesList:
                self._treeViewModel.append((f,
                            (f.fornitore or ''),
                            (f.codice_articolo_fornitore or ''),
                            (f.codice_articolo or ''),
                            (f.articolo or ''),
                            dateToString(f.data_fornitura),
                            ('%14.' + Environment.conf.decimals + 'f') % float(f.prezzo_lordo),
                            ('%14.' + Environment.conf.decimals + 'f') % float(f.prezzo_netto),
                            (f.denominazione_gruppo_taglia or ''),
                            (f.denominazione_taglia or ''),
                            (f.denominazione_colore or ''),
                            (f.anno or ''),
                            (f.stagione or ''),
                            (f.genere or '')))
            else:
                self._treeViewModel.append((f,
                            (f.fornitore or ''),
                            (f.codice_articolo_fornitore or ''),
                            (f.codice_articolo or ''),
                            (f.articolo or ''),
                            dateToString(f.data_fornitura),
                            ('%14.' + Environment.conf.decimals + 'f') % float(f.prezzo_lordo or 0),
                            ('%14.' + Environment.conf.decimals + 'f') % float(f.prezzo_netto or 0)))


class AnagraficaFornitureHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'fornitura',
                                'Informazioni sulla fornitura')


class AnagraficaFornitureReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle forniture',
                                  defaultFileName='forniture',
                                  htmlTemplate='forniture',
                                  sxwTemplate='forniture')


class AnagraficaFornitureEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle forniture """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_forniture_detail_table',
                                'Dati fornitura',
                                gladeFile='_anagrafica_fornitura_articoli_elements.glade')
        self._widgetFirstFocus = self.codice_articolo_fornitore_entry
        self._percentualeIva = 0
        self.taglia_colore_table.hide()
        self.taglia_colore_table.set_no_show_all(True)


    def draw(self,cplx=False):
        self.id_articolo_customcombobox.setSingleValue()
        self.id_articolo_customcombobox.setOnChangedCall(self.on_id_articolo_customcombobox_changed)
        self.id_fornitore_customcombobox.setSingleValue()

        self.sconti_widget.button.connect('toggled',
                                        self.on_sconti_widget_button_toggled)

        if self._anagrafica._articoloFissato:
            self.id_articolo_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_customcombobox.set_sensitive(False)
            res = self.id_articolo_customcombobox.getData()
            self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
            self._percentualeIva = res["percentualeAliquotaIva"]
            self.percentuale_aliquota_iva_label.set_text('%5.2f' % self._percentualeIva + ' %')
        if self._anagrafica._fornitoreFissato:
            self.id_fornitore_customcombobox.setId(self._anagrafica._idFornitore)
            self.id_fornitore_customcombobox.set_sensitive(False)

        fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self.id_articolo_customcombobox.getId())
        self.id_multiplo_customcombobox.connect('clicked',
                                                self.on_id_multiplo_customcombobox_button_clicked)

        self.prezzo_lordo_entry.connect('focus_out_event', self._calcolaPrezzoNetto)


    def on_id_multiplo_customcombobox_button_clicked(self, widget, button):
        on_id_multiplo_customcombobox_clicked(widget, button, self.id_articolo_customcombobox.getId())


    def on_id_articolo_customcombobox_changed(self):
        res = self.id_articolo_customcombobox.getData()
        self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
        self._percentualeIva = res["percentualeAliquotaIva"]
        self.percentuale_aliquota_iva_label.set_text('%5.2f' % self._percentualeIva + ' %')
        fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self.id_articolo_customcombobox.getId())
        if "PromoWear" in Environment.modulesList:
            self._refreshTagliaColore(res["id"])

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Fornitura()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Fornitura().getRecord(id=dao.id)
        self._refresh()


    def _refresh(self):
        self.id_articolo_customcombobox.refresh(clear=True, filter=False)
        self.id_articolo_customcombobox.set_sensitive(True)
        if self.dao.id_articolo is None:
            if self._anagrafica._articoloFissato:
                self.dao.id_articolo = self._anagrafica._idArticolo
                self.id_articolo_customcombobox.set_sensitive(False)
        else:
            self.id_articolo_customcombobox.set_sensitive(False)
        self.id_articolo_customcombobox.setId(self.dao.id_articolo)
        res = self.id_articolo_customcombobox.getData()
        self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
        self._percentualeIva = res["percentualeAliquotaIva"]
        self.percentuale_aliquota_iva_label.set_text('%5.2f' % self._percentualeIva + ' %')
        self.id_fornitore_customcombobox.refresh(clear=True, filter=False)
        self.id_fornitore_customcombobox.set_sensitive(True)
        if self.dao.id_fornitore is None:
            if self._anagrafica._fornitoreFissato:
                self.dao.id_fornitore = self._anagrafica._idFornitore
                self.id_fornitore_customcombobox.set_sensitive(False)
        else:
            self.id_fornitore_customcombobox.set_sensitive(False)
        self.id_fornitore_customcombobox.setId(self.dao.id_fornitore)
        self.codice_articolo_fornitore_entry.set_text(self.dao.codice_articolo_fornitore or '')
        self.prezzo_lordo_entry.set_text(Environment.conf.number_format % float(self.dao.prezzo_lordo or 0))
        self.prezzo_netto_label.set_text(Environment.conf.number_format % float(self.dao.prezzo_netto or 0))
        self.scorta_minima_entry.set_text('%-6d' % int(self.dao.scorta_minima or 0))
        self.tempo_arrivo_merce_entry.set_text('%-6d' % float(self.dao.tempo_arrivo_merce or 0))
        self.fornitore_preferenziale_checkbutton.set_active(self.dao.fornitore_preferenziale or False)
        self.data_fornitura_entry.set_text(dateToString(self.dao.data_fornitura))
        self.data_prezzo_entry.set_text(dateToString(self.dao.data_prezzo))
        fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self.id_articolo_customcombobox.getId())
        findComboboxRowFromId(self.id_multiplo_customcombobox.combobox,
                              self.dao.id_multiplo)
        self.sconti_widget.setValues(self.dao.sconti, self.dao.applicazione_sconti)
        self._calcolaPrezzoNetto()
        if "PromoWear" in Environment.modulesList:
            self._refreshTagliaColore(self.dao.id_articolo)

    def _refreshTagliaColore(self, idArticolo):
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


    def _calcolaPrezzoNetto(self, widget = None, event = None):
        self.prezzo_netto_label.set_text('')
        if self.prezzo_lordo_entry.get_text() == '':
            self.prezzo_lordo_entry.set_text(Environment.conf.number_format % float(0))
        prezzoLordo = prezzoNetto = float(self.prezzo_lordo_entry.get_text())
        sconti = self.sconti_widget.getSconti()
        applicazione = self.sconti_widget.getApplicazione()
        for s in sconti:
            if s["tipo"] == 'percentuale':
                if applicazione == 'scalare':
                    prezzoNetto = prezzoNetto * (1 - float(s["valore"]) / 100)
                elif applicazione == 'non scalare':
                    prezzoNetto = prezzoNetto - prezzoLordo * float(s["valore"]) / 100
            elif s["tipo"] == 'valore':
                prezzoNetto = prezzoNetto - float(s["valore"])
        self.prezzo_netto_label.set_text(Environment.conf.number_format % float(prezzoNetto or 0))


    def saveDao(self):
        if self.id_articolo_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel, self.id_articolo_customcombobox)

        if self.id_fornitore_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel, self.id_fornitore_customcombobox)

        if (self.prezzo_lordo_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.prezzo_lordo_entry)

        if (self.prezzo_netto_label.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.prezzo_netto_label)

        if (self.data_prezzo_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.data_prezzo_entry)

        self.dao.id_articolo = self.id_articolo_customcombobox.getId()
        self.dao.id_fornitore = self.id_fornitore_customcombobox.getId()
        self.dao.codice_articolo_fornitore = self.codice_articolo_fornitore_entry.get_text()
        self.dao.id_multiplo = findIdFromCombobox(self.id_multiplo_customcombobox.combobox)
        self.dao.prezzo_lordo = float(self.prezzo_lordo_entry.get_text())
        self.dao.prezzo_netto = float(self.prezzo_netto_label.get_text())
        self.dao.scorta_minima = int(self.scorta_minima_entry.get_text())
        self.dao.tempo_arrivo_merce = int(self.tempo_arrivo_merce_entry.get_text())
        self.dao.fornitore_preferenziale = self.fornitore_preferenziale_checkbutton.get_active()
        self.dao.percentuale_iva = float(self._percentualeIva)
        self.dao.data_fornitura = stringToDate(self.data_fornitura_entry.get_text())
        self.dao.data_prezzo = stringToDate(self.data_prezzo_entry.get_text())

        sconti = []
        self.dao.applicazione_sconti = self.sconti_widget.getApplicazione()
        for s in self.sconti_widget.getSconti():
            daoSconto = ScontoFornitura()
            daoSconto.id_fornitura = self.dao.id
            daoSconto.valore = s["valore"]
            daoSconto.tipo_sconto = s["tipo"]
            sconti.append(daoSconto)

        self.dao.sconti = sconti
        self.dao.persist()


    def on_sconti_widget_button_toggled(self, button):
        if button.get_property('active') is True:
            return

        self._calcolaPrezzoNetto()
