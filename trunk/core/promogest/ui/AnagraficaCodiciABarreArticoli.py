# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas   <andrea@promotux.it>
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

from promogest.ui.AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaCodiciABarreArticoli(Anagrafica):
    """ Anagrafica codici a barre """

    def __init__(self, idArticolo = None):
        self._idArticolo = idArticolo
        Anagrafica.__init__(self, 'Promogest - Anagrafica codici a barre',
                            '_Codici a barre',
                            AnagraficaCodiciABarreArticoliFilter(self),
                            AnagraficaCodiciABarreArticoliDetail(self))


    def draw(self):
        # Colonne della Treeview per il filtro/modifica
        treeview = self.anagrafica_treeview
        self.row=None
        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Codice a barre', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', False)
        renderer.connect('toggled', self.on_column_edited, None, treeview)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Primario', renderer, active=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object, str, bool)
        treeview.set_model(self._treeViewModel)

        self.codBar_combo = GTK_COMBOBOXTEXT()
        self.codBar_combo.append_text("Crea Codice Random Ean13 ")
        self.codBar_combo.append_text("Crea Codice Random Ean8 ")
        self.bodyWidget.hbox1.pack_start(self.codBar_combo, True, True, 0)
        self.codBar_combo.connect('changed', self.on_generic_combobox_changed)

        treeview.set_search_column(1)

        self.refresh()

    def on_generic_combobox_changed(self,combobox):
        if self.codBar_combo.get_active()==0:
            codice = generateRandomBarCode(ean=13)
            self.on_record_new_activate(self,codice=codice)
            #self.codBar_combo.set_active(0)
        elif self.codBar_combo.get_active()==1:
            codice = generateRandomBarCode(ean=8)
            self.on_record_new_activate(self,codice=codice)
        else:
            self.codBar_combo.set_active(-1)

    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self._idArticolo
        codice = prepareFilterString(self.filter.codice_filter_entry.get_text())
        self.numRecords = CodiceABarreArticolo().count(idArticolo=idArticolo,
                                                                   codice=codice)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return CodiceABarreArticolo().select(idArticolo=idArticolo,
                                                             codice=codice,
                                                             orderBy=self.orderBy,
                                                             offset=self.offset,
                                                             batchSize=self.batchSize)

        self._filterClosure = filterClosure

        bars = self.runFilter()

        self._treeViewModel.clear()

        for b in bars:
            self._treeViewModel.append((b,
                                        (b.codice or ''),
                                        (b.primario or False)))


class AnagraficaCodiciABarreArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei codici a barre """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_codici_a_barre_articoli_filter_table',
                                  gladeFile='_anagrafica_codici_a_barre_articoli_elements.glade')
        self._widgetFirstFocus = self.codice_filter_entry


    def clear(self):
        # Annullamento filtro
        self.codice_filter_entry.set_text('')
        self.codice_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaCodiciABarreArticoliDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica dei codici a barre """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                anagrafica,
                                gladeFile='_anagrafica_codici_a_barre_articoli_elements.glade')


    def setDao(self, dao, codice=None):
        if dao is None:
            self.dao = CodiceABarreArticolo()
            self.dao.id_articolo = self._anagrafica._idArticolo
            if codice:
                self.dao.codice = codice
                self._anagrafica._newRow((self.dao, codice, False))
            else:
                self._anagrafica._newRow((self.dao, '', False))
            self._refresh()
        else:
            self.dao = dao
        return self.dao

    def updateDao(self):
        if self.dao:
            self.dao = CodiceABarreArticolo().getRecord(id=self.dao.id)
        self._refresh()


    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator and self.dao:
            model.set_value(iterator, 0, self.dao)
            model.set_value(iterator, 1, self.dao.codice)
            model.set_value(iterator, 2, self.dao.primario or False)


    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        codice = model.get_value(iterator, 1) or ''
        if (codice == ''):
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        self.verifica(codice)
        primario = model.get_value(iterator, 2)

        self.dao.id_articolo = self._anagrafica._idArticolo
        self.dao.codice = codice
        self.dao.primario = primario
        self.dao.persist()


    def deleteDao(self):
        self.dao.delete()

    def verifica(self, codice):
        bars = CodiceABarreArticolo().select(idArticolo=None,
                                                         codice=codice,
                                                         offset=None,
                                                         batchSize=None)
        if len(bars) > 0:
            # FIXME: la select non esegue una ricerca esatta !!
            if bars[0].codice != codice:
                return

            if bars[0].id_articolo != self._anagrafica._idArticolo:
                articolo = leggiArticolo(bars[0].id_articolo)
                msg = "Codice gia' assegnato all'articolo: \n\nCod. " + articolo["codice"] + " (" + articolo["denominazione"] + ")"
                messageInfo(msg=msg, transient=self._anagrafica.getTopLevel())
                raise Exception, 'Operation aborted: Cod Barre già assegnato'
