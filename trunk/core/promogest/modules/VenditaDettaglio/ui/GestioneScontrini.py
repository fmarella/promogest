# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import gtk, gobject
import os, popen2
import gtkhtml2
from promogest.dao.DaoUtils import giacenzaSel
from datetime import datetime, timedelta
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.ui.utils import *
from promogest.ui import utils
from jinja2 import Environment  as Env
from jinja2 import FileSystemLoader,FileSystemBytecodeCache


class GestioneScontrini(GladeWidget):
    """ Classe per la gestione degli scontrini emessi """

    def __init__(self, idArticolo = None,
                       daData = None,
                       aData = None,
                       righe = []):
        self._idArticolo = idArticolo
        self._daData = daData
        self._aData = aData
        self._righe = righe
        self._htmlTemplate = None
        self.dao = None

        GladeWidget.__init__(self, 'generic_dialog',
                fileName="promogest/modules/VenditaDettaglio/gui/generic_dialog.glade", isModule=True)
        self._window = self.generic_dialog

        self.placeWindow(self._window)
        self.draw()

    def draw(self):
        self._window.set_title('Scontrini emessi')
        rhesus_button = gtk.Button(stock=gtk.STOCK_REDO)
        alignment = rhesus_button.get_children()[0]
        hbox = alignment.get_children()[0]
        image, label = hbox.get_children()
        label.set_text('_Reso')
        label.set_use_underline(True)
        quit_button = gtk.Button(stock=gtk.STOCK_QUIT)
        self.main_hbuttonbox.pack_start(rhesus_button)
        self.main_hbuttonbox.pack_end(quit_button)
        #self._window.add_action_widget(rhesus_button, gtk.RESPONSE_APPLY)
        #self._window.add_action_widget(quit_button, gtk.RESPONSE_CANCEL)

        rhesus_button.connect('clicked', self.on_rhesus_button_clicked)
        quit_button.connect('clicked', self.on_scontrini_window_close)

        main_hpaned = gtk.HPaned()
        self.main_vbox.add(main_hpaned)

        self.filterss = FilterWidget(owner=self, filtersElement=GladeWidget(rootWidget='scontrini_filter_table',
            fileName="VenditaDettaglio/gui/_scontrini_emessi_elements.glade", isModule=True))
        self.filters = self.filterss.filtersElement
        self.filterTopLevel = self.filterss.getTopLevel()
        main_hpaned.pack1(self.filterTopLevel)
        self.detail = GladeWidget(rootWidget = 'scontrini_detail_vbox',
            fileName="VenditaDettaglio/gui/_scontrini_emessi_elements.glade", isModule=True)
        self.detailTopLevel = self.detail.getTopLevel()
        main_hpaned.pack2(self.detailTopLevel)

        self.filterss.filter_scrolledwindow.set_policy(hscrollbar_policy = gtk.POLICY_AUTOMATIC,
                                                     vscrollbar_policy = gtk.POLICY_AUTOMATIC)
        self.filterss.filter_body_label.set_markup('<b>Elenco scontrini</b>')
        self.filterss.filter_body_label.set_property('visible', True)


        # Colonne della Treeview per il filtro
        treeview = self.filterss.resultsElement
        model = self.filterss._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str)

        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Data', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, 'data_inserimento, id')
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Totale', rendererDx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Contanti', rendererDx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Assegni', rendererDx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('C di Cr', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data M.M.', rendererSx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, 'data_movimento')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('N° M.M.', rendererSx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, 'numero_movimento')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_model(model)

        self.filters.id_articolo_filter_customcombobox.setId(self._idArticolo)

        if self._daData is None:
            self.filters.da_data_filter_entry.setNow()
        else:
            self.filters.da_data_filter_entry.set_text(self_daData)
        if self._aData is None:
            self.filters.a_data_filter_entry.setNow()
        else:
            self.filters.a_data_filter_entry.set_text(self_aData)
        self.defaultFileName = "scontrino.html"
        self._htmlTemplate = "promogest/modules/VenditaDettaglio/templates"
        self.refreshHtml()


        self.refresh()

    def clear(self):
        # Annullamento filtro
        self.filters.id_articolo_filter_customcombobox.set_active(0)
        self.filters.da_data_filter_entry.setNow()
        self.filters.a_data_filter_entry.setNow()
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self.filters.id_articolo_filter_customcombobox.getId()
        daData = stringToDate(self.filters.da_data_filter_entry.get_text())
        aData = stringToDateBumped(self.filters.a_data_filter_entry.get_text())
        self.filterss.numRecords = TestataScontrino().count(idArticolo=idArticolo,
                                                                      daData=daData,
                                                                      aData=aData)

        self.filterss._refreshPageCount()

        scos = TestataScontrino().select( orderBy=self.filterss.orderBy,
                                                     idArticolo=idArticolo,
                                                     daData=daData,
                                                     aData=aData,
                                                     offset=self.filterss.offset,
                                                     batchSize=self.filterss.batchSize)

        self.filterss._treeViewModel.clear()

        for s in scos:
            totale = mN(s.totale_scontrino) or 0
            contanti = mN(s.totale_contanti) or 0
            assegni = mN(s.totale_assegni) or 0
            carta = mN(s.totale_carta_credito) or 0
            self.filterss._treeViewModel.append((s, dateToString(s.data_inserimento), totale,
                                               contanti, assegni, carta,
                                               dateToString(s.data_movimento), str(s.numero_movimento or '')))

        scos_no_batchSize = TestataScontrino().select( orderBy=self.filterss.orderBy,
                                                     idArticolo=idArticolo,
                                                     daData=daData,
                                                     aData=aData,
                                                     offset=None,
                                                     batchSize=None)

        self.calcolaTotale(scos_no_batchSize)

    def calcolaTotale(self, scos_no_batchSize):
        #print dir(self.filterss._treeViewModel)

        #model = self.filterss.resultsElement.get_model()
        tot=0
        for m in scos_no_batchSize:
            #print m.totale_scontrino
            tot += m.totale_scontrino
        self.filterss.label1.set_text("TOTALE SCONTRINI:")
        self.filterss.info_label.set_text( str(mN(tot)))


    def on_filter_treeview_cursor_changed(self, treeview):
        sel = self.filterss.resultsElement.get_selection()
        (model, iterator) = sel.get_selected()

        if iterator is None:
            print 'on_filter_treeview_cursor_changed(): FIXME: iterator is None!'
            return

        self.dao = model.get_value(iterator, 0)
        self.refreshHtml(self.dao)

    def on_filter_treeview_row_activated(self, treeview, path, column):
        # Not used here
        pass

    def on_filter_treeview_selection_changed(self, treeSelection):
        # Not used here
        pass

    def refreshHtml(self, dao=None):
        document =gtkhtml2.Document()
        if self.dao is None:
            html = '<html></html>'
        else:
            templates_dir = self._htmlTemplate
            jinja_env = Env(loader=FileSystemLoader(templates_dir),
                bytecode_cache = FileSystemBytecodeCache(os.path.join(Environment.promogestDir, 'temp'), '%s.cache'))
            jinja_env.globals['environment'] = Environment
            jinja_env.globals['utils'] = utils
            html = jinja_env.get_template(self.defaultFileName).render(dao=self.dao)
        document.open_stream('text/html')
        document.write_stream(html)
        document.close_stream()
        self.detail.detail_html.set_document(document)

    def on_scontrini_window_close(self, widget, event=None):
        self.destroy()
        return None

    def on_rhesus_button_clicked(self, widget):
        if self.dao is not None:
            self._righe.append(self.dao.id)
            self.on_scontrini_window_close(widget)
