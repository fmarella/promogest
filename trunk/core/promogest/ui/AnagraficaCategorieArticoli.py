# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from promogest.ui.AnagraficaSemplice import \
                        Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.Articolo import Articolo
from promogest.lib.utils import *


class AnagraficaCategorieArticoli(Anagrafica):
    """ Anagrafica categorie degli articoli """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica categorie articoli',
                            '_Categorie',
                            AnagraficaCategorieArticoliFilter(self),
                            AnagraficaCategorieArticoliDetail(self))

    def draw(self):
        """ Facoltativo ma suggerito per indicare la lunghezza
        massima della cella di testo
        NOTA: Si è dovuto riaggiungere il set_data con il dato column
        il precedente sistema automatizzato leggeva dal posizionamento
        della celrenderer nella funzione on_column_edit dentro anagraficaFilter
        purtroppo pygi gestisce la cosa in maniera diversa vedi quella funzione
        SOLUZIONE Trovata...monitorare
        """
        self.filter.descrizione_column.get_cells()[0].set_data(
                                                        'max_length', 200)
        self.filter.descrizione_breve_column.get_cells()[0].set_data(
                                                        'max_length', 10)
        #self.filter.descrizione_column.get_cells()[0].set_data('column', 0)
        #self.filter.descrizione_breve_column.get_cells()[0].set_data(
#                                                            'column', 1)
        self._treeViewModel = self.filter.filter_listore
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(
                        self.filter.denominazione_filter_entry.get_text())
        self.numRecords = CategoriaArticolo().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return CategoriaArticolo().select(denominazione=denominazione,
                                            orderBy=self.orderBy,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        self._filterClosure = filterClosure

        cats = self.runFilter()

        self._treeViewModel.clear()

        for c in cats:
            self._treeViewModel.append((c,
                                        (c.denominazione or ''),
                                        (c.denominazione_breve or '')))


class AnagraficaCategorieArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle categorie articoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                      anagrafica,
                      root='anagrafica_categorie_articoli_filter_table',
                      path='_anagrafica_categorie_articoli_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def _reOrderBy(self, column):
        if column.get_name() == "descrizione_column":
            return self._anagrafica._changeOrderBy(
                            column, (None, CategoriaArticolo.denominazione))
        if column.get_name() == "descrizione_breve_column":
            return self._anagrafica._changeOrderBy(
                        column, (None, CategoriaArticolo.denominazione_breve))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaCategorieArticoliDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle categorie articoli """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
            anagrafica,
            path='_anagrafica_categorie_articoli_elements.glade')

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            self.dao = CategoriaArticolo()
            self._anagrafica._newRow((self.dao, '', ''))
        #self._refresh()
        return self.dao

    def updateDao(self):
        if self.dao:
            self.dao = CategoriaArticolo().getRecord(id=self.dao.id)
        self._refresh()

    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator and self.dao:
            model.set_value(iterator, 0, self.dao)
            model.set_value(iterator, 1, self.dao.denominazione)
            model.set_value(iterator, 2, self.dao.denominazione_breve)

    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        denominazione = model.get_value(iterator, 1) or ''
        denominazioneBreve = model.get_value(iterator, 2) or ''
        if (denominazione == ''):
            obligatoryField(self._anagrafica.getTopLevel(),
                    self._anagrafica.anagrafica_treeview)
        if (denominazioneBreve == ''):
            obligatoryField(self._anagrafica.getTopLevel(),
                    self._anagrafica.anagrafica_treeview)
        self.dao.denominazione = denominazione
        self.dao.denominazione_breve = denominazioneBreve
        self.dao.persist()

    def deleteDao(self):
        usata = Articolo().select(idCategoria=self.dao.id, batchSize=None)
        if usata:
            msg = """NON è possibile cancellare questa CATEGORIA ARTICOLO
perchè abbinata ad uno o più articoli

ATTENZIONE ATTENZIONE!!

E' però possibile "passare" tutti gli articoli della categoria che
si vuole cancellare ad un'altra ancora presente.
Inserite la descrizione breve ( Esattamente come è scritta)
della categoria di destinazione qui sotto e premete SI
L'operazione è irreversibile,retroattiva e potrebbe impiegare qualche minuto
"""
            move, nuova_categoria = YesNoDialog(msg=msg,
                                        transient=None, show_entry=True)
            if move and nuova_categoria:
                cate = CategoriaArticolo().select(
                                    denominazioneBreveEM=nuova_categoria)
                if cate:
                    idcat = cate[0].id
                else:
                    msg = """NON è stato possibile trovare la categoria
 di passaggio, non faccio niente"""
                    messageInfo(msg=msg)
                    return
                for u in usata:
                    u.id_categoria_articolo = idcat
                    u.persist()
                self.dao.delete()
        else:
            self.dao.delete()
