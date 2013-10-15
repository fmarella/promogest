# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
#    Author: Francesco Marella  <francesco.marella@anche.no>

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
from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.anagArti.AnagraficaArticoliEdit import AnagraficaArticoliEdit
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo
import promogest.dao.Fornitura

from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
if posso("PW"):
    from promogest.modules.PromoWear.ui.PromowearUtils import *
    from promogest.modules.PromoWear.ui import AnagraficaArticoliPromoWearExpand


class AnagraficaArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli articoli
    """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  root='ricerca_semplice_articoli_filter_vbox',
                                  path='_ricerca_semplice_articoli.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.ricerca_avanzata_button_alignment.destroy()

    def draw(self):
        if posso("PW"):
            AnagraficaArticoliPromoWearExpand.treeViewExpand(self, self.anagrafica_filter_treeview)
        else:
            self._treeViewModel = self.standard_liststore
            #self.promowear_expander_semplice.destroy()
            self.filter_promowear.destroy()

        self.anagrafica_filter_treeview.set_model(self._treeViewModel)
        self.id_famiglia_articolo_filter_combobox.set_wrap_width(int(setconf("Numbers", "combo_column")))
        self.id_categoria_articolo_filter_combobox.set_wrap_width(int(setconf("Numbers", "combo_column")))

        self.clear()
        self.altri_filtri_frame.hide()

    def on_altri_filtri_togglebutton_toggled(self, button):
        if button.get_active():
            self.position = self._anagrafica.anagrafica_hpaned.get_position()
            self._anagrafica.anagrafica_hpaned.set_position(self.position+300)
            self.altri_filtri_frame.show()
        else:
            self.altri_filtri_frame.hide()
            self._anagrafica.anagrafica_hpaned.set_position(self.position)

    def _reOrderBy(self, column):
        if column.get_name() == "codice_column":
            return self._changeOrderBy(column, (
                                    None, Articolo.codice))
        if column.get_name() == "descrizione_column":
            return self._changeOrderBy(column, (
                                    None, Articolo.denominazione))
        if column.get_name() == "produttore_column":
            return self._changeOrderBy(column, (
                                    None, Articolo.produttore))
        if column.get_name() == "codiceabarre_column":
            from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
            return self._changeOrderBy(column, (CodiceABarreArticolo,
                                        CodiceABarreArticolo.codice))
        if column.get_name() == "famiglia_column":
            from promogest.dao.FamigliaArticolo import FamigliaArticolo
            return self._changeOrderBy(column, (FamigliaArticolo, FamigliaArticolo.denominazione))
        if column.get_name() == "categoria_column":
            from promogest.dao.CategoriaArticolo import CategoriaArticolo
            return self._changeOrderBy(column, (CategoriaArticolo, CategoriaArticolo.denominazione))





    def _refresh_filter_comboboxes(self, widget=None):
        self.refresh()

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.codice_filter_entry.set_text('')
        self.codice_a_barre_filter_entry.set_text('')
        #self.url_articolo_entry.set_text('')
        self.codice_articolo_fornitore_filter_entry.set_text('')
        self.produttore_filter_entry.set_text('')
        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_filter_combobox, filter=True)
        fillComboboxCategorieArticoli(self.id_categoria_articolo_filter_combobox, True)
        fillComboboxStatiArticoli(self.id_stato_articolo_filter_combobox, True)
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        self.id_categoria_articolo_filter_combobox.set_active(0)
        self.id_stato_articolo_filter_combobox.set_active(0)
        self.cancellato_filter_checkbutton.set_active(False)
        if posso("PW"):
            AnagraficaArticoliPromoWearExpand.clear(self)
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
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
        self.filterDict = { "denominazione":denominazione,
                            "codice":codice,
                            "codiceABarre":codiceABarre,
                            "codiceArticoloFornitore":codiceArticoloFornitore,
                            "produttore":produttore,
                            "idFamiglia":idFamiglia,
                            "idCategoria":idCategoria,
                            "idStato":idStato,
                            "cancellato":cancellato}

        if posso("PW"):
            AnagraficaArticoliPromoWearExpand.refresh(self)

        def filterCountClosure():
            return Articolo().count(filterDict = self.filterDict)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Articolo().select(orderBy=self.orderBy,
                                        join=self.join,
                                        offset=offset,
                                        batchSize=batchSize,
                                        filterDict=self.filterDict)

        self._filterClosure = filterClosure

        arts = self.runFilter()
        self._treeViewModel.clear()
        for a in arts:
            modelRowPromoWear = []
            modelRow = []
            col = None
            if a.cancellato:
                col = 'red'

            modelRow = [a,col,(a.codice or ''),
                        (a.denominazione or ''),
                        (a.produttore or ''),
                        (a.codice_a_barre or ''),
                        (''), # qui c'era a.codice_articolo_fornitore or ""
                        (a.denominazione_famiglia or ''),
                        (a.denominazione_categoria or '')]
            if posso("PW"):
                modelRowPromoWear = [(a.denominazione_gruppo_taglia or ''),
                                    (a.denominazione_modello or ''),
                                    (a.denominazione_taglia or ''),
                                    (a.denominazione_colore or ''),
                                    (a.anno or ''),
                                    (a.stagione or ''),
                                    (a.genere or '')]
            if modelRowPromoWear:
                self._treeViewModel.append(modelRow +modelRowPromoWear)
            else:
                self._treeViewModel.append(modelRow)

    def on_taglie_colori_filter_combobox_changed(self, combobox):
        AnagraficaArticoliPromoWearExpand.on_taglie_colori_filter_combobox_changed(self,combobox)

from promogest.ui.Ricerca import Ricerca

class RicercaArticoli(Ricerca):
    """ Ricerca articoli """
    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca articoli',
                         AnagraficaArticoliFilter(self))

    def insert(self, toggleButton, returnWindow):

        def refresh():
            self.filter.refresh()
            self.filter.denominazione_filter_entry.grab_focus()

        from promogest.ui.AnagArti.AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)
        anag.on_record_new_activate(anag.record_new_button)
