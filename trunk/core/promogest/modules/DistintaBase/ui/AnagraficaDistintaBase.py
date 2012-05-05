# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest import Environment
from promogest.dao.Articolo import Articolo
from promogest.modules.DistintaBase.dao.AssociazioneArticolo import AssociazioneArticolo
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *


class AnagraficaDistintaBase(Anagrafica):
    """
    Visualizza le distinte base
    """
    def __init__(self):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica distinte base',
                            recordMenuLabel='_Distinta Base',
                            filterElement=AnagraficaDistintaBaseFilter(self),
                            htmlHandler=AnagraficaDistintaBaseHtml(self),
                            reportHandler=AnagraficaDistintaBaseReport(self),
                            editElement=AnagraficaDistintaBaseEdit(self))
        self.record_duplicate_menu.set_property('visible', True)


    def on_record_delete_activate(self, widget):
        if not YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel()):
            return
        dao = self.filter.getSelectedDao()
        for d in dao.articoliAss:
            d.delete()

        self.filter.refresh()
        self.htmlHandler.setDao(None)
        self.setFocus()


class AnagraficaDistintaBaseFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle distinte base """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_associazioni_articoli_filter_table',
                                    gladeFile='DistintaBase/gui/_distinta_base_plugins.glade',
                                    module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.articoliprincipaliList = []

    def draw(self, cplx=False):
        #self._treeViewModel = self._anagrafica.anagrafica_filter_treeview.get_model()
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "codice_column":
            return self._changeOrderBy(column, (None, 'codice'))
        elif column.get_name() == "denominazione_column":
            return self._changeOrderBy(column, (None, 'denominazione'))
        elif column.get_name() == "produttore_column":
            return self._changeOrderBy(column, (None, 'produttore'))
        elif column.get_name() == "codice_a_barre_articolo_column":
            from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
            return self._changeOrderBy(column, (CodiceABarreArticolo, CodiceABarreArticolo.codice))
        elif column.get_name() == "codice_articolo_fornitore_column":
            return self._changeOrderBy(column, (None, 'codice_articolo_fornitore'))
        elif column.get_name() == "famiglia_articolo_column":
            from promogest.dao.FamigliaArticolo import FamigliaArticolo
            return self._changeOrderBy(column, (FamigliaArticolo, FamigliaArticolo.denominazione))
        else:  # column.get_name() == "categoria_articolo_column":
            from promogest.dao.CategoriaArticolo import CategoriaArticolo
            return self._changeOrderBy(column, (CategoriaArticolo, CategoriaArticolo.denominazione))

    def _refresh_filter_comboboxes(self, widget=None):
        self.refresh()

    def clear(self):
        """Annullamento filtro"""
        self.denominazione_filter_entry.set_text('')
        self.codice_filter_entry.set_text('')
        self.codice_a_barre_filter_entry.set_text('')
        self.codice_articolo_fornitore_filter_entry.set_text('')
        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_filter_combobox, filter=True)
        fillComboboxCategorieArticoli(self.id_categoria_articolo_filter_combobox, True)
        fillComboboxStatiArticoli(self.id_stato_articolo_filter_combobox, True)
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        self.id_categoria_articolo_filter_combobox.set_active(0)
        self.id_stato_articolo_filter_combobox.set_active(0)
        self.cancellato_filter_checkbutton.set_active(False)
        self.refresh()

    def refresh(self):
        """ Aggiornamento TreeView"""
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        produttore = prepareFilterString(self.produttore_filter_entry.get_text())
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        codiceABarre = prepareFilterString(self.codice_a_barre_filter_entry.get_text())
        codiceArticoloFornitore = prepareFilterString(self.codice_articolo_fornitore_filter_entry.get_text())
        idFamiglia = findIdFromCombobox(self.id_famiglia_articolo_filter_combobox)
        idCategoria = findIdFromCombobox(self.id_categoria_articolo_filter_combobox)
        idStato = findIdFromCombobox(self.id_stato_articolo_filter_combobox)
        if self.cancellato_filter_checkbutton.get_active():
            cancellato = True
        else:
            cancellato = False

        def filterCountClosure():
            return Articolo().count(node=True,
                                    denominazione=denominazione,
                                    codice=codice,
                                    codiceABarre=codiceABarre,
                                    codiceArticoloFornitore=codiceArticoloFornitore,
                                    produttore=produttore,
                                    idFamiglia=idFamiglia,
                                    idCategoria=idCategoria,
                                    idStato=idStato,
                                    #cancellato=cancellato
                                    )

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults() or 0

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Articolo().select(
                                    node=True,
                                    join=self.join,
                                    orderBy=self.orderBy,
                                    denominazione=denominazione,
                                    codice=codice,
                                    codiceABarre=codiceABarre,
                                    codiceArticoloFornitore=codiceArticoloFornitore,
                                    produttore=produttore,
                                    idFamiglia=idFamiglia,
                                    idCategoria=idCategoria,
                                    idStato=idStato,
                                    #cancellato=cancellato,
                                    offset=offset,
                                    batchSize=batchSize)

        self._filterClosure = filterClosure

        arts = self.runFilter()
        self.distinta_base_filter_listore.clear()
        for a in arts:
            col = None
            if a.cancellato:
                col = 'red'
            #if a.isNode:
            self.distinta_base_filter_listore.append((a,
                                        col,
                                        (a.codice or ''),
                                        (a.denominazione or ''),
                                        (a.produttore or ''),
                                        (a.codice_a_barre or ''),
                                        (a.codice_articolo_fornitore or ''),
                                        (a.denominazione_famiglia or ''),
                                        (a.denominazione_categoria or '')))



class AnagraficaDistintaBaseHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'distinta_base',
                                'Dettaglio distinta base',
                                #templatesHTMLDir ="promogest/modules/DistintaBase/templates/"
 )


class AnagraficaDistintaBaseReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco distinte base',
                                  defaultFileName='articoli_associati',
                                  htmlTemplate='articoli_associati',
                                  sxwTemplate='articoli_associati')

class AnagraficaDistintaBaseEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle distinte base """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_associazioni_articoli_detail_vbox',
                                'Dati articolo',
                                gladeFile='DistintaBase/gui/_distinta_base_plugins.glade',
                                module=True)
        self._widgetFirstFocus = self.articolo_principale_button
        self.remove_article_button.set_sensitive(False)
        self._loading= False
        self.articoliAssociatiList = []

    def draw(self, cplx=False):
        self._assTreeViewModel = self.articoli_associati_liststore

    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        value = value.replace(",",".")
        model[path][0].quantita = Decimal(value)
        model[path][4] = value

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.daoPadre = Articolo()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.daoPadre = Articolo().getRecord(id=dao.id)
            self.articoliAssociatiList = self.daoPadre.articoliAss
        self._refresh()

    def _refresh(self):
        self._loading = True
        self.descrizione_label.set_text('')
        self.codice_label.set_text('')
        self.articoli_associati_liststore.clear()

        for articolo in self.articoliAssociatiList:
            col = None
            if articolo.cancellato:
                col = 'red'
            codice = articolo.codice
            denominazione = articolo.denominazione

            #else:
                #if articolo.cancellato:
                    #col = 'red'
                #codice = articolo.codice
                #denominazione = articolo.denominazione
            quantita = articolo.quantita or 0
            self.articoli_associati_liststore.append([articolo,
                                        col,
                                        codice,
                                        denominazione,
                                        quantita])

        if self.daoPadre.id is None:
            string='<b>Selezionare un articolo principale</b>'
            self.descrizione_label.set_markup(string)
        else:
            self.descrizione_label.set_text(self.daoPadre.denominazione)

        if self.daoPadre.codice is not None:
            self.codice_label.set_markup(str(self.daoPadre.codice))

    def on_add_article_button_clicked(self, button):
        self.ricercaArticolo()

    def saveDao(self, tipo=None):
        """
        salva tutte le distinte base nel database
        """
        for articolo in self.articoliAssociatiList:
            articolo.persist()

    def on_articolo_principale_button_clicked(self, button):
        self.ricercaArticolo(isNode=True)

    def ricercaArticolo(self, isNode= False):

        def on_ricerca_articolo_hide(anagWindow, anag, isNode=False):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            if isNode:
                print "SEI PADRE"
                self.mostraArticoloPadre(anag.dao)
            else:
                print "SEI FIGLIO"
                self.mostraArticoloFiglio(anag.dao)

        codice = None
        codiceABarre = None
        denominazione = None
        codiceArticoloFornitore = None

        from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
        anag = RicercaComplessaArticoli(denominazione=denominazione,
                                        codice=codice,
                                        codiceABarre=codiceABarre,
                                        codiceArticoloFornitore=codiceArticoloFornitore)
        anag.setTreeViewSelectionType(GTK_SELECTIONMODE_SINGLE)

        anagWindow = anag.getTopLevel()
        anagWindow.connect("hide",
                           on_ricerca_articolo_hide,
                           anag, isNode)
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()


    def mostraArticoloPadre(self, dao):
        self.daoPadre = dao
        daoAssociazione= AssociazioneArticolo()
        daoAssociazione.id_figlio = dao.id
        daoAssociazione.id_padre = self.daoPadre.id
        daoAssociazione.denominazione = dao.denominazione
        daoAssociazione.codice = dao.codice
        daoAssociazione.posizione = 0
        daoAssociazione.cancellato = dao.cancellato
        self.articoliAssociatiList.append(daoAssociazione)
        for articolo in self.articoliAssociatiList:
            articolo.id_associato = id
        self._refresh()

    def mostraArticoloFiglio(self,dao):
        daoAssociazione= AssociazioneArticolo()
        # qui è sufficiente settare solo le proprietà dell'associazione che vengono poi visualizzate nella treeview
        # nel salvataggio dellla stessa sono necessari solo id_articolo, e id_associato
        daoAssociazione.id_figlio = dao.id
        daoAssociazione.id_padre = self.daoPadre.id
        daoAssociazione.denominazione = dao.denominazione
        daoAssociazione.codice = dao.codice
        daoAssociazione.cancellato = dao.cancellato
        daoAssociazione.posizione = len(self.articoliAssociatiList)
        self.articoliAssociatiList.append(daoAssociazione)
        self._refresh()

    def on_remove_article_button_clicked(self, button):
        (model,iter) = self.articoli_associati_treeview.get_selection().get_selected()
        for dao in self.articoliAssociatiList:
            if model[iter][0] == dao:
                self.articoliAssociatiList.remove(dao)
                if dao.id is not None:
                    dao.delete()
        model.remove(iter)
        for art in self.articoliAssociatiList:
            art.posizione = self.articoliAssociatiList.index(art)

    def on_articoli_associati_treeview_row_activated(self, treeview, path, column):
        self.remove_article_button.set_sensitive(True)
