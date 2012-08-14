# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012,2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
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
from promogest.dao.FamigliaArticolo import FamigliaArticolo
from promogest.dao.Articolo import Articolo
from promogest.lib.utils import *
from utilsCombobox import *


class AnagraficaFamiglieArticoli(Anagrafica):
    """ Anagrafica famiglie degli articoli """

    def __init__(self):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica famiglie articoli',
                            recordMenuLabel='_Famiglie',
                            filterElement=AnagraficaFamiglieArticoliFilter(self),
                            htmlHandler=AnagraficaFamiglieArticoliHtml(self),
                            reportHandler=AnagraficaFamiglieArticoliReport(self),
                            editElement=AnagraficaFamiglieArticoliEdit(self))
        self.hideNavigator()
        self.records_file_export.set_sensitive(True)
        self.duplica_button.set_sensitive(False)

    def on_record_delete_activate(self, widget):
        delete = YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel())
        if not delete:
            return
        dao = self.filter.getSelectedDao()
        if not dao:
            return
        usata = Articolo().select(idFamiglia=dao.id, batchSize=None)
        if usata:
            msg = """NON è possibile cancellare questa FAMIGLIA ARTICOLO
perchè abbinata ad uno o più articoli

ATTENZIONE ATTENZIONE!!

E' però possibile "passare" tutti gli articoli della famiglia che
si vuole cancellare ad un'altra ancora presente.
Inserite il codice ( Esattamente come è scritto) della famiglia di destinazione
qui sotto e premete SI
L'operazione è irreversibile, retroattiva e potrebbe impiegare qualche minuto.
"""
            resp, move = YesNoDialog(msg=msg, transient=self.getTopLevel(), show_entry=True)
            if resp:
                famm = FamigliaArticolo().select(codice = move)
                if famm:
                    idfam = famm[0].id
                    isfather = FamigliaArticolo().select(idPadre =idfam)
                    if isfather:
                        messageInfo(msg = "Cancellare prima i figli,\n questa è una famiglia padre non vuota ")
                        return
                else:
                    messageInfo(msg = "NON è stato possibile trovare la famiglia\n di passaggio, non faccio niente")
                    return
                for u in usata:
                    u.id_famiglia_articolo = idfam
                    u.persist()
                dao.delete()
                self.htmlHandler.setDao(None)
        else:
            dao.delete()
            self.htmlHandler.setDao(None)
        self.filter.refresh()
        self.setFocus()


class AnagraficaFamiglieArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle famiglie articoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  root='anagrafica_famiglie_articoli_filter_table',
                                  path='_anagrafica_famiglie_articoli_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.orderBy = 'denominazione'


    def draw(self):
        self.clear()


    def clear(self):
        # Annullamento filtro
        self.codice_filter_entry.set_text('')
        self.denominazione_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        def filterCountClosure():
            return FamigliaArticolo().count()

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return  FamigliaArticolo().select(offset=None,batchSize=None)

        self._filterClosure = filterClosure

        fams = self.runFilter()

        self.filter_listore.clear()

        padri= FamigliaArticolo().fathers()

        def recurse(padre,f):
            """ funzione di recursione per ogni figlio di ogni padre """
            for s in f.children:
                figlio1 = self.filter_listore.append(padre, (s,
                                                    (s.codice or ''),
                                                    (s.denominazione or ''),
                                                    (s.denominazione_breve or ''),
                                                    None))
                recurse(figlio1,s)

        for f in fams:
            if f.id == f.id_padre:
                f.id_padre= None
                f.persist()
            if not f.parent:
                padre = self.filter_listore.append(None, (f,
                                                        (f.codice or ''),
                                                        (f.denominazione or ''),
                                                        (f.denominazione_breve or ''),
                                                        None))
                if f.children:
                    recurse(padre,f)

        denominazione = emptyStringToNone(self.denominazione_filter_entry.get_text())
        codice = emptyStringToNone(self.codice_filter_entry.get_text())
        if not (denominazione is None) or not (codice is None):
            self.filter_listore.foreach(self.selectFilter, (denominazione, codice))


    def selectFilter(self, model, path, iter, (denominazione, codice)):
        #Seleziona elementi che concordano con il filtro
        c = self.filter_listore.get_value(iter, 0)
        found = False
        if denominazione is not None:
            found = (denominazione.upper() in c.denominazione.upper())
        if codice is not None:
            found = found or (codice.upper() in c.codice.upper())
        if found:
            ah =self.marcatore.get_stock()
            anagPixbuf = self.marcatore.render_icon(ah[0],ah[1], None)
            self.filter_listore.set_value(iter, 4, anagPixbuf)
            self._anagrafica.anagrafica_filter_treeview.expand_to_path(path)
        else:
            self.filter_listore.set_value(iter, 4, None)



class AnagraficaFamiglieArticoliHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'famiglia_articolo',
                                'Informazioni sulla famiglia articoli')



class AnagraficaFamiglieArticoliReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle famiglie articoli',
                                  defaultFileName='famiglie_articoli',
                                  htmlTemplate='famiglie_articoli',
                                  sxwTemplate='famiglie_articoli')



class AnagraficaFamiglieArticoliEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle famiglie articoli """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'Dati famiglia articolo',
                                root='anagrafica_famiglie_articoli_detail_table',
                                path='_anagrafica_famiglie_articoli_elements.glade')
        self._widgetFirstFocus = self.codice_entry

    def draw(self,cplx=False):
        #Popola combobox famiglie articoli
        fillComboboxFamiglieArticoli(self.id_padre_combobox)

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = FamigliaArticolo()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            #self.dao = FamigliaArticolo().getRecord(id = dao.id)
            self.dao = dao
        self._refresh()
        return self.dao

    def _refresh(self):
        self.codice_entry.set_text(self.dao.codice or '')
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.denominazione_breve_entry.set_text(self.dao.denominazione_breve or '')
        fillComboboxFamiglieArticoli(self.id_padre_combobox, ignore=[self.dao.id])
        findComboboxRowFromId(self.id_padre_combobox, self.dao.id_padre)

    def saveDao(self, tipo=None):
        if (self.codice_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.codice_entry,
            msg="Codice Famiglia Articolo.\n\n Campo Obbligatorio!")
            self.dao.codice = omogeneousCode(section="Famiglie", string=self.dao.codice )

        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry,
            msg="Denominazione Famiglia Articolo.\n\n Campo Obbligatorio!")

        if (self.denominazione_breve_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_breve_entry,
            msg="Denominazione Breve Famiglia Articolo.\n\n Campo Obbligatorio!")

        daoEsistente = FamigliaArticolo().select(codice=self.codice_entry.get_text())
        if daoEsistente:
            messageInfo(msg="""ATTENZIONE!!
Una famiglia con lo stesso codice esiste già
Verrà aggiornata la precedente.""")
            del self.dao
            self.dao = daoEsistente[0]

        self.dao.codice = self.codice_entry.get_text()
        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.denominazione_breve =self.denominazione_breve_entry.get_text()
        self.dao.id_padre = findIdFromCombobox(self.id_padre_combobox)
        if self.dao.id and self.dao.id == self.dao.id_padre:
            messageInfo(msg="NON SI PUÒ ASSEGNARE QUESTO COME PADRE\n È UGUALE AL FIGLIO ")
            return
        else:
            self.dao.persist()
