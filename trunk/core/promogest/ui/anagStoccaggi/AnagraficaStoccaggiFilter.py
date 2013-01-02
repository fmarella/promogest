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

from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter

from promogest.dao.Stoccaggio import Stoccaggio
from promogest.dao.Magazzino import Magazzino
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *

if posso("PW"):
    from promogest.modules.PromoWear.ui.PromowearUtils import *


class AnagraficaStoccaggiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica stoccaggi """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
            anagrafica,
            root='anagrafica_stoccaggi_filter_table',
            path='_anagrafica_stoccaggi_articoli_elements.glade')
        self._widgetFirstFocus = self.id_magazzino_filter_combobox
        self.orderBy = None

    def draw(self, cplx=False):

        # Colonne della Treeview per il filtro
        #TODO: FARE GLI ORDINAMENTI COLONNA

        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
        fillComboboxFamiglieArticoli(
                        self.id_famiglia_articolo_filter_combobox, True)
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        fillComboboxCategorieArticoli(
                        self.id_categoria_articolo_filter_combobox, True)
        self.id_categoria_articolo_filter_combobox.set_active(0)

        if self._anagrafica._articoloFissato:
            self.id_articolo_filter_customcombobox.setId(
                                                self._anagrafica._idArticolo)
            self.id_articolo_filter_customcombobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(1)
            column.set_property('visible', False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(2)
            column.set_property('visible', False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(3)
            column.set_property('visible', False)
        if self._anagrafica._magazzinoFissato:
            findComboboxRowFromId(self.id_magazzino_filter_combobox,
                                            self._anagrafica._idMagazzino)
            #self.id_magazzino_filter_combobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(0)
            column.set_property('visible', False)
        if posso("PW"):
            fillComboboxGruppiTaglia(
                        self.id_gruppo_taglia_articolo_filter_combobox, True)
            self.id_gruppo_taglia_articolo_filter_combobox.set_active(0)
            fillComboboxTaglie(self.id_taglia_articolo_filter_combobox)
            self.id_taglia_articolo_filter_combobox.set_active(0)
            fillComboboxColori(self.id_colore_articolo_filter_combobox, True)
            self.id_colore_articolo_filter_combobox.set_active(0)
            fillComboboxModelli(self.id_modello_filter_combobox, True)
            self.id_modello_filter_combobox.set_active(0)

            fillComboboxAnniAbbigliamento(
                        self.id_anno_articolo_filter_combobox, True)
            self.id_anno_articolo_filter_combobox.set_active(0)

            fillComboboxStagioniAbbigliamento(
                        self.id_stagione_articolo_filter_combobox, True)
            self.id_stagione_articolo_filter_combobox.set_active(0)

            fillComboboxGeneriAbbigliamento(
                        self.id_genere_articolo_filter_combobox, True)
            self.id_genere_articolo_filter_combobox.set_active(0)
        else:
            self.promowear_expander_semplice.destroy()
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "magazzino_column":
            return self._changeOrderBy(column, (
                                    Magazzino, Magazzino.denominazione))
        if column.get_name() == "ragione_sociale_column":
            return self._changeOrderBy(column, (
                                    None, PersonaGiuridica_.ragione_sociale))

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
        denominazione = prepareFilterString(
                    self.denominazione_filter_entry.get_text())
        produttore = prepareFilterString(
                    self.produttore_filter_entry.get_text())
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        codiceABarre = prepareFilterString(
                    self.codice_a_barre_filter_entry.get_text())
        codiceArticoloFornitore = prepareFilterString(
                    self.codice_articolo_fornitore_filter_entry.get_text())
        idFamiglia = findIdFromCombobox(
                    self.id_famiglia_articolo_filter_combobox)
        idCategoria = findIdFromCombobox(
                    self.id_categoria_articolo_filter_combobox)
        idStato = findIdFromCombobox(self.id_stato_articolo_filter_combobox)
        if self.cancellato_filter_checkbutton.get_active():
            cancellato = False
        else:
            cancellato = True
        self.filterDict = {"articolo": denominazione,
                            "codice": codice,
                            "codiceABarre": codiceABarre,
                            "codiceArticoloFornitore": codiceArticoloFornitore,
                            "produttore": produttore,
                            "idFamiglia": idFamiglia,
                            "idCategoria": idCategoria,
                            "idStato": idStato,
                            "cancellato": cancellato
                            }

#        if posso("PW"):
#            AnagraficaArticoliPromoWearExpand.refresh(self)

        def filterCountClosure():
            return Stoccaggio().count(idMagazzino=idMagazzino,
                                    idArticolo=idArticolo,
                                    filterDict=self.filterDict)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        def filterClosure(offset, batchSize):
            return Stoccaggio().select(orderBy=self.orderBy,
                                       idMagazzino=idMagazzino,
                                       idArticolo=idArticolo,
                                       offset=offset,
                                       batchSize=batchSize,
                                       filterDict=self.filterDict)
        self._filterClosure = filterClosure

        stos = self.runFilter()

        self.filter_listore.clear()

        for s in stos:
            self.filter_listore.append((s,
                                        (s.magazzino or ''),
                                        (s.codice_articolo or ''),
                                        (s.arti.codice_a_barre or ''),
                                        (s.articolo or ''),
                                        (str(s.giacenza[0]) or '')))
