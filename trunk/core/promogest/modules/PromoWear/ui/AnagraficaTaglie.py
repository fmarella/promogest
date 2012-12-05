# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.dao.GruppoTagliaTaglia import GruppoTagliaTaglia
from promogest.modules.PromoWear.ui.PromowearUtils import *
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *


class AnagraficaTaglie(Anagrafica):
    """ Anagrafica taglie degli articoli
    """

    def __init__(self):
        Anagrafica.__init__(self,
                            windowTitle='PromoWear - Anagrafica taglie',
                            recordMenuLabel='_Taglie',
                            filterElement=AnagraficaTaglieFilter(self),
                            htmlHandler=AnagraficaTaglieHtml(self),
                            reportHandler=AnagraficaTaglieReport(self),
                            editElement=AnagraficaTaglieEdit(self))
        self.hideNavigator()
        self.records_file_export.set_sensitive(True)

    def on_anagrafica_filter_treeview_selection_changed(self, treeSelection):
        (model, iterator) = treeSelection.get_selected()
        if iterator is None:
            # No items are currently selected
            dao = None
        else:
            dao = model.get_value(iterator, 0)

        if not isinstance(dao, GruppoTagliaTaglia):
            self.htmlHandler.setDao(None)
            return

        if dao.id_taglia == 1:
            # La taglia 1 (n/a) e` read-only
            Anagrafica.on_anagrafica_filter_treeview_selection_changed(self, treeSelection)
        else:
            Anagrafica.on_anagrafica_filter_treeview_selection_changed(self, treeSelection)

    def on_record_edit_activate(self, widget, path=None, column=None):
        dao = self.filter.getSelectedDao()
        if not isinstance(dao, GruppoTagliaTaglia):
            return
        if dao.id_taglia == 1:
            # La taglia 1 (n/a) e` read-only
            return
        Anagrafica.on_record_edit_activate(self, widget, path=path,
                                           column=column)


class AnagraficaTaglieFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle taglie promoWear """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                  anagrafica,
                  root='anagrafica_taglie_filter_table',
                  path='PromoWear/gui/_anagrafica_taglie_elements.glade',
                  isModule=True)
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.orderBy = 'denominazione'

    def draw(self, cplx=False):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', renderer, pixbuf=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = self.anagrafica_filter_treestore
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)
        self.refresh()

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        def filterCountClosure():
            return GruppoTagliaTaglia().count()

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return GruppoTagliaTaglia().select(batchSize=None)

        self._filterClosure = filterClosure

        gruppiTaglieTaglie = self.runFilter()

        self._treeViewModel.clear()

        gruppiTaglie = set()
        parentNodes = {}
        for gruppoTagliaTaglia in gruppiTaglieTaglie:
            if gruppoTagliaTaglia.id_gruppo_taglia not in gruppiTaglie:
                gruppiTaglie.add(gruppoTagliaTaglia.id_gruppo_taglia)
                gruppoTaglia = GruppoTaglia().getRecord(id =gruppoTagliaTaglia.id_gruppo_taglia)
                parentNode = self._treeViewModel.append(None,
                                            (gruppoTaglia,
                                             gruppoTaglia.denominazione,
                                             gruppoTaglia.denominazione_breve,
                                             None))
                parentNodes[gruppoTagliaTaglia.id_gruppo_taglia] = parentNode
            taglia = Taglia().getRecord(id=gruppoTagliaTaglia.id_taglia)
            node = self._treeViewModel.append(parentNodes[gruppoTagliaTaglia.id_gruppo_taglia],
                                              (gruppoTagliaTaglia,
                                               taglia.denominazione,
                                               taglia.denominazione_breve,
                                               None))

        self._anagrafica.anagrafica_filter_treeview.collapse_all()

        denominazione = emptyStringToNone(self.denominazione_filter_entry.get_text())
        if not (denominazione is None):
            self._treeViewModel.foreach(self.selectFilter, denominazione)

    def selectFilter(self, model, path, iter, denominazione):
        #Seleziona elementi che concordano con il filtro
        c = model.get_value(iter, 0)
        found = False
        if isinstance(c, GruppoTagliaTaglia):
            taglia = Taglia().getRecord(id= c.id_taglia)
            found = denominazione.upper() in taglia.denominazione.upper()
        elif isinstance(c, GruppoTaglia):
            found = denominazione.upper() in c.denominazione.upper()

        if found:
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_GO_BACK,
                                           GTK_ICON_SIZE_BUTTON)
            model.set_value(iter, 3, anagPixbuf)
            self._anagrafica.anagrafica_filter_treeview.expand_to_path(path)
        else:
            model.set_value(iter, 3, None)


class AnagraficaTaglieHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'taglia',
                                'Informazioni sulla famiglia articoli')


class AnagraficaTaglieReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle taglie',
                                  defaultFileName='taglie',
                                  htmlTemplate='taglie',
                                  sxwTemplate='taglie')


class AnagraficaTaglieEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle famiglie articoli """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                anagrafica,
                'Dati taglia',
                root='anagrafica_taglie_detail_table',
                path="PromoWear/gui/_anagrafica_taglie_elements.glade",
                isModule=True)
        self._widgetFirstFocus = self.denominazione_entry

    def draw(self, cplx=False):
        """popola combobox gruppi taglia"""
        fillComboboxGruppiTaglia(self.gruppo_taglia_combobox)

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            self.dao = GruppoTagliaTaglia()

        self.taglia = None
        self._refresh()
        return self.dao

    def _refresh(self):
        if self.dao.id_taglia is not None:
            self.taglia = Taglia().getRecord(id= self.dao.id_taglia)
        else:
            self.taglia = Taglia()
        self.denominazione_entry.set_text(self.taglia.denominazione or '')
        self.denominazione_breve_entry.set_text(self.taglia.denominazione_breve or '')
        fillComboboxGruppiTaglia(self.gruppo_taglia_combobox)
        findComboboxRowFromId(self.gruppo_taglia_combobox,
                                                self.dao.id_gruppo_taglia)
        self.ordine_spinbutton.set_value(self.dao.ordine or 1)

    def saveDao(self, tipo=None):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        id_gruppo_taglia = findIdFromCombobox(self.gruppo_taglia_combobox)
        if id_gruppo_taglia is None:
            obligatoryField(self.dialogTopLevel, self.gruppo_taglia_combobox)
#        if id_gruppo_taglia == 1:
#            obligatoryField(self.dialogTopLevel, self.gruppo_taglia_combobox,
#                            'Impossibile inserire nel gruppo "taglia unica" !')

        if self.dao.id_taglia is not None:
            gts = GruppoTagliaTaglia().select(idTaglia=self.dao.id_taglia,
                                                            batchSize=None)
            if len(gts) > 1:
                msg = ('La taglia e\' collegata a diversi gruppi taglia:\n' +
                       'la modifica sara\' visibile su tutti i gruppi taglia ai quali la taglia e\' legata.\n\nContinuare ?')
                if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                    raise Exception, 'Operation aborted: Errore in taglie'

        # Controllo se esiste gia' la taglia
        self.taglia.denominazione = self.denominazione_entry.get_text()
        self.taglia.denominazione_breve = self.denominazione_breve_entry.get_text()
        tag = Taglia().select(denominazioneBreve = self.taglia.denominazione_breve)
        if not tag:
            self.taglia.persist()
            tagliaid = self.taglia.id
        else:
            tagliaid = tag[0].id
        self.dao.id_gruppo_taglia = findIdFromCombobox(self.gruppo_taglia_combobox)
        self.dao.id_taglia = tagliaid
        self.dao.ordine = self.ordine_spinbutton.get_value_as_int()
        self.dao.persist()
