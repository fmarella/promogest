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

from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.modules.ADR.dao.CategoriaTrasporto import CategoriaTrasporto
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaCategoriaTrasporto(Anagrafica):
    """ Anagrafica categoria di trasporto """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle=_('Promogest - Anagrafica categoria di trasporto'),
                            recordMenuLabel=_('_Categoria trasporto'),
                            filterElement=AnagraficaCategoriaTrasportoFilter(self),
                            htmlHandler=AnagraficaCategoriaTrasportoHtml(self),
                            reportHandler=AnagraficaCategoriaTrasportoReport(self),
                            editElement=AnagraficaCategoriaTrasportoEdit(self),
                            aziendaStr=aziendaStr)


class AnagraficaCategoriaTrasportoFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle categorie di trasporto """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_categorie_trasporto_filter_table',
                          gladeFile='ADR/gui/_anagrafica_categorie_trasporto_elements.glade',
                          module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry

    def draw(self):
        self._treeViewModel = self.filter_listore
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "denominazione_column":
            return self._changeOrderBy(column, (None, CategoriaTrasporto.denominazione))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        categoria_trasporto = CategoriaTrasporto()

        def filterCountClosure():
            return categoria_trasporto.count(denominazione=denominazione)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return categoria_trasporto.select(denominazione=denominazione,
                                        orderBy=self.orderBy,
                                        offset=offset,
                                        batchSize=batchSize)

        self._filterClosure = filterClosure

        categorie_trasporto = self.runFilter()

        self._treeViewModel.clear()
        for i in categorie_trasporto:
            self._treeViewModel.append((i,
                                        (i.denominazione or ''),
                                        (("%s") % (i.quantita_massima_trasportabile or '0')),
                                        (("%s") % (i.coefficiente_moltiplicazione_virtuale or '0'))))


class AnagraficaCategoriaTrasportoHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'categoriatrasporto',
                                _('Dettaglio categoria trasporto'))


class AnagraficaCategoriaTrasportoReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description=_('Elenco delle categorie trasporto'),
                                  defaultFileName='categorietrasporto',
                                  htmlTemplate='categorietrasporto',
                                  sxwTemplate='categorietrasporto')


class AnagraficaCategoriaTrasportoEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle categorie di trasporto """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_categorie_trasporto_detail_table',
                                _('Dati categoria di trasporto'),
                                gladeFile='ADR/gui/_anagrafica_categorie_trasporto_elements.glade',
                                module=True)
        self._widgetFirstFocus = self.denominazione_entry

    def draw(self, cplx=False):
        pass

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = CategoriaTrasporto()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = CategoriaTrasporto().getRecord(id=dao.id)
        self._refresh()

    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.quantita_massima_trasportabile_entry.set_text(('%s') % (self.dao.quantita_massima_trasportabile or '0'))
        self.coefficiente_moltiplicazione_virtuale_entry.set_text(('%s') % (self.dao.coefficiente_moltiplicazione_virtuale or '0'))
        text_buffer = self.note_textview.get_buffer()
        text_buffer.set_text(self.dao.note or '')

    def saveDao(self, tipo=None):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        if (self.quantita_massima_trasportabile_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.quantita_massima_trasportabile_entry)

        if (self.coefficiente_moltiplicazione_virtuale_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.coefficiente_moltiplicazione_virtuale_entry)

        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.quantita_massima_trasportabile = self.quantita_massima_trasportabile_entry.get_text()
        self.dao.coefficiente_moltiplicazione_virtuale = self.coefficiente_moltiplicazione_virtuale_entry.get_text()
        text_buffer = self.note_textview.get_buffer()
        self.dao.note = text_buffer.get_text(*text_buffer.get_bounds())
        self.dao.persist()
