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

class AnagraficaArticoli(Anagrafica):
    """ Anagrafica articoli
    """
    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica articoli',
                            recordMenuLabel='_Articoli',
                            filterElement=AnagraficaArticoliFilter(self),
                            htmlHandler=AnagraficaArticoliHtml(self),
                            reportHandler=AnagraficaArticoliReport(self),
                            editElement=AnagraficaArticoliEdit(self),
                            aziendaStr=aziendaStr)
        self.record_duplicate_menu.set_property('visible', True)
        self.records_file_export.set_sensitive(True)

    def on_record_edit_activate(self, widget, path=None, column=None, dao=None):
        if not dao:
            dao = self.filter.getSelectedDao()
        if dao:
            if dao.cancellato:
                msg = "L'articolo risulta eliminato.\nSi desidera riattivare l'articolo ?"
                if YesNoDialog(msg=msg, transient=self.getTopLevel()):
                    daoArticolo = Articolo().getRecord(id=dao.id)
                    daoArticolo.cancellato = False
                    daoArticolo.persist()

                    # toglie l'evidenziatura rossa
                    sel = self.anagrafica_filter_treeview.get_selection()
                    (model, iterator) = sel.get_selected()
                    model.set_value(iterator, 1, None)
            Anagrafica.on_record_edit_activate(self, widget, path, column, dao=dao)

    def duplicate(self,dao):
        """ Duplica le informazioni relative ad un articolo scelto su uno nuovo (a meno del codice)
        """
        if dao is None:
            return

        #self.editElement._duplicatedDaoId = dao.id
        self.editElement.dao = Articolo()

        if posso("PW"):
                # le varianti non si possono duplicare !!!
                #articoloTagliaColore = dao.articoloTagliaColore
                if dao.id_articolo_padre is not None:
                    messageInfo(msg="Attenzione !\n\n Le varianti non sono duplicabili !")
                    return

        #copia dei dati del vecchio articolo nel nuovo
        self.editElement.dao.denominazione = dao.denominazione
        self.editElement.dao.id_aliquota_iva = dao.id_aliquota_iva
        self.editElement.dao.id_famiglia_articolo = dao.id_famiglia_articolo
        self.editElement.dao.id_categoria_articolo = dao.id_categoria_articolo
        self.editElement.dao.id_unita_base = dao.id_unita_base
        self.editElement.dao.produttore = dao.produttore
        self.editElement.dao.unita_dimensioni = dao.unita_dimensioni
        self.editElement.dao.lunghezza = dao.lunghezza
        self.editElement.dao.larghezza = dao.larghezza
        self.editElement.dao.altezza = dao.altezza
        self.editElement.dao.unita_volume = dao.unita_volume
        self.editElement.dao.volume = dao.volume
        self.editElement.dao.unita_peso = dao.unita_peso
        self.editElement.dao.peso_lordo = dao.peso_lordo
        self.editElement.dao.id_imballaggio = dao.id_imballaggio
        self.editElement.dao.peso_imballaggio = dao.peso_imballaggio
        self.editElement.dao.stampa_etichetta = dao.stampa_etichetta
        self.editElement.dao.codice_etichetta = dao.codice_etichetta
        self.editElement.dao.descrizione_etichetta = dao.descrizione_etichetta
        self.editElement.dao.stampa_listino = dao.stampa_listino
        self.editElement.dao.descrizione_listino = dao.descrizione_listino
        self.editElement.dao.aggiornamento_listino_auto = \
                                        dao.aggiornamento_listino_auto
        self.editElement.dao.timestamp_variazione = dao.timestamp_variazione
        self.editElement.dao.note = dao.note
        self.editElement.dao.url_immagine = dao.url_immagine
        self.editElement.dao.cancellato = dao.cancellato
        self.editElement.dao.sospeso = dao.sospeso
        self.editElement.dao.id_stato_articolo = dao.id_stato_articolo
        self.editElement.dao.quantita_minima = dao.quantita_minima

        if posso("ADR"):
            self.editElement.adr_page.adrSetDao(self.editElement.dao)

        if self.editElement._codiceByFamiglia:
            self.editElement.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=dao.id_famiglia_articolo)
        else:
            self.editElement.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=None)

        self.editElement.setVisible(True)
        self.editElement._refresh()
        msg = 'Si desidera duplicare anche tutti i listini dell\' articolo scelto ?'
        if YesNoDialog(msg=msg, transient=self.editElement.dialogTopLevel):
            self.editElement._duplicatedDaoId = dao.id


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
            self.promowear_expander_semplice.destroy()

        self.anagrafica_filter_treeview.set_model(self._treeViewModel)
        self.id_famiglia_articolo_filter_combobox.set_wrap_width(int(setconf("Numbers", "combo_column")))
        self.id_categoria_articolo_filter_combobox.set_wrap_width(int(setconf("Numbers", "combo_column")))

        self.clear()


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


class AnagraficaArticoliHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica,
                                'articolo',
                                'Dettaglio articolo')


class AnagraficaArticoliReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli articoli',
                                  defaultFileName='articoli',
                                  htmlTemplate='articoli',
                                  sxwTemplate='articoli')

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
