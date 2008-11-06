# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import gtk
import gobject

from promogest.ui.AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.Dao import Dao
from promogest.ui.utils import *
#if "PromoWear" in Environment.modulesList:
from promogest.modules.PromoWear.ui.PromowearUtils import *
from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
import promogest.modules.PromoWear.dao.ArticoloTagliaColore
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.Colore import Colore
import promogest.modules.PromoWear.dao.ArticoloPromowear
#try:
from promogest.modules.PromoWear.dao.ArticoloPromowear import ArticoloPromowear
#except ImportError:
    #print "Errore import"
#else:
    #import promogest.dao.Articolo
    #from promogest.dao.Articolo import Articolo

from promogest.ui.GladeWidget import GladeWidget


class AnagraficaArticoli(Anagrafica):
    """ Anagrafica articoli """

    def __init__(self, aziendaStr=None):
        if "PromoWear" in Environment.modulesList:
            self._taglia_colore = Environment.taglia_colore or False
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica articoli',
                            recordMenuLabel='_Articoli',
                            filterElement=AnagraficaArticoliFilter(self),
                            htmlHandler=AnagraficaArticoliHtml(self),
                            reportHandler=AnagraficaArticoliReport(self),
                            editElement=AnagraficaArticoliEdit(self),
                            aziendaStr=aziendaStr)
        self.record_duplicate_menu.set_property('visible', True)

    def on_record_edit_activate(self, widget, path=None, column=None):
        dao = self.filter.getSelectedDao()
        if dao.cancellato:
            msg = "L'articolo risulta eliminato.\nSi desidera riattivare l'articolo ?"
            dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                daoArticolo = Articolo(Environment.connection, dao.id)
                daoArticolo.cancellato = False
                daoArticolo.persist()

                # toglie l'evidenziatura rossa
                sel = self.anagrafica_filter_treeview.get_selection()
                (model, iterator) = sel.get_selected()
                model.set_value(iterator, 1, None)
            else:
                return
        Anagrafica.on_record_edit_activate(self, widget, path, column)


    def duplicate(self,dao):
        """ Duplica le informazioni relative ad un articolo scelto su uno nuovo (a meno del codice) """
        if dao is None:
            return

        self.editElement._duplicatedDaoId = dao.id
        self.editElement.dao = Articolo(Environment.connection)

        if "PromoWear" in Environment.modulesList:
                # le varianti non si possono duplicare !!!
                articoloTagliaColore = dao.articoloTagliaColore
                if articoloTagliaColore is not None and articoloTagliaColore.id_articolo_padre is not None:
                    msg = "Attenzione !\n\n Le varianti non sono duplicabili !"
                    dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                            gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK, msg)
                    response = dialog.run()
                    dialog.destroy()
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
        self.editElement.dao.aggiornamento_listino_auto = dao.aggiornamento_listino_auto
        self.editElement.dao.timestamp_variazione = dao.timestamp_variazione
        self.editElement.dao.note = dao.note
        self.editElement.dao.cancellato = dao.cancellato
        self.editElement.dao.sospeso = dao.sospeso
        self.editElement.dao.id_stato_articolo = dao.id_stato_articolo
        self.editElement.dao.quantita_minima = dao.quantita_minima

        if self.editElement._codiceByFamiglia:
            self.editElement.dao.codice = getNuovoCodiceArticolo(Environment.connection, dao.id_famiglia_articolo)
        else:
            self.editElement.dao.codice = getNuovoCodiceArticolo(Environment.connection, None )

        self.editElement.setVisible(True)
        self.editElement._refresh()

        msg = 'Si desidera duplicare anche tutti i listini dell\' articolo scelto ?'
        dialog = gtk.MessageDialog(self.editElement.dialogTopLevel,
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION,
                                   gtk.BUTTONS_YES_NO, msg)

        response = dialog.run()
        dialog.destroy()
        if response != gtk.RESPONSE_YES:
            self.editElement._duplicatedDaoId = None



class AnagraficaArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli articoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_articoli_filter_table',
                                  gladeFile='promogest/modules/PromoWear/gui/_anagrafica_articoli_elements.glade',module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry


    def draw(self):
        treeview = self._anagrafica.anagrafica_filter_treeview

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Codice', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Produttore', renderer, text=4, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'produttore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice a barre', renderer, text=5, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice_a_barre')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', renderer, text=6, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice_articolo_fornitore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Famiglia', renderer, text=7, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione_famiglia')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Categoria', renderer, text=8, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione_categoria')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        if "PromoWear" in Environment.modulesList and self._anagrafica._taglia_colore:
            column = gtk.TreeViewColumn('Gruppo taglia', renderer, text=9, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'denominazione_gruppo_taglia')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Taglia', renderer, text=10, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'denominazione_taglia')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Colore', renderer, text=11, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'denominazione_colore')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Anno', renderer, text=12, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'anno')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Stagione', renderer, text=13, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'stagione')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Genere', renderer, text=14, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'genere')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)
            self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
            if not self._anagrafica._taglia_colore:
                self.gruppo_taglia_filter_label.set_no_show_all(True)
                self.gruppo_taglia_filter_label.set_property('visible', False)
                self.id_gruppo_taglia_articolo_filter_combobox.set_property('visible', False)
                self.id_gruppo_taglia_articolo_filter_combobox.set_no_show_all(True)
                self.taglia_filter_label.set_no_show_all(True)
                self.taglia_filter_label.set_property('visible', False)
                self.id_taglia_articolo_filter_combobox.set_property('visible', False)
                self.id_taglia_articolo_filter_combobox.set_no_show_all(True)
                self.colore_filter_label.set_no_show_all(True)
                self.colore_filter_label.set_property('visible', False)
                self.id_colore_articolo_filter_combobox.set_property('visible', False)
                self.id_colore_articolo_filter_combobox.set_no_show_all(True)
                self.anno_filter_label.set_no_show_all(True)
                self.anno_filter_label.set_property('visible', False)
                self.id_anno_articolo_filter_combobox.set_property('visible', False)
                self.id_anno_articolo_filter_combobox.set_no_show_all(True)
                self.stagione_filter_label.set_no_show_all(True)
                self.stagione_filter_label.set_property('visible', False)
                self.id_stagione_articolo_filter_combobox.set_property('visible', False)
                self.id_stagione_articolo_filter_combobox.set_no_show_all(True)
                self.genere_filter_label.set_no_show_all(True)
                self.genere_filter_label.set_property('visible', False)
                self.id_genere_articolo_filter_combobox.set_property('visible', False)
                self.id_genere_articolo_filter_combobox.set_no_show_all(True)
                self.taglie_colori_filter_label.set_no_show_all(True)
                self.taglie_colori_filter_label.set_property('visible', False)
                self.taglie_colori_filter_combobox.set_property('visible', False)
                self.taglie_colori_filter_combobox.set_no_show_all(True)
        else:
            self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str, str, str, str, str, str)

        treeview.set_search_column(2)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.filter_promowear.set_property('visible', Environment.conf.PromoWear)

        self.clear()


    def _refresh_filter_comboboxes(self, widget=None):
        self.refresh()


    def clear(self):
        # Annullamento filtro
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
        if "PromoWear" in Environment.modulesList:
            fillComboboxGruppiTaglia(self.id_gruppo_taglia_articolo_filter_combobox, True)
            fillComboboxTaglie(self.id_taglia_articolo_filter_combobox, True)
            fillComboboxColori(self.id_colore_articolo_filter_combobox, True)
            fillComboboxAnniAbbigliamento(self.id_anno_articolo_filter_combobox, True)
            fillComboboxStagioniAbbigliamento(self.id_stagione_articolo_filter_combobox, True)
            fillComboboxGeneriAbbigliamento(self.id_genere_articolo_filter_combobox, True)
            self.id_categoria_articolo_filter_combobox.set_active(0)
            self.id_gruppo_taglia_articolo_filter_combobox.set_active(0)
            self.id_taglia_articolo_filter_combobox.set_active(0)
            self.id_colore_articolo_filter_combobox.set_active(0)
            self.id_anno_articolo_filter_combobox.set_active(0)
            if hasattr(Environment.conf,'TaglieColori'):
                anno = getattr(Environment.conf.TaglieColori,'anno_default', None)
                if anno is not None:
                    findComboboxRowFromId(self.id_anno_articolo_filter_combobox, int(anno))
            self.id_stagione_articolo_filter_combobox.set_active(0)
            if hasattr(Environment.conf,'TaglieColori'):
                stagione = getattr(Environment.conf.TaglieColori,'stagione_default', None)
                if stagione is not None:
                    findComboboxRowFromId(self.id_stagione_articolo_filter_combobox, int(stagione))
            self.id_genere_articolo_filter_combobox.set_active(0)
            self.taglie_colori_filter_combobox.set_active(0)

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
            cancellato = None
        else:
            cancellato = False

        if "PromoWear" in Environment.modulesList and self._anagrafica._taglia_colore:
            padriTagliaColore = ((self.taglie_colori_filter_combobox.get_active() == 0) or
                                 (self.taglie_colori_filter_combobox.get_active() == 1))
            figliTagliaColore = ((self.taglie_colori_filter_combobox.get_active() == 0) or
                                 (self.taglie_colori_filter_combobox.get_active() == 2))
            idGruppoTaglia = findIdFromCombobox(self.id_gruppo_taglia_articolo_filter_combobox)
            idTaglia = findIdFromCombobox(self.id_taglia_articolo_filter_combobox)
            idColore = findIdFromCombobox(self.id_colore_articolo_filter_combobox)
            idAnno = findIdFromCombobox(self.id_anno_articolo_filter_combobox)
            idStagione = findIdFromCombobox(self.id_stagione_articolo_filter_combobox)
            idGenere = findIdFromCombobox(self.id_genere_articolo_filter_combobox)
        else: # Qua c'e' un errore, anche se promowear e' False ho lo stesso queste
                  # variabili. Ma siamo sicuri che non sia uno spreco di memoria?
            padriTagliaColore = None
            figliTagliaColore = None
            idGruppoTaglia = None
            idTaglia = None
            idColore = None
            idAnno = None
            idStagione = None
            idGenere = None

        def filterCountClosure():

            return ArticoloPromowear(isList=True).count( denominazione=denominazione,
                                            codice=codice,
                                            codiceABarre=codiceABarre,
                                            codiceArticoloFornitore=codiceArticoloFornitore,
                                            produttore=produttore,
                                            idFamiglia=idFamiglia,
                                            idCategoria=idCategoria,
                                            idStato=idStato,
                                            cancellato=cancellato,
                                            idGruppoTaglia=idGruppoTaglia,
                                            idTaglia=idTaglia,
                                            idColore=idColore,
                                            idAnno=idAnno,
                                            idStagione=idStagione,
                                            idGenere=idGenere,
                                            padriTagliaColore=padriTagliaColore,
                                            figliTagliaColore=figliTagliaColore)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return ArticoloPromowear(isList=True).select(orderBy=self.orderBy,
                                                denominazione=denominazione,
                                                codice=codice,
                                                codiceABarre=codiceABarre,
                                                codiceArticoloFornitore=codiceArticoloFornitore,
                                                produttore=produttore,
                                                idFamiglia=idFamiglia,
                                                idCategoria=idCategoria,
                                                idStato=idStato,
                                                cancellato=cancellato,
                                                idGruppoTaglia=idGruppoTaglia,
                                                idTaglia=idTaglia,
                                                idColore=idColore,
                                                idAnno=idAnno,
                                                idStagione=idStagione,
                                                idGenere=idGenere,
                                                padriTagliaColore=padriTagliaColore,
                                                figliTagliaColore=figliTagliaColore,
                                                offset=offset,
                                                batchSize=batchSize)

        self._filterClosure = filterClosure

        arts = self.runFilter()

        self._treeViewModel.clear()

        for a in arts:
            col = None
            if a.cancellato:
                col = 'red'
            self._treeViewModel.append((a,
                                    col,
                                    (a.codice or ''),
                                    (a.denominazione or ''),
                                    (a.produttore or ''),
                                    (a.codice_a_barre or ''),
                                    (a.codice_articolo_fornitore or ''),
                                    (a.denominazione_famiglia or ''),
                                    (a.denominazione_categoria or ''),
                                    (a.denominazione_gruppo_taglia or ''),
                                    (a.denominazione_taglia or ''),
                                    (a.denominazione_colore or ''),
                                    (a.anno or ''),
                                    (a.stagione or ''),
                                    (a.genere or '')))

    def on_taglie_colori_filter_combobox_changed(self, combobox):
        selected = self.taglie_colori_filter_combobox.get_active()
        if selected == 1:
            # solo principali
            self.id_taglia_articolo_filter_combo.set_active(0)
            self.id_taglia_articolo_filter_combo.set_sensitive(False)
            self.id_colore_articolo_filter_combobox.set_active(0)
            self.id_colore_articolo_filter_combobox.set_sensitive(False)
        else:
            self.id_taglia_articolo_filter_combo.set_sensitive(True)
            self.id_colore_articolo_filter_combobox.set_sensitive(True)

class AnagraficaArticoliHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'articolo',
                                'Dettaglio articolo')



class AnagraficaArticoliReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli articoli',
                                  defaultFileName='articoli',
                                  htmlTemplate='articoli',
                                  sxwTemplate='articoli')



class AnagraficaArticoliEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica degli articoli """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_articoli_detail_table',
                                'Dati articolo',
                                gladeFile='_anagrafica_articoli_elements.glade')
        self._widgetFirstFocus = self.codice_entry
        self._loading = False
        self._codiceByFamiglia = promogest.dao.Articolo.isNuovoCodiceByFamiglia()
        self._duplicatedDaoId = None
        if "PromoWear" in Environment.modulesList:
            self._articoloTagliaColore = None
        else:
            self.notebook1.remove_page(3)
            self.promowear_frame.destroy()

    def draw(self):
        if "PromoWear" in Environment.modulesList and not self._anagrafica._taglia_colore:
            self.senza_taglie_colori_radiobutton.set_active(True)
            self.codici_a_barre_label.set_text('')
            self.senza_taglie_colori_radiobutton.set_property('visible', False)
            self.senza_taglie_colori_radiobutton.set_no_show_all(True)
            self.codici_a_barre_hseparator.set_property('visible', False)
            self.codici_a_barre_hseparator.set_no_show_all(True)
            self.con_taglie_colori_radiobutton.set_property('visible', False)
            self.con_taglie_colori_radiobutton.set_no_show_all(True)
            self.taglie_colori_togglebutton.set_property('visible', False)
            self.taglie_colori_togglebutton.set_no_show_all(True)
            self.notebook1.remove_page(3)
        elif "PromoWear" in Environment.modulesList and self._anagrafica._taglia_colore:
            #Popola combobox gruppi taglia
            fillComboboxGruppiTaglia(self.id_gruppo_taglia_customcombobox.combobox)
            self.id_gruppo_taglia_customcombobox.connect('clicked',
                                                         on_id_gruppo_taglia_customcombobox_clicked)
            #Popola combobox taglie
            fillComboboxTaglie(self.id_taglia_customcombobox.combobox)
            self.id_taglia_customcombobox.connect('clicked',
                                                  self.on_id_taglia_customcombobox_clicked)
            #Popola combobox colori
            fillComboboxColori(self.id_colore_customcombobox.combobox)
            self.id_colore_customcombobox.connect('clicked',
                                                  self.on_id_colore_customcombobox_clicked)
            #Popola combobox anni
            fillComboboxAnniAbbigliamento(self.id_anno_combobox)
            #Popola combobox stagioni
            fillComboboxStagioniAbbigliamento(self.id_stagione_combobox)
            #Popola combobox generi
            fillComboboxGeneriAbbigliamento(self.id_genere_combobox)

        #Popola combobox aliquote iva
        fillComboboxAliquoteIva(self.id_aliquota_iva_customcombobox.combobox)
        self.id_aliquota_iva_customcombobox.connect('clicked',
                                                    on_id_aliquota_iva_customcombobox_clicked)
        #Popola combobox categorie articolo
        fillComboboxCategorieArticoli(self.id_categoria_articolo_customcombobox.combobox)
        self.id_categoria_articolo_customcombobox.connect('clicked',
                                                          on_id_categoria_articolo_customcombobox_clicked)
        #Popola combobox famiglie articolo
        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_customcombobox.combobox)
        self.id_famiglia_articolo_customcombobox.connect('clicked',
                                                         on_id_famiglia_articolo_customcombobox_clicked)
        if self._codiceByFamiglia:
            #Collega la creazione di un nuovo codice articolo al cambiamento della famiglia
            self.id_famiglia_articolo_customcombobox.combobox.connect('changed',
                                                                      self.on_id_famiglia_articolo_customcombobox_changed)
        #Popola combobox stati articolo
        fillComboboxStatiArticoli(self.id_stato_articolo_combobox)
        #Popola combobox imballaggi
        fillComboboxImballaggi(self.id_imballaggio_customcombobox.combobox)
        self.id_imballaggio_customcombobox.connect('clicked',
                                                   on_id_imballaggio_customcombobox_clicked)
        #Popola combobox unita base
        fillComboboxUnitaBase(self.id_unita_base_combobox)
        #Popola comboboxentry unita dimensioni
        fillComboboxUnitaFisica(self.unita_dimensioni_comboboxentry,
                                'dimensioni')
        #Popola comboboxentry unita volume
        fillComboboxUnitaFisica(self.unita_volume_comboboxentry,
                                'volume')
        #Popola comboboxentry unita peso
        fillComboboxUnitaFisica(self.unita_peso_comboboxentry,
                                'peso')


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Articolo(Environment.connection)
            # Assegna il codice se ne e' prevista la crazione automatica, ma non per famiglia
            if not self._codiceByFamiglia:
                self.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(Environment.connection, None)
            # Prova a impostare "pezzi" come unita' di misura base
            self.dao.id_unita_base = 1
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Articolo(Environment.connection, dao.id)
        self._refresh()


    def _refresh(self):
        self._loading = True
        self.codice_entry.set_text(self.dao.codice or '')
        self.dao.codice = omogeneousCode(section="Articoli", string=self.dao.codice )
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        findComboboxRowFromId(self.id_aliquota_iva_customcombobox.combobox,
                              self.dao.id_aliquota_iva)
        findComboboxRowFromId(self.id_famiglia_articolo_customcombobox.combobox,
                              self.dao.id_famiglia_articolo)
        findComboboxRowFromId(self.id_categoria_articolo_customcombobox.combobox, self.dao.id_categoria_articolo)
        findComboboxRowFromId(self.id_unita_base_combobox,
                              self.dao.id_unita_base)
        findComboboxRowFromId(self.id_stato_articolo_combobox,
                              self.dao.id_stato_articolo)
        findComboboxRowFromId(self.id_imballaggio_customcombobox.combobox,
                              self.dao.id_imballaggio)
        self.produttore_entry.set_text(self.dao.produttore or '')
        self.unita_dimensioni_comboboxentry.child.set_text(self.dao.unita_dimensioni or '')
        self.unita_volume_comboboxentry.child.set_text(self.dao.unita_volume
                                                       or '')
        self.unita_peso_comboboxentry.child.set_text(self.dao.unita_peso or '')
        self.lunghezza_entry.set_text('%-6.3f' % float(self.dao.lunghezza or 0))
        self.larghezza_entry.set_text('%-6.3f' % float(self.dao.larghezza or 0))
        self.altezza_entry.set_text('%-6.3f' % float(self.dao.altezza or 0))
        self.volume_entry.set_text('%-6.3f' % float(self.dao.volume or 0))
        self.peso_lordo_entry.set_text('%-6.3f' % float(self.dao.peso_lordo or 0))
        self.peso_imballaggio_entry.set_text('%-6.3f' % float(self.dao.peso_imballaggio or 0))
        self.stampa_etichetta_checkbutton.set_active(self.dao.stampa_etichetta or True)
        self.codice_etichetta_entry.set_text(self.dao.codice_etichetta or '')
        self.descrizione_etichetta_entry.set_text(self.dao.descrizione_etichetta or '')
        self.stampa_listino_checkbutton.set_active(self.dao.stampa_listino or True)
        self.descrizione_listino_entry.set_text(self.dao.descrizione_listino or '')
        self.quantita_minima_entry.set_text(str(self.dao.quantita_minima or 0))
        if self.quantita_minima_entry.get_text() == '0':
            self.quantita_minima_entry.set_text('')
        textBuffer = self.note_textview.get_buffer()
        if self.dao.note is not None:
            textBuffer.set_text(self.dao.note)
        else:
            textBuffer.set_text('')
        self.note_textview.set_buffer(textBuffer)
        self.sospeso_checkbutton.set_active(self.dao.sospeso or False)
        self._loading = False
        if if "PromoWear" in Environment.modulesList and self._anagrafica._taglia_colore:
            self.id_aliquota_iva_customcombobox.set_sensitive(True)
            self.id_famiglia_articolo_customcombobox.set_sensitive(True)
            self.id_categoria_articolo_customcombobox.set_sensitive(True)
            self.id_unita_base_combobox.set_sensitive(True)
            self.produttore_entry.set_sensitive(True)

            # Aggiorna con/senza taglie e colori
            self.senza_taglie_colori_radiobutton.set_active(False)
            self.con_taglie_colori_radiobutton.set_active(True)
            self.senza_taglie_colori_radiobutton.set_sensitive(True)
            self.con_taglie_colori_radiobutton.set_sensitive(True)
            self._articoloTagliaColore = self.dao.articoloTagliaColoreCompleto
            if self._articoloTagliaColore is not None:
                if self._articoloTagliaColore.id_articolo_padre is not None:
                # variante: niente gestione taglie, ma possibilita' di trattare i codici a barre
                    self.senza_taglie_colori_radiobutton.set_active(True)
                    self.con_taglie_colori_radiobutton.set_active(False)
                    self.senza_taglie_colori_radiobutton.set_sensitive(True)
                    self.con_taglie_colori_radiobutton.set_sensitive(False)

                    # niente possibilita' di variare gruppo taglie, genere, anno e stagione
                    findComboboxRowFromId(self.id_gruppo_taglia_customcombobox.combobox, self._articoloTagliaColore.id_gruppo_taglia)
                    self.id_gruppo_taglia_customcombobox.set_property('visible', False)
                    self.denominazione_gruppo_taglia_label.set_markup(
                            '<span weight="bold">%s</span>'
                            % (self._articoloTagliaColore.denominazione_gruppo_taglia,))
                    self.denominazione_gruppo_taglia_label.set_property('visible', True)
                    findComboboxRowFromId(self.id_genere_combobox, self._articoloTagliaColore.id_genere)
                    self.id_genere_combobox.set_property('visible', False)
                    self.denominazione_genere_label.set_markup(
                            '<span weight="bold">%s</span>'
                            % (self._articoloTagliaColore.genere,))
                    self.denominazione_genere_label.set_property('visible', True)
                    findComboboxRowFromId(self.id_stagione_combobox, self._articoloTagliaColore.id_stagione)
                    self.id_stagione_combobox.set_property('visible', False)
                    findComboboxRowFromId(self.id_anno_combobox, self._articoloTagliaColore.id_anno)
                    self.id_anno_combobox.set_property('visible', False)
                    self.denominazione_stagione_anno_label.set_markup(
                            '<span weight="bold">%s - %s</span>'
                            % (self._articoloTagliaColore.stagione,
                                self._articoloTagliaColore.anno))
                    self.denominazione_stagione_anno_label.set_property('visible', True)

                    # possibilita' di variare taglia e colore
                    articoliTagliaColore = self._articoloTagliaColore.articoloPadre().articoliTagliaColore
                    idTaglie = set(a.id_taglia for a in articoliTagliaColore)
                    idTaglie.remove(self._articoloTagliaColore.id_taglia)
                    fillComboboxTaglie(self.id_taglia_customcombobox.combobox,
                        idGruppoTaglia=self._articoloTagliaColore.id_gruppo_taglia,
                        ignore=list(idTaglie))
                    findComboboxRowFromId(self.id_taglia_customcombobox.combobox,
                        self._articoloTagliaColore.id_taglia)
                    self.id_taglia_customcombobox.set_property('visible', True)
                    self.denominazione_taglia_label.set_markup('-')
                    self.denominazione_taglia_label.set_property('visible', False)
                    idColori = set(a.id_colore for a in articoliTagliaColore)
                    idColori.remove(self._articoloTagliaColore.id_colore)
                    fillComboboxColori(self.id_colore_customcombobox.combobox, ignore=list(idColori))
                    findComboboxRowFromId(self.id_colore_customcombobox.combobox, self._articoloTagliaColore.id_colore)
                    self.id_colore_customcombobox.set_property('visible', True)
                    self.denominazione_colore_label.set_markup('-')
                    self.denominazione_colore_label.set_property('visible', False)

                    self.id_aliquota_iva_customcombobox.set_sensitive(False)
                    self.id_famiglia_articolo_customcombobox.set_sensitive(False)
                    self.id_categoria_articolo_customcombobox.set_sensitive(False)
                    self.id_unita_base_combobox.set_sensitive(False)
                    self.produttore_entry.set_sensitive(False)
                else:
                    # articolo principale: gestione codici a barre - taglie - colori
                    self.senza_taglie_colori_radiobutton.set_active(False)
                    self.con_taglie_colori_radiobutton.set_active(True)

                    # niente variazione gruppo taglia
                    # possibilita' di variare anno, stagione e genere
                    findComboboxRowFromId(self.id_gruppo_taglia_customcombobox.combobox, self._articoloTagliaColore.id_gruppo_taglia)
                    self.id_gruppo_taglia_customcombobox.set_property('visible', False)
                    self.denominazione_gruppo_taglia_label.set_markup('<span weight="bold">%s</span>'
                                                                        % (self._articoloTagliaColore.denominazione_gruppo_taglia,))
                    findComboboxRowFromId(self.id_genere_combobox, self._articoloTagliaColore.id_genere)
                    self.id_genere_combobox.set_property('visible', True)
                    self.denominazione_genere_label.set_markup('-')
                    self.denominazione_genere_label.set_property('visible', False)
                    findComboboxRowFromId(self.id_stagione_combobox, self._articoloTagliaColore.id_stagione)
                    self.id_stagione_combobox.set_property('visible', True)
                    findComboboxRowFromId(self.id_anno_combobox, self._articoloTagliaColore.id_anno)
                    self.denominazione_stagione_anno_label.set_markup('-')
                    self.denominazione_stagione_anno_label.set_property('visible', False)

                    # niente variazione taglia, colore
                    self.id_taglia_customcombobox.combobox.set_active(-1)
                    self.id_taglia_customcombobox.set_property('visible', False)
                    self.denominazione_taglia_label.set_markup('<span weight="bold">-</span>')
                    self.denominazione_taglia_label.set_property('visible', True)
                    self.id_colore_customcombobox.combobox.set_active(-1)
                    self.id_colore_customcombobox.set_property('visible', False)
                    self.denominazione_colore_label.set_markup('<span weight="bold">-</span>')
                    self.denominazione_colore_label.set_property('visible', True)
            elif "PromoWear" in Environment.modulesList:
                # possibile articolo principale
                # possibilita' di inserire gruppo taglia, genere, anno, stagione
                if self.dao.id is None:
                    self.senza_taglie_colori_radiobutton.set_active(False)
                    self.con_taglie_colori_radiobutton.set_active(True)
                else:
                    self.senza_taglie_colori_radiobutton.set_active(True)
                    self.con_taglie_colori_radiobutton.set_active(False)
                self.senza_taglie_colori_radiobutton.set_sensitive(True)
                self.con_taglie_colori_radiobutton.set_sensitive(True)

                self.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
                self.id_gruppo_taglia_customcombobox.set_property('visible', True)
                self.denominazione_gruppo_taglia_label.set_markup('-')
                self.denominazione_gruppo_taglia_label.set_property('visible', False)
                self.id_genere_combobox.set_active(-1)
                self.id_genere_combobox.set_property('visible', True)
                self.denominazione_genere_label.set_markup('-')
                self.denominazione_genere_label.set_property('visible', False)
                self.id_stagione_combobox.set_active(-1)
                self.id_stagione_combobox.set_property('visible', True)
                self.id_anno_combobox.set_active(-1)
                self.id_anno_combobox.set_property('visible', True)
                self.denominazione_stagione_anno_label.set_markup('-')
                self.denominazione_stagione_anno_label.set_property('visible', False)
                if self.dao.id is None:
                    # Prova a impostare l'anno di default
                    self.id_anno_combobox.set_active(0)
                    if hasattr(Environment.conf,'TaglieColori'):
                        anno = getattr(Environment.conf.TaglieColori,'anno_default', None)
                        if anno is not None:
                            findComboboxRowFromId(self.id_anno_combobox, int(anno))
                    # Prova a impostare la stagione di default
                    self.id_stagione_combobox.set_active(0)
                    if hasattr(Environment.conf,'TaglieColori'):
                        stagione = getattr(Environment.conf.TaglieColori,'stagione_default', None)
                        if stagione is not None:
                            findComboboxRowFromId(self.id_stagione_combobox, int(stagione))

                # niente possibilita' di inserire taglia, colore
                self.id_taglia_customcombobox.combobox.set_active(-1)
                self.id_taglia_customcombobox.set_property('visible', False)
                self.denominazione_taglia_label.set_markup('<span weight="bold">-</span>')
                self.denominazione_taglia_label.set_property('visible', True)
                self.id_colore_customcombobox.combobox.set_active(-1)
                self.id_colore_customcombobox.set_property('visible', False)
                self.denominazione_colore_label.set_markup('<span weight="bold">-</span>')
                self.denominazione_colore_label.set_property('visible', True)


    def saveDao(self):
        if (self.codice_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.codice_entry,
                            msg='Campo obbligatorio !\nCodice')

        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.denominazione_entry,
                            msg='Campo obbligatorio !\nDenominazione')

        if findIdFromCombobox(self.id_aliquota_iva_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_aliquota_iva_customcombobox.combobox,
                            msg='Campo obbligatorio !\nAliquota IVA')

        if findIdFromCombobox(self.id_famiglia_articolo_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_famiglia_articolo_customcombobox.combobox,
                            msg='Campo obbligatorio !\nFamiglia merceologica')

        if findIdFromCombobox(self.id_categoria_articolo_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_categoria_articolo_customcombobox.combobox,
                            msg='Campo obbligatorio !\nCategoria articolo')

        if findIdFromCombobox(self.id_unita_base_combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_unita_base_combobox,
                            msg='Campo obbligatorio !\nUnita\' base')
        if "PromoWear" in Environment.modulesList:
            idGruppoTaglia = findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox)
            idAnno = findIdFromCombobox(self.id_anno_combobox)
            idStagione = findIdFromCombobox(self.id_stagione_combobox)
            idGenere = findIdFromCombobox(self.id_genere_combobox)
            if idGruppoTaglia is not None or idAnno is not None or idStagione is not None or idGenere is not None:
                isArticoloTagliaColore = True
                if findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox) is None:
                    obligatoryField(self.dialogTopLevel,
                                    self.id_gruppo_taglia_customcombobox.combobox,
                                    msg='Campo obbligatorio !\nGruppo taglia')

                if findIdFromCombobox(self.id_anno_combobox) is None:
                    obligatoryField(self.dialogTopLevel,
                                    self.id_anno_combobox,
                                    msg='Campo obbligatorio !\nAnno')

                if findIdFromCombobox(self.id_stagione_combobox) is None:
                    obligatoryField(self.dialogTopLevel,
                                    self.id_stagione_combobox,
                                    msg='Campo obbligatorio !\nStagione')

                if findIdFromCombobox(self.id_genere_combobox) is None:
                    obligatoryField(self.dialogTopLevel,
                                    self.id_genere_combobox,
                                    msg='Campo obbligatorio !\nGenere')

                if self._articoloTagliaColore is not None:
                    if self._articoloTagliaColore.id_articolo_padre is not None:
                        if findIdFromCombobox(self.id_taglia_customcombobox.combobox) is None:
                            obligatoryField(self.dialogTopLevel,
                                            self.id_taglia_customcombobox.combobox,
                                            msg='Campo obbligatorio !\nTaglia')

                        if findIdFromCombobox(self.id_colore_customcombobox.combobox) is None:
                            obligatoryField(self.dialogTopLevel,
                                            self.id_colore_customcombobox.combobox,
                                            msg='Campo obbligatorio !\nColore')
            else:
                isArticoloTagliaColore = False
            if isArticoloTagliaColore:
                if self._articoloTagliaColore is not None:
                    articoloTagliaColore = ArticoloTagliaColore(Environment.connection, self.dao.id)
                else:
                    articoloTagliaColore = ArticoloTagliaColore(Environment.connection)
                    articoloTagliaColore.id_articolo = self.dao.id

                articoloTagliaColore.id_gruppo_taglia = findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox)
                articoloTagliaColore.id_taglia = findIdFromCombobox(self.id_taglia_customcombobox.combobox)
                articoloTagliaColore.id_colore = findIdFromCombobox(self.id_colore_customcombobox.combobox)
                articoloTagliaColore.id_anno = findIdFromCombobox(self.id_anno_combobox)
                articoloTagliaColore.id_stagione = findIdFromCombobox(self.id_stagione_combobox)
                articoloTagliaColore.id_genere = findIdFromCombobox(self.id_genere_combobox)
                self.dao.articoloTagliaColore = articoloTagliaColore
            else:
                self.dao.articoloTagliaColore = None

        self.dao.codice = self.codice_entry.get_text()
        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.id_aliquota_iva = findIdFromCombobox(self.id_aliquota_iva_customcombobox.combobox)
        self.dao.id_famiglia_articolo = findIdFromCombobox(self.id_famiglia_articolo_customcombobox.combobox)
        self.dao.id_categoria_articolo = findIdFromCombobox(self.id_categoria_articolo_customcombobox.combobox)
        self.dao.id_unita_base = findIdFromCombobox(self.id_unita_base_combobox)
        self.dao.id_stato_articolo = findIdFromCombobox(self.id_stato_articolo_combobox)
        self.dao.id_imballaggio = findIdFromCombobox(self.id_imballaggio_customcombobox.combobox)
        self.dao.produttore = self.produttore_entry.get_text()
        self.dao.unita_dimensioni = self.unita_dimensioni_comboboxentry.child.get_text()
        self.dao.unita_volume = self.unita_volume_comboboxentry.child.get_text()
        self.dao.unita_peso = self.unita_peso_comboboxentry.child.get_text()
        self.dao.lunghezza = float(self.lunghezza_entry.get_text())
        self.dao.larghezza = float(self.larghezza_entry.get_text())
        self.dao.altezza = float(self.altezza_entry.get_text())
        self.dao.volume = float(self.volume_entry.get_text())
        self.dao.peso_lordo = float(self.peso_lordo_entry.get_text())
        self.dao.peso_imballaggio = float(self.peso_imballaggio_entry.get_text())
        self.dao.stampa_etichetta = self.stampa_etichetta_checkbutton.get_active()
        self.dao.codice_etichetta = self.codice_etichetta_entry.get_text()
        self.dao.descrizione_etichetta = self.descrizione_etichetta_entry.get_text()
        self.dao.stampa_listino = self.stampa_listino_checkbutton.get_active()
        self.dao.descrizione_listino = self.descrizione_listino_entry.get_text()
        self.dao.quantita_minima = float(self.quantita_minima_entry.get_text() or 0)
        textBuffer = self.note_textview.get_buffer()
        self.dao.note = textBuffer.get_text(textBuffer.get_start_iter(),
                                            textBuffer.get_end_iter())
        self.dao.sospeso = self.sospeso_checkbutton.get_active()
        if self.dao.cancellato == None:
            self.dao.cancellato = False
        if self.dao.aggiornamento_listino_auto == None:
            self.dao.aggiornamento_listino_auto = False

        self.dao.persist()

        if self._duplicatedDaoId is not None:
            self.duplicaListini()

        if "PromoWear" in Environment.modulesList:
            self._articoloTagliaColore = self.dao.articoloTagliaColoreCompleto


    def on_codici_a_barre_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i codici a barre occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaCodiciABarreArticoli import AnagraficaCodiciABarreArticoli
        anag = AnagraficaCodiciABarreArticoli(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)


    def on_multipli_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i multipli occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaMultipli import AnagraficaMultipli
        anag = AnagraficaMultipli(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)


    def on_stoccaggi_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i dati di stoccaggio occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaStoccaggi import AnagraficaStoccaggi
        anag = AnagraficaStoccaggi(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)


    def on_forniture_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = ('Prima di poter inserire le forniture occorre '
                   + 'salvare l\' articolo.\n Salvare ?')
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)


    def on_listini_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i listini occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)


    def duplicaListini(self):
        """ Duplica i listini relativi ad un articolo scelto su un nuovo articolo """
        if self._duplicatedDaoId is None:
            return

        from promogest.dao import ListinoArticolo
        listini = ListinoArticolo.select(Environment.connection, idArticolo = self._duplicatedDaoId, immediate = True)
        for listino in listini:
            daoLA = ListinoArticolo.ListinoArticolo(Environment.connection)
            daoLA.id_listino = listino.id_listino
            daoLA.id_articolo = self.dao.id
            daoLA.prezzo_dettaglio = listino.prezzo_dettaglio
            daoLA.prezzo_ingrosso = listino.prezzo_ingrosso
            daoLA.ultimo_costo = listino.ultimo_costo
            daoLA.data_listino_articolo = listino.data_listino_articolo
            daoLA.persist()

        self._duplicatedDaoId = None


    def on_id_famiglia_articolo_customcombobox_changed(self, combobox):
        """ Restituisce un nuovo codice articolo al cambiamento della famiglia """

        if self._loading:
            return

        if not self._codiceByFamiglia:
            return

        idFamiglia = findIdFromCombobox(self.id_famiglia_articolo_customcombobox.combobox)
        if idFamiglia is not None:
            self.dao.codice = getNuovoCodiceArticolo(Environment.connection, idFamiglia)
            self.codice_entry.set_text(self.dao.codice)

    def on_senza_taglie_colori_radiobutton_toggled(self, radioButton):
        active = radioButton.get_active()
        self.codici_a_barre_togglebutton.set_sensitive(active)
        self.taglie_colori_togglebutton.set_sensitive(not active)
        if active and self._articoloTagliaColore is None:
            self.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
            self.id_genere_combobox.set_active(-1)
            self.id_stagione_combobox.set_active(-1)
            self.id_anno_combobox.set_active(-1)


    def on_taglie_colori_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox) is None:
            toggleButton.set_active(False)
            obligatoryField(self.dialogTopLevel, self.id_gruppo_taglia_customcombobox.combobox, 'Specificare il gruppo taglia !')

        if self.dao.id is None or self._articoloTagliaColore is None:
            msg = 'Prima di poter inserire taglie, colori e codici a barre occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                try:
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                except:
                    toggleButton.set_active(False)
                    return
            else:
                toggleButton.set_active(False)
                return

        from promogest.modules.PromoWear.ui.TaglieColori import GestioneTaglieColori
        tagcol = GestioneTaglieColori(articolo=self.dao)
        tagcolWindow = tagcol.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, tagcolWindow, toggleButton)


    def on_id_taglia_customcombobox_clicked(self, widget, button):
        articoliTagliaColore = self._articoloTagliaColore.articoloPadre().articoliTagliaColore
        idTaglie = set(a.id_taglia for a in articoliTagliaColore)
        idTaglie.remove(self._articoloTagliaColore.id_taglia)
        on_id_taglia_customcombobox_clicked(widget,
                                            button,
                                            idGruppoTaglia=self._articoloTagliaColore.id_gruppo_taglia,
                                            ignore=list(idTaglie))


    def on_id_colore_customcombobox_clicked(self, widget, button):
        articoliTagliaColore = self._articoloTagliaColore.articoloPadre().articoliTagliaColore
        idColori = set(a.id_colore for a in articoliTagliaColore)
        idColori.remove(self._articoloTagliaColore.id_colore)
        on_id_colore_customcombobox_clicked(widget,
                                            button,
                                            ignore=list(idColori))
