# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import gtk
import os, popen2

from promogest.dao.DaoUtils import giacenzaSel
from datetime import datetime, timedelta
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
from promogest.modules.VenditaDettaglio.ui.Distinta import Distinta
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.ui.utils import *
from promogest.ui import utils

from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML

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

        GladeWidget.__init__(self, 'scontrini_emessi',
                fileName="VenditaDettaglio/gui/scontrini_emessi.glade", isModule=True)
        self._window = self.scontrini_emessi

        self.placeWindow(self._window)
        self.draw()

    def draw(self):

        self.filterss = FilterWidget(owner=self, filtersElement=GladeWidget(rootWidget='scontrini_filter_table',
            fileName="VenditaDettaglio/gui/_scontrini_emessi_elements.glade", isModule=True))
        self.filters = self.filterss.filtersElement
        self.filterTopLevel = self.filterss.getTopLevel()
        self.main_hpaned.pack1(self.filterTopLevel)

        sw = gtk.ScrolledWindow()
        sw.set_policy(hscrollbar_policy = gtk.POLICY_AUTOMATIC,
                            vscrollbar_policy = gtk.POLICY_AUTOMATIC)
        #createHtmlObj(self)
        self.detail = createHtmlObj(self)
        sw.add(self.detail)
        self.main_hpaned.pack2(sw)

        self.filterss.filter_scrolledwindow.set_policy(hscrollbar_policy = gtk.POLICY_AUTOMATIC,
                                                     vscrollbar_policy = gtk.POLICY_AUTOMATIC)
        self.filterss.filter_body_label.set_markup('<b>Elenco scontrini</b>')
        self.filterss.filter_body_label.set_property('visible', True)

        self.filterss.hbox1.destroy()
        self.quit_button.connect('clicked', self.on_scontrini_window_close)
        # Colonne della Treeview per il filtro
        treeview = self.filterss.resultsElement
        model = self.filterss._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str)

        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Data', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, (None, 'data_inserimento'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Totale', rendererDx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, (None, 'totale_scontrino'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Contanti', rendererDx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, (None, 'totale_contanti'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Assegni', rendererDx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, (None, 'totale_assegni'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('C di Cr', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, (None, 'totale_carta_credito'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data M.M.', rendererSx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self.filterss._changeOrderBy, 'data_movimento')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('N° M.M.', rendererSx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self.filterss._changeOrderBy, 'numero_movimento')
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
            self.filterss._treeViewModel.append((s, dateTimeToString(s.data_inserimento).replace(" "," Ore: "), totale,
                                               contanti, assegni, carta,
                                               dateToString(s.data_movimento), str(s.numero_movimento or '')))

        scos_no_batchSize = TestataScontrino().select( orderBy=self.filterss.orderBy,
                                                     idArticolo=idArticolo,
                                                     daData=daData,
                                                     aData=aData,
                                                     offset=None,
                                                     batchSize=None)
        self.scontrini = scos_no_batchSize
        self.calcolaTotale(scos_no_batchSize)

    def calcolasconto(self, dao):
        if dao.sconti[0].tipo_sconto=="valore":
            return dao.sconti[0].valore
        else:
            #print ((dao.totale_scontrino*100)/dao.sconti[0].valore), (dao.totale_scontrino)
            return (100 * dao.totale_scontrino) / (100 - dao.sconti[0].valore) -(dao.totale_scontrino)
            #totale_scontato = total-totale_sconto

    def calcolaTotale(self, scos_no_batchSize):
        tot=0
        totccr = 0
        totass = 0
        totnum = 0
        totcont = 0
        tot_sconti = 0
        for m in scos_no_batchSize:
            if m.sconti:
                tot_sconti += self.calcolasconto(m)
            tot += m.totale_scontrino
            totccr += m.totale_carta_credito
            totass += m.totale_assegni
            totcont += m.totale_contanti
            totnum += 1
        self.filterss.label1.set_text("T scontrini:")
        stringa = """<b><span foreground="black" size="20000">%s</span></b> - Resto da contante:<b>%s</b> - T Carta:<b>%s</b> - T Assegni:<b>%s</b> - T Sconti:<b>%s</b> - N°:<b><span foreground="black" size="18000">%s</span></b>""" %(mN(tot),mN(totcont), mN(totccr), mN(totass),mN(tot_sconti), totnum )
        self.filterss.info_label.set_markup(str(stringa))


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
        pageData = {}
        html = '<html></html>'
        if self.dao:
            pageData = {
                    "file": "scontrino.html",
                    "dao" :self.dao
                    }
            html = renderTemplate(pageData)
        renderHTML(self.detail,html)

    #def on_quit_button_clicked(self, widget, event=None):
        #self.destroy()
        #return None


    def on_scontrini_window_close(self, widget, event=None):
        self.destroy()
        return None

    def on_rhesus_button_clicked(self, widget):
        if self.dao is not None:
            self._righe.append(self.dao.id)
            self.on_scontrini_window_close(widget)

    def on_delete_button_clicked(self, button):
        if self.dao is not None:
            msg = """ ATTENZIONE!!!!
    Si sta per cancellare uno scontrino, L'operazione
    è irreversibile per cui dovete essere sicuri di
    quel che state facendo. VUOI CANCELLARLO?"""
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   msg)
            response = dialog.run()
            dialog.destroy()
            if response ==  gtk.RESPONSE_YES:
                if self.dao.numero_movimento:
                    messageInfo(msg= """Esiste già un movimento abbinato di chiusura per scarico da cassa,
        l'operazione è comunque impossibile
        Rivolgersi all'assasistenza""")
                else:
                    Environment.pg2log.info("CANCELLO UNO SCONTRINO DAL PG2 ")
                    self.dao.delete()
                self.refresh()
            else:
                return

    def on_affluenza_oraria_chart_clicked(self, button):
        if "Statistiche" in Environment.modulesList and \
            hasattr(Environment.conf,"Statistiche") and \
            hasattr(Environment.conf.Statistiche,"affluenza_oraria_giornaliera") and\
            Environment.conf.Statistiche.affluenza_oraria_giornaliera == "yes":
            from promogest.modules.Statistiche.ui.chart import chartViewer
            chartViewer(self._window, func="affluenzaOrariaGiornaliera",scontrini= self.scontrini)
        else:
            fenceDialog()

    def on_affluenza_mensile_chart_clicked(self, button):
        if "Statistiche" in Environment.modulesList and \
            hasattr(Environment.conf,"Statistiche") and \
            hasattr(Environment.conf.Statistiche,"affluenza_giornaliera_mensile") and\
            Environment.conf.Statistiche.affluenza_giornaliera_mensile == "yes":
            from promogest.modules.Statistiche.ui.chart import chartViewer
            chartViewer(self._window, func="affluenzaGiornalieraMensile", scontrini= self.scontrini)
        else:
            fenceDialog()

    def on_affluenza_annuale_chart_clicked(self, button):
        if "Statistiche" in Environment.modulesList and \
            hasattr(Environment.conf,"Statistiche") and \
            hasattr(Environment.conf.Statistiche,"affluenza_mensile_annuale") and\
            Environment.conf.Statistiche.affluenza_mensile_annuale == "yes":
            from promogest.modules.Statistiche.ui.chart import chartViewer
            chartViewer(self._window, func="affluenzaMensileAnnuale", scontrini= self.scontrini)
        else:
            fenceDialog()

    def on_esporta_affluenza_csv_clicked(self, button):
        print "esport to csv"

    def on_aggiorna_inve_activate(self, item):
        if "Inventario" in Environment.modulesList:
            for scontrino in self.scontrini:
                for riga in scontrino.righe:
                    daoInv = Inventario().select(idArticolo=riga.id_articolo)
                    if daoInv:
                        if riga.data_inserimento > daoInv[0].data_aggiornamento:
                            print "OKKEI DEVO AGGIORNARLO"
                            quantitaprecedente = daoInv[0].quantita
                            quantitavenduta = riga.quantita
                            nuovaquantita = quantitaprecedente-quantitavenduta
                            daoInv[0].quantita= nuovaquantita
#                            daoInv.persist()

    def on_distinta_button_clicked(self, button):
        gest = Distinta(righe = self.scontrini)
        gestWnd = gest.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), gestWnd, None, None)
