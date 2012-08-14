# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012,2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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


from AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest import Environment
from promogest.dao.Magazzino import Magazzino

from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaMagazzini(Anagrafica):
    """ Anagrafica magazzini """

    def __init__(self, denominazione=None, aziendaStr=None):
        self._denominazione = denominazione
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica magazzini',
                            recordMenuLabel='_Magazzini',
                            filterElement=AnagraficaMagazziniFilter(self),
                            htmlHandler=AnagraficaMagazziniHtml(self),
                            reportHandler=AnagraficaMagazziniReport(self),
                            editElement=AnagraficaMagazziniEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)

class AnagraficaMagazziniFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei magazzini """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  root='anagrafica_magazzini_filter_table',
                                  path='_anagrafica_magazzini_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def draw(self, cplx=False):
        ## Colonne della Treeview per il filtro
        if self._anagrafica._denominazione:
            self.denominazione_filter_entry.set_text(self._anagrafica._denominazione)
        self._treeViewModel = self.filter_listore
        self.refresh()
        if self._anagrafica._denominazione:
            self._anagrafica.anagrafica_filter_treeview.grab_focus()

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())

        def filterCountClosure():
            return Magazzino().count(denominazione=denominazione)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Magazzino().select(  denominazione=denominazione,
                                orderBy=self.orderBy,
                                offset=offset,
                                batchSize=batchSize)


        self._filterClosure = filterClosure

        mags = self.runFilter()

        self._treeViewModel.clear()

        for m in mags:
            self._treeViewModel.append((m,
                                        (m.denominazione or '')))


class AnagraficaMagazziniHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'magazzino',
                                'Informazioni sul magazzino')



class AnagraficaMagazziniReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei magazzini',
                                  defaultFileName='magazzini',
                                  htmlTemplate='magazzini',
                                  sxwTemplate='magazzini')


class AnagraficaMagazziniEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei magazzini """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                  anagrafica,
                                  'Dati magazzino',
                                  root='anagrafica_magazzini_detail_table',
                                  path='_anagrafica_magazzini_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry


    def draw(self, cplx=False):
        pass


    def setDao(self, dao):
        if dao is None:
            self.dao = Magazzino()
            self._refresh()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Magazzino().getRecord(id=dao.id)
            self._refresh()
        return self.dao


    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.indirizzo_entry.set_text(self.dao.indirizzo or '')
        self.localita_entry.set_text(self.dao.localita or '')
        self.cap_entry.set_text(self.dao.cap or '')
        self.provincia_entry.set_text(self.dao.provincia or '')
        self.pvcode_entry.set_text(self.dao.pvcode or '')

    def saveDao(self, tipo=None):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)


        daoEsistente = Magazzino().select(denominazione=self.denominazione_entry.get_text())
        if daoEsistente:
            messageInfo(msg="""ATTENZIONE!!
Un magazzino con lo stesso nome esiste già
Verrà aggiornata la precedente.""")
            del self.dao
            self.dao = daoEsistente[0]


        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.indirizzo = self.indirizzo_entry.get_text()
        self.dao.localita = self.localita_entry.get_text()
        self.dao.cap = self.cap_entry.get_text()
        self.dao.provincia = self.provincia_entry.get_text()
        self.dao.pvcode = self.pvcode_entry.get_text()
        self.dao.persist()


    def on_contatti_togglebutton_clicked(self, toggleButton):
        if posso("CN"):
            toggleButton.set_active(False)
            if self.dao.id is None:
                msg = 'Prima di poter inserire i contatti occorre salvare il magazzino.\n Salvare ?'
                if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
                else:
                    toggleButton.set_active(False)
                    return

            from promogest.ui.Contatti.AnagraficaContatti import AnagraficaContatti
            anag = AnagraficaContatti(self.dao.id, 'magazzino')
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        else:
            fencemsg()
            toggleButton.set_active(False)
