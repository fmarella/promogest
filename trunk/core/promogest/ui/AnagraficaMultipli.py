# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas   <andrea@promotux.it>
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

from promogest import Environment
from promogest.dao.Multiplo import Multiplo

from promogest.lib.utils import *
from utilsCombobox import fillComboboxUnitaBase, findIdFromCombobox



class AnagraficaMultipli(Anagrafica):
    """ Anagrafica multipli unita di misura """

    def __init__(self, idArticolo = None):
        self._articoloFissato = (idArticolo <> None)
        self._idArticolo = idArticolo
        if self._idArticolo is not None:
            articolo = leggiArticolo(self._idArticolo)
            self._idUnitaBase = articolo["idUnitaBase"]
        else:
            self._idUnitaBase = None
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica unita'' di misura derivate',
                            recordMenuLabel='_Multipli',
                            filterElement=AnagraficaMultipliFilter(self),
                            htmlHandler=AnagraficaMultipliHtml(self),
                            reportHandler=AnagraficaMultipliReport(self),
                            editElement=AnagraficaMultipliEdit(self))
        self.records_file_export.set_sensitive(True)

    def on_record_edit_activate(self, widget, path=None, column=None):
        dao = self.filter.getSelectedDao()
        if self._idArticolo is not None and dao.id_unita_base is not None:
            msg = "Il multiplo e' generico !!"
            messageInfo(msg=msg)
            return

        Anagrafica.on_record_edit_activate(self, widget, path, column)



class AnagraficaMultipliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei multipli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                              anagrafica,
                              root='anagrafica_multipli_filter_table',
                              path='_anagrafica_multipli_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def draw(self):
        self._treeViewModel = self.filter_listore
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "descrizione_column":
            return self._changeOrderBy(column,(None,Multiplo.denominazione))
        if column.get_name() == "descrizione_breve_column":
            return self._changeOrderBy(column,(None,Multiplo.denominazione_breve))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self._anagrafica._idArticolo
        idUnitaBase = None

        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        multiplo = Multiplo()
        def filterCountClosure():
            return multiplo.count(denominazione=denominazione,
                                idArticolo=idArticolo,
                                idUnitaBase=idUnitaBase)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return multiplo.select(orderBy=self.orderBy,
                                denominazione=denominazione,
                                idArticolo=idArticolo,
                                idUnitaBase=idUnitaBase,
                                offset=offset,
                                batchSize=batchSize)

        self._filterClosure = filterClosure

        muls = self.runFilter()

        self._treeViewModel.clear()

        for m in muls:
            self._treeViewModel.append((m,
                                        (m.denominazione or ''),
                                        (m.denominazione_breve or ''),
                                        (('%-6.4f') % (m.moltiplicatore or 0)),
                                        (m.unita_base or ''),
                                        (m.articolo or '')))

        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)



class AnagraficaMultipliHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'multiplo',
                                'Informazioni sul multiplo')



class AnagraficaMultipliReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei multipli',
                                  defaultFileName='multipli',
                                  htmlTemplate='multipli',
                                  sxwTemplate='multipli')



class AnagraficaMultipliEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei multipli """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'Dati multiplo',
                                root='anagrafica_multipli_detail_table',
                                path='_anagrafica_multipli_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry


    def draw(self,cplx=False):
        #Popola combobox unita di misura base
        fillComboboxUnitaBase(self.id_unita_base_combobox)
        if self._anagrafica._idUnitaBase is not None:
            self.id_unita_base_combobox.set_sensitive(False)


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Multiplo()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Multiplo().getRecord(id=dao.id)
        self._refresh()
        return self.dao

    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.denominazione_breve_entry.set_text(self.dao.denominazione_breve or '')
        moltiplicatore = self.dao.moltiplicatore or 0
        self.moltiplicatore_entry.set_text('%-6.4f' % moltiplicatore)
        findComboboxRowFromId(self.id_unita_base_combobox,
                              self.dao.id_unita_base or self._anagrafica._idUnitaBase)
        if self._anagrafica._idUnitaBase is not None:
            self.id_unita_base_combobox.set_sensitive(False)


    def saveDao(self, tipo=None):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        if (self.denominazione_breve_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_breve_entry)

        if (self.moltiplicatore_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.moltiplicatore_entry)

        if findIdFromCombobox(self.id_unita_base_combobox) is None:
            obligatoryField(self.dialogTopLevel, self.id_unita_base_combobox)

        if self._anagrafica._idArticolo is not None:
            if self.dao.id_unita_base is not None:
                # il multiplo esiste gia' ed e' generico e tale deve restare
                return
            else:
                # e' un multiplo legato all'articolo
                self.dao.id_articolo = self._anagrafica._idArticolo
                self.dao.id_unita_base = None
        else:
            # il multiplo e' generico
            self.dao.id_articolo = None
            self.dao.id_unita_base = findIdFromCombobox(self.id_unita_base_combobox)

        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.denominazione_breve =self.denominazione_breve_entry.get_text()
        self.dao.moltiplicatore = float(self.moltiplicatore_entry.get_text())
        self.dao.persist()
