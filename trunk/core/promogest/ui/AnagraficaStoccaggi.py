# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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

import gtk

from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.Stoccaggio import Stoccaggio

from utils import *
from utilsCombobox import *
if posso("PW"):
    from promogest.modules.PromoWear.ui.PromowearUtils import *
    from promogest.modules.PromoWear.ui import AnagraficaArticoliPromoWearExpand

class AnagraficaStoccaggi(Anagrafica):
    """ Anagrafica stoccaggi articoli """

    def __init__(self, idArticolo=None, idMagazzino=None, aziendaStr=None):
        self._articoloFissato = idArticolo
        self._magazzinoFissato = idMagazzino
        self._idArticolo=idArticolo
        self._idMagazzino=idMagazzino
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Situazione magazzino',
                            recordMenuLabel='_Stoccaggi',
                            filterElement=AnagraficaStoccaggiFilter(self),
                            htmlHandler=AnagraficaStoccaggiHtml(self),
                            reportHandler=AnagraficaStoccaggiReport(self),
                            editElement=AnagraficaStoccaggiEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)


class AnagraficaStoccaggiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica stoccaggi """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                anagrafica,
                        'anagrafica_stoccaggi_filter_table',
                        gladeFile='_anagrafica_stoccaggi_articoli_elements.glade')
        self._widgetFirstFocus = self.id_magazzino_filter_combobox
        self.orderBy=None


    def draw(self, cplx=False):

        # Colonne della Treeview per il filtro
        #TODO: FARE GLI ORDINAMENTI COLONNA
        treeview = self._anagrafica.anagrafica_filter_treeview
        rendererSx = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Magazzino', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,("Magazzino", 'denominazione'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,("Articolo", 'codice'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice a Barre', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy,("Articolo", 'codice'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, ("Articolo", 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Giacenza', rendererSx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object, str, str, str, str,str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_filter_combobox, True)
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        fillComboboxCategorieArticoli(self.id_categoria_articolo_filter_combobox, True)
        self.id_categoria_articolo_filter_combobox.set_active(0)


        if self._anagrafica._articoloFissato:
            self.id_articolo_filter_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_filter_customcombobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(1)
            column.set_property('visible', False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(2)
            column.set_property('visible', False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(3)
            column.set_property('visible', False)
        if self._anagrafica._magazzinoFissato:
            findComboboxRowFromId(self.id_magazzino_filter_combobox, self._anagrafica._idMagazzino)
            self.id_magazzino_filter_combobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(0)
            column.set_property('visible', False)
        if posso("PW"):
            fillComboboxGruppiTaglia(self.id_gruppo_taglia_articolo_filter_combobox,True)
            self.id_gruppo_taglia_articolo_filter_combobox.set_active(0)
            fillComboboxTaglie(self.id_taglia_articolo_filter_combobox)
            self.id_taglia_articolo_filter_combobox.set_active(0)
            fillComboboxColori(self.id_colore_articolo_filter_combobox, True)
            self.id_colore_articolo_filter_combobox.set_active(0)
            fillComboboxModelli(self.id_modello_filter_combobox, True)
            self.id_modello_filter_combobox.set_active(0)

            fillComboboxAnniAbbigliamento(self.id_anno_articolo_filter_combobox, True)
            self.id_anno_articolo_filter_combobox.set_active(0)

            fillComboboxStagioniAbbigliamento(self.id_stagione_articolo_filter_combobox,True)
            self.id_stagione_articolo_filter_combobox.set_active(0)

            fillComboboxGeneriAbbigliamento(self.id_genere_articolo_filter_combobox, True)
            self.id_genere_articolo_filter_combobox.set_active(0)
        else:
            self.promowear_expander_semplice.destroy()
        self.clear()


    def clear(self):
        # Annullamento filtro
        if not(self._anagrafica._magazzinoFissato):
            fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
            self.id_magazzino_filter_combobox.set_active(0)
        if not(self._anagrafica._articoloFissato):
            self.id_articolo_filter_customcombobox.set_active(0)
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        self.id_categoria_articolo_filter_combobox.set_active(0)
        self.denominazione_filter_entry.set_text("")
        self.produttore_filter_entry.set_text("")
        self.codice_filter_entry.set_text("")
        self.codice_a_barre_filter_entry.set_text("")
        self.codice_articolo_fornitore_filter_entry.set_text("")
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self.id_articolo_filter_customcombobox.getId()
        idMagazzino = findIdFromCombobox(self.id_magazzino_filter_combobox)
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        produttore = prepareFilterString(self.produttore_filter_entry.get_text())
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        codiceABarre = prepareFilterString(self.codice_a_barre_filter_entry.get_text())
        codiceArticoloFornitore = prepareFilterString(self.codice_articolo_fornitore_filter_entry.get_text())
        idFamiglia = findIdFromCombobox(self.id_famiglia_articolo_filter_combobox)
        idCategoria = findIdFromCombobox(self.id_categoria_articolo_filter_combobox)
        idStato = findIdFromCombobox(self.id_stato_articolo_filter_combobox)
        if self.cancellato_filter_checkbutton.get_active():
            cancellato = False
        else:
            cancellato = True
        self.filterDict = { "articolo":denominazione,
                            "codice":codice,
                            "codiceABarre":codiceABarre,
                            "codiceArticoloFornitore":codiceArticoloFornitore,
                            "produttore":produttore,
                            "idFamiglia":idFamiglia,
                            "idCategoria":idCategoria,
                            "idStato":idStato,
                            "cancellato":cancellato
                            }

#        if posso("PW"):
#            AnagraficaArticoliPromoWearExpand.refresh(self)

        def filterCountClosure():
            return Stoccaggio().count(idMagazzino=idMagazzino,
                                    idArticolo = idArticolo,
                                    filterDict = self.filterDict)
#                                            idArticolo=idArticolo,


        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Stoccaggio().select(orderBy=self.orderBy,
                                       idMagazzino=idMagazzino,
                                       idArticolo = idArticolo,
                                       offset=offset,
                                       batchSize=batchSize,
                                       filterDict = self.filterDict)
#                                                   idArticolo=idArticolo,
        self._filterClosure = filterClosure

        stos = self.runFilter()

        self._treeViewModel.clear()

        for s in stos:
            self._treeViewModel.append((s,
                                        (s.magazzino or ''),
                                        (s.codice_articolo or ''),
                                        (s.arti.codice_a_barre or ''),
                                        (s.articolo or ''),
                                        (str(s.giacenza) or '')))


class AnagraficaStoccaggiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'stoccaggio',
                                'Informazioni sullo stoccaggio')



class AnagraficaStoccaggiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli stoccaggi',
                                  defaultFileName='stoccaggi',
                                  htmlTemplate='stoccaggi',
                                  sxwTemplate='stoccaggi')



class AnagraficaStoccaggiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei stoccaggi """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_stoccaggi_detail_table',
                                'Dati stoccaggi',
                                gladeFile='_anagrafica_stoccaggi_articoli_elements.glade')
        self._widgetFirstFocus = self.id_magazzino_customcombobox
        if posso("PW"):
            self.promowear_frame.destroy()


    def draw(self, cplx=False):
        self.id_articolo_customcombobox.setSingleValue()

        fillComboboxMagazzini(self.id_magazzino_customcombobox.combobox)
        self.id_magazzino_customcombobox.connect('clicked',
                                                 on_id_magazzino_customcombobox_clicked)

        if self._anagrafica._articoloFissato:
            self.id_articolo_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_customcombobox.set_sensitive(False)
        if self._anagrafica._magazzinoFissato:
            findComboboxRowFromId(self.id_magazzino_customcombobox.combobox, self._anagrafica._idMagazzino)
            self.id_magazzino_customcombobox.set_sensitive(False)


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Stoccaggio()
            self.newDao = True
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Stoccaggio().getRecord(id=dao.id)
            self.newDao = False
        self._refresh()
        return self.dao

    def _refresh(self):
        self.id_articolo_customcombobox.refresh(clear=True, filter=False)
        self.id_articolo_customcombobox.set_sensitive(True)
        if self.dao.id_articolo is None:
            if self._anagrafica._articoloFissato:
                self.dao.id_articolo = self._anagrafica._idArticolo
                self.id_articolo_customcombobox.set_sensitive(False)
        else:
            self.id_articolo_customcombobox.set_sensitive(False)
        self.id_articolo_customcombobox.setId(self.dao.id_articolo)
        self.id_magazzino_customcombobox.combobox.set_active(-1)
        self.id_magazzino_customcombobox.set_sensitive(True)
        if self.dao.id_magazzino is None:
            if self._anagrafica._magazzinoFissato:
                self.dao.id_magazzino = self._anagrafica._idMagazzino
                self.id_magazzino_customcombobox.set_sensitive(False)
        else:
            self.id_magazzino_customcombobox.set_sensitive(False)
        findComboboxRowFromId(self.id_magazzino_customcombobox.combobox, self.dao.id_magazzino)
        self.scorta_minima_entry.set_text(str(self.dao.scorta_minima or 0))
        self.livello_riordino_entry.set_text(str(self.dao.livello_riordino or 0))
        self.data_fine_scorte_entry.set_text(dateToString(self.dao.data_fine_scorte))
        self.data_prossimo_ordine_entry.set_text(dateToString(self.dao.data_prossimo_ordine))
        if posso("PW"):
            self.colore_label.set_text(self.dao.denominazione_colore or "")
            self.stagione_label.set_text(self.dao.stagione or "" )
            self.genere_label.set_text(self.dao.genere or "")
            try:
                tagliageneregruppotaglia = self.dao.denominazione_gruppo_taglia + " " + \
                                            self.dao.denominazione_taglia
            except:
                tagliageneregruppotaglia = ""
            self.taglia_label.set_markup(tagliageneregruppotaglia)

    def saveDao(self):
        if findIdFromCombobox(self.id_magazzino_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel, self.id_magazzino_customcombobox.combobox)
        idMagazzino = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        idArticolo = self.id_articolo_customcombobox.getId()
        if not idArticolo:
            obligatoryField(self.dialogTopLevel, self.id_articolo_customcombobox)
        elif idArticolo:
            a = Stoccaggio().select(idArticolo=idArticolo,idMagazzino=idMagazzino)
            if a:
#                msg = "Attenzione !\n\n L'Articolo è già presente nel magazzino!"
#                dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
#                                            gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK, msg)
#                response = dialog.run()
#                dialog.destroy()
#                raise Exception("Tentativo di inserimento di un articolo esistente")
                a[0].scorta_minima = int(self.scorta_minima_entry.get_text() or 0)
                a[0].livello_riordino = int(self.livello_riordino_entry.get_text() or 0)
                a[0].data_fine_scorte = stringToDate(self.data_fine_scorte_entry.get_text())
                a[0].data_prossimo_ordine = stringToDate(self.data_prossimo_ordine_entry.get_text())
                a[0].persist()
                return
        self.dao.id_magazzino = idMagazzino
        self.dao.id_articolo = idArticolo
        self.dao.scorta_minima = int(self.scorta_minima_entry.get_text() or 0)
        self.dao.livello_riordino = int(self.livello_riordino_entry.get_text() or 0)
        self.dao.data_fine_scorte = stringToDate(self.data_fine_scorte_entry.get_text())
        self.dao.data_prossimo_ordine = stringToDate(self.data_prossimo_ordine_entry.get_text())
        self.dao.persist()
