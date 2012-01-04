# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

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

from promogest.ui.gtk_compat import *
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from decimal import *
from promogest import Environment
from promogest.dao.Articolo import Articolo
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.ListinoComplessoListino import ListinoComplessoListino
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import fillComboboxListini,findIdFromCombobox,findComboboxRowFromId

if posso("PW"):
    from promogest.modules.PromoWear.ui.AnagraficaListinoArticoliExpand import *

class AnagraficaListiniArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei listini """

    def __init__(self, anagrafica):
        """
        """
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_listini_articoli_filter_table',
                                  gladeFile='_anagrafica_listini_articoli_elements.glade')
        self._widgetFirstFocus = self.id_listino_filter_combobox

    def draw(self, cplx=False):
        """
        FIXME
        """
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (Listino, 'Listino.denominazione'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (Articolo, 'Articolo.codice'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (Articolo, 'Articolo.denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data variazione', rendererSx, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'data_listino_articolo'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio', rendererDx, text=5)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'prezzo_dettaglio'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso', rendererDx, text=6)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'prezzo_ingrosso'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)
        if posso("PW"):
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
                if posso("PW"):
                    drawPromoWearExpand2(self)
        if self._anagrafica._listinoFissato:
            findComboboxRowFromId(self.id_listino_filter_combobox, self._anagrafica._idListino)
            Environment.listinoFissato = self._anagrafica._idListino
            #self.id_listino_filter_combobox.set_sensitive(False)
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
        #print " ID SOTTO SLIIIIIIIIIIIIIIIIIIII", idSottoListino, idListino, idArticolo
        if not idSottoListino and self.isComplexPriceList:
            for sottolist in self.isComplexPriceList:
                multilist.append(sottolist.id_listino)
            idListino=multilist
        elif idSottoListino and self.isComplexPriceList :
            idListino=idSottoListino

        def filterCountClosure():
            """
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
                                            join=self.join,
                                            batchSize=batchSize)

        self._filterClosure = filterClosure
        self.liss = self.runFilter()
#        self.xptDaoList = self.runFilter(offset=None, batchSize=None)
        modelRow = []
        modelRowPromoWear = []
        self._treeViewModel.clear()
        for l in self.liss:
            modelRow = [l,
                        (l.denominazione or 'PP'),
                        (l.codice_articolo or ''),
                        (l.articolo or ''),
                        dateToString(l.data_listino_articolo),
                        str(mN(l.prezzo_dettaglio) or 0),
                        str(mN(l.prezzo_ingrosso) or 0)]

            if posso("PW"):
                modelRowPromoWear=[(l.denominazione_gruppo_taglia or ''),
                                        (l.denominazione_taglia or ''),
                                        (l.denominazione_colore or ''),
                                        (l.anno or ''),
                                        (l.stagione or ''),
                                        (l.genere or '')]

            if modelRowPromoWear:
                self._treeViewModel.append(modelRow +modelRowPromoWear)
            else:
                self._treeViewModel.append((modelRow))
        #Environment.listinoFissato =  None

    def on_annulla_ml_button_clicked(self, button):
        self.modifiche_listino.hide()

    def on_ok_ml_button_clicked(self, button):
        daos = self._filterClosure(None, None)
        valore = Decimal(self.valore_ml_entry.get_text() or 0)
        #if not valore:
            #return
        if self.aggiungi_ml_radio.get_active():
            segno = "+"
        else:
            segno = "-"
        if self.valore_ml_radio.get_active():
            tipo_sconto = "valore"
        else:
            tipo_sconto = "percentuale"

        if self.aggiungi_sconto_dettaglio:
            for d in daos:
                sconti_ingrosso = []
                sconti_dettaglio = []
                if valore > 0:
                    g = ScontoVenditaDettaglio()
                    g.valore = valore
                    g.tipo_sconto = tipo_sconto
                    sconti_dettaglio.append(g)
                if d.sconto_vendita_ingrosso:
                    h = ScontoVenditaIngrosso()
                    h.valore = d.sconto_vendita_ingrosso[0].valore
                    h.tipo_sconto = d.sconto_vendita_ingrosso[0].tipo_sconto
                    sconti_ingrosso.append(h)
                d.persist(sconti={"dettaglio":sconti_dettaglio,"ingrosso":sconti_ingrosso})

        elif self.aggiungi_sconto_ingrosso:
            for d in daos:
                sconti_ingrosso = []
                sconti_dettaglio = []
                if valore > 0:
                    g = ScontoVenditaIngrosso()
                    g.valore = valore
                    g.tipo_sconto = tipo_sconto
                    sconti_ingrosso.append(g)
                if d.sconto_vendita_dettaglio:
                    h = ScontoVenditaDettaglio()
                    h.valore = d.sconto_vendita_dettaglio[0].valore
                    h.tipo_sconto = d.sconto_vendita_dettaglio[0].tipo_sconto
                    sconti_ingrosso.append(h)
                d.persist(sconti={"dettaglio":sconti_dettaglio,"ingrosso":sconti_ingrosso})

        elif self.variazione_dettaglio:
            if not valore:
                return
            for d in daos:
                if segno =="+" and tipo_sconto =="valore":
                    d.prezzo_dettaglio = d.prezzo_dettaglio + valore
                elif segno =="-" and tipo_sconto =="valore":
                    d.prezzo_dettaglio = d.prezzo_dettaglio - valore
                elif segno == "+" and tipo_sconto =="percentuale":
                    d.prezzo_dettaglio = d.prezzo_dettaglio*(1+valore/100)
                elif segno == "-" and tipo_sconto =="percentuale":
                    d.prezzo_dettaglio = d.prezzo_dettaglio*(1-valore/100)
                Environment.session.add(d)
        elif self.variazione_ingrosso:
            if not valore:
                return
            for d in daos:
                if segno =="+" and tipo_sconto =="valore":
                    d.prezzo_ingrosso = d.prezzo_ingrosso + valore
                elif segno =="-" and tipo_sconto =="valore":
                    d.prezzo_ingrosso = d.prezzo_ingrosso - valore
                elif segno == "+" and tipo_sconto =="percentuale":
                    d.prezzo_ingrosso = d.prezzo_ingrosso*(1+valore/100)
                elif segno == "-" and tipo_sconto =="percentuale":
                    d.prezzo_ingrosso = d.prezzo_ingrosso*(1-valore/100)
                Environment.session.add(d)

        Environment.session.commit()
        messageInfo(msg="Operazione effettuata")
        self.modifiche_listino.hide()
        self.refresh()
