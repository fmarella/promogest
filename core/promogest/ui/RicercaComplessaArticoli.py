# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Andrea Argiolas <andrea@promotux.it>
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

import gtk
import gobject
from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.lib.sqlalchemy import and_, or_
from RicercaComplessa import RicercaComplessa
from RicercaComplessa import analyze_treeview_key_press_event
from RicercaComplessa import parseModel, onColumnEdited, columnSelectAll
from RicercaComplessa import optimizeString, insertTreeViewRow, deleteTreeViewRow, clearWhereString

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo
import promogest.dao.FamigliaArticolo
from promogest.dao.FamigliaArticolo import FamigliaArticolo
import promogest.dao.CategoriaArticolo
from promogest.dao.CategoriaArticolo import CategoriaArticolo
import promogest.dao.StatoArticolo
from promogest.dao.StatoArticolo import StatoArticolo
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
if "PromoWear" in Environment.modulesList:
    from promogest.modules.PromoWear.dao.Colore import Colore
    from promogest.modules.PromoWear.dao.Taglia import Taglia
    from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
    from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
    from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
    from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento
    from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia


from promogest.ui.GladeWidget import GladeWidget
import Login
from utils import *
from utilsCombobox import *



class RicercaComplessaArticoli(RicercaComplessa):
    """ Ricerca avanzata articoli """

    def __init__(self, denominazione = None, codice = None, codiceABarre = None,
                  codiceArticoloFornitore = None, produttore = None,
                  idFamiglia = None, idCategoria = None, idStato = None, cancellato = None,
                  idGruppoTaglia = None, idTaglia = None, idColore = None,
                  idAnno = None, idStagione = None, idGenere = None):

        self._denominazione = denominazione
        self._codice = codice
        self._codiceABarre = codiceABarre
        self._codiceArticoloFornitore = codiceArticoloFornitore
        self._produttore = produttore
        self._idFamiglia = idFamiglia
        self._idCategoria = idCategoria
        self._idStato = idStato
        self._cancellato = cancellato
        self._idGruppoTaglia = idGruppoTaglia
        self._idTaglia = idTaglia
        self._idColore = idColore
        self._idAnno = idAnno
        self._idStagione = idStagione
        self._idGenere = idGenere
        if "PromoWear" in Environment.modulesList:
            self._taglia_colore = Environment.taglia_colore or False

        self._ricerca = RicercaArticoliFilter(parentObject=self,
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
                                              idTaglia = idTaglia,
                                              idColore = idColore,
                                              idAnno = idAnno,
                                              idStagione = idStagione,
                                              idGenere = idGenere)
        RicercaComplessa.__init__(self, 'Promogest - Ricerca articoli',
                                  self._ricerca)

        self.ricerca_hpaned = gtk.HPaned()
        self.ricerca_viewport.add(self.ricerca_hpaned)

        # set filter part on the left
        filterElement = self.filter.filter_frame
        filterElement.unparent()
        self.ricerca_hpaned.pack1(filterElement, resize=False, shrink=False)

        # set treeview on the right
        resultElement = self.filter.filter_list_vbox
        resultElement.unparent()
        self.results_vbox = gtk.VBox()
        self.results_vbox.pack_start(resultElement)
        self.ricerca_hpaned.pack2(self.results_vbox, resize=True, shrink=False)

        self.ricerca_hpaned.set_position(360)

        # no detail part below treeview
        self.detail = None
        self.detailTopLevel = None

        # single selection for simple search, no selection for advanced search
        self._fixedSelectionTreeViewType = False

        self.filter.filter_clear_button.connect('clicked', self.on_filter_clear_button_clicked)
        self.filter.filter_search_button.connect('clicked', self.on_filter_search_button_clicked)

        #accelGroup = gtk.AccelGroup()
        #self.getTopLevel().add_accel_group(accelGroup)
        #self.filter.filter_clear_button.add_accelerator('clicked', accelGroup, gtk.keysyms.Escape, 0, gtk.ACCEL_VISIBLE)
        #self.filter.filter_search_button.add_accelerator('clicked', accelGroup, gtk.keysyms.F3, 0, gtk.ACCEL_VISIBLE)

        self.draw()

        self.setInitialSearch()


    def draw(self):
        """ Disegna la treeview relativa al risultato del filtraggio """
        treeview = self.filter.resultsElement
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Codice', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'codice')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Produttore', renderer, text=4, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'produttore')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice a barre', renderer, text=5, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'codice_a_barre')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', renderer, text=6, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'codice_articolo_fornitore')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Famiglia', renderer, text=7, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'denominazione_famiglia')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Categoria', renderer, text=8, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'denominazione_categoria')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)
        if "PromoWear" in Environment.modulesList and self._taglia_colore:
            column = gtk.TreeViewColumn('Gruppo taglia', renderer, text=9, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self.filter._changeOrderBy, 'denominazione_gruppo_taglia')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Taglia', renderer, text=10, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self.filter._changeOrderBy, 'denominazione_taglia')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Colore', renderer, text=11, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self.filter._changeOrderBy, 'denominazione_colore')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Anno', renderer, text=12, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self.filter._changeOrderBy, 'anno')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Stagione', renderer, text=13, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self.filter._changeOrderBy, 'stagione')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Genere', renderer, text=14, background=1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self.filter._changeOrderBy, 'genere')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)
            model = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
        else:
            model = gtk.ListStore(object, str, str, str, str, str, str, str, str)

        treeview.set_search_column(1)
        treeview.set_model(model)


    def setInitialSearch(self):
        """ Imposta il tipo di ricerca iniziale """
        # puo' essere ridefinito dalle classi derivate
        self._ricerca.setRicercaSemplice()


    def clear(self):
        """ Re-inizializza i filtri """
        self._ricerca.clear()


    def refresh(self):
        """ Esegue il filtraggio in base ai filtri impostati e aggiorna la treeview """
        self._ricerca.refresh()


    def on_filter_clear_button_clicked(self, button):
        """ Gestisce la pressione del bottone pulisci """
        pass


    def on_filter_search_button_clicked(self, button):
        """ Gestisce la pressione del bottone trova """
        pass


    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza

        from AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli()
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, self.refresh)

        anag.on_record_new_activate(anag.record_new_button)


    def on_filter_treeview_cursor_changed(self, treeview):
        """ Rileva la riga attualmente selezionata """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        if iterator is None:
            return

        self.dao = model.get_value(iterator, 0)
        self.refreshDetail()


    def refreshDetail(self):
        """ Aggiornamento della parte di dettaglio """
        # puo' essere ridefinito dalle classi derivate che
        # prevedono un parte di dettaglio
        pass


    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ La finestra viene nascosta perche' una riga e' stata selezionata """
        if self.getTopLevel() in Login.windowGroup:
            Login.windowGroup.remove(self.getTopLevel())
        self.getTopLevel().hide()


    def _changeTreeViewSelectionType(self):
        """ Imposta il tipo di selezione di default che si puo' fare sulla treeview """
        if self._fixedSelectionTreeViewType:
            return
        selection = self.filter.resultsElement.get_selection()
        if self._ricerca._tipoRicerca == 'semplice':
            # solo se la ricerca e' semplice si puo' selezionare una riga
            selection.set_mode(gtk.SELECTION_SINGLE)
        else:
            selection.set_mode(gtk.SELECTION_NONE)


    def setTreeViewSelectionType(self, mode=None):
        self._fixedSelectionTreeViewType = True
        if mode is not None:
            if mode in (gtk.SELECTION_SINGLE, gtk.SELECTION_MULTIPLE, gtk.SELECTION_NONE):
                selection = self.filter.resultsElement.get_selection()
                selection.set_mode(mode)


    def getResultsElement(self):
        """ Restituisce il risultato della ricerca se composto da un solo elemento """
        if self._ricerca._tipoRicerca == 'semplice':
            print "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"
            return self.dao
        else:
            selection = self.filter.resultsElement.get_selection()
            selectionMode = selection.get_mode()
            if selectionMode == gtk.SELECTION_SINGLE:
                print "QUIIIIIIIIIIIIIIIIIIIIIIIIIIOOOOOOOOOOOOOOOOOO"
                return self.dao
            elif self._ricerca.resultsCount == 1:
                print "O QUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
                treeview = self.filter.resultsElement
                model = treeview.get_model()
                self.dao = model[0][0]
                return self.dao
            else:
                return self._ricerca.getArtsResult()


    def getResultsCount(self):
        """ Restituisce il numero di clienti selezionati """
        if self._ricerca._tipoRicerca == 'semplice':
            if self.dao is not None:
                return 1
            else:
                return 0
        else:
            selection = self.filter.resultsElement.get_selection()
            selectionMode = selection.get_mode()
            if (selectionMode == gtk.SELECTION_SINGLE):
                if self.dao is not None:
                    return 1
                else:
                    return 0
            else:
                return self._ricerca.resultsCount


    def setSummaryTextBefore(self, value):
        self._ricerca.textBefore = value
        self._ricerca.setRiepilogoArticolo()


    def setSummaryTextAfter(self, value):
        self._ricerca.textAfter = value
        self._ricerca.setRiepilogoArticolo()



class RicercaArticoliFilter(GladeWidget):
    """ Classe che gestisce la tipologia di ricerca articoli """

    def __init__(self, parentObject,
                            denominazione = None,
                            codice = None,
                            codiceABarre = None,
                            codiceArticoloFornitore = None,
                            produttore = None,
                            idFamiglia = None,
                            idCategoria = None,
                            idStato = None,
                            cancellato = None,
                            idGruppoTaglia = None,
                            idTaglia = None,
                            idColore = None,
                            idAnno = None,
                            idStagione = None,
                            idGenere = None):

        GladeWidget.__init__(self, 'anagrafica_articoli_filter_vbox',
                            fileName='_anagrafica_articoli_elements.glade')

        self._denominazione = denominazione
        self._codice = codice
        self._codiceABarre = codiceABarre
        self._codiceArticoloFornitore = codiceArticoloFornitore
        self._produttore = produttore
        self._idFamiglia = idFamiglia
        self._idCategoria = idCategoria
        self._idStato = idStato
        self._cancellato = cancellato
        self._idGruppoTaglia = idGruppoTaglia
        self._idTaglia = idTaglia
        self._idColore = idColore
        self._idAnno = idAnno
        self._idStagione = idStagione
        self._idGenere = idGenere
        if "PromoWear" in Environment.modulesList:
            self._taglia_colore = Environment.taglia_colore or False
        self._parentObject = parentObject
        self.resultsCount = 0
        self.complexFilter=None
        self.textBefore = None
        self.textAfter = None
        self.res = None
        self.draw()

        self.ricerca_avanzata_articoli_button.connect('clicked',
                                                      self.on_ricerca_avanzata_articoli_button_clicked)
        self.ricerca_semplice_articoli_button.connect('clicked',
                                                      self.on_ricerca_semplice_articoli_button_clicked)


    def on_ricerca_avanzata_articoli_button_clicked(self, button):
        """ Seleziona la ricerca avanzata """
        self.setRicercaAvanzata()


    def on_ricerca_semplice_articoli_button_clicked(self, button):
        """ Seleziona la ricerca semplice """
        self.setRicercaSemplice()


    def setRicercaSemplice(self):
        """ Gestisce la visualizzazione della sola parte semplice della ricerca """
        self._tipoRicerca = 'semplice'
        self.ricerca_avanzata_articoli_filter_vbox.set_no_show_all(True)
        self.ricerca_avanzata_articoli_filter_vbox.hide()
        self.ricerca_semplice_articoli_filter_vbox.show()
        self.denominazione_filter_entry.grab_focus()
        self._parentObject._changeTreeViewSelectionType()
        self._parentObject.refresh()


    def setRicercaAvanzata(self):
        """ Gestisce la visualizzazione della sola parte avanzata della ricerca """
        self._tipoRicerca = 'avanzata'
        self.ricerca_semplice_articoli_filter_vbox.set_no_show_all(True)
        self.ricerca_semplice_articoli_filter_vbox.hide()
        self.ricerca_avanzata_articoli_filter_vbox.show()
        self.descrizione_articolo_filter_expander.grab_focus()
        self._parentObject._changeTreeViewSelectionType()
        self._parentObject.refresh()



    def draw(self):
        """ Disegna e imposta i widgets relativi a tutta la ricerca """
        self.drawRicercaSemplice()
        self.drawRicercaComplessa()


    def drawRicercaSemplice(self):
        """ Disegna e imposta i widgets relativi alla sola parte semplice della ricerca """
        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_filter_combobox, filter=True)
        fillComboboxCategorieArticoli(self.id_categoria_articolo_filter_combobox, True)
        fillComboboxStatiArticoli(self.id_stato_articolo_filter_combobox, True)
        if "PromoWear" in Environment.modulesList:
            from promogest.modules.PromoWear.ui.PromowearUtils import fillComboboxGruppiTaglia, fillComboboxTaglie, fillComboboxColori, fillComboboxAnniAbbigliamento, fillComboboxStagioniAbbigliamento, fillComboboxGeneriAbbigliamento
            self.filter_promowear.set_property('visible', True)
            fillComboboxGruppiTaglia(self.id_gruppo_taglia_articolo_filter_combobox, True)
            fillComboboxTaglie(self.id_taglia_articolo_filter_combobox, True)
            fillComboboxColori(self.id_colore_articolo_filter_combobox, True)
            fillComboboxAnniAbbigliamento(self.id_anno_articolo_filter_combobox, True)
            fillComboboxStagioniAbbigliamento(self.id_stagione_articolo_filter_combobox, True)
            fillComboboxGeneriAbbigliamento(self.id_genere_articolo_filter_combobox, True)
            if self._idGruppoTaglia is not None:
                findComboboxRowFromId(self.id_gruppo_taglia_articolo_filter_combobox, self._idGruppoTaglia)
            self.id_taglia_articolo_filter_combobox.set_active(0)
            if self._idTaglia is not None:
                findComboboxRowFromId(self.id_taglia_articolo_filter_combobox, self._idTaglia)
            self.id_colore_articolo_filter_combobox.set_active(0)
            if self._idColore is not None:
                findComboboxRowFromId(self.id_colore_articolo_filter_combobox, self._idColore)
            self.id_anno_articolo_filter_combobox.set_active(0)
            if self._idAnno is not None:
                findComboboxRowFromId(self.id_anno_articolo_filter_combobox, self._idAnno)
            else:
                if hasattr(Environment.conf,'TaglieColori'):
                    anno = getattr(Environment.conf.TaglieColori,'anno_default', None)
                    if anno is not None:
                        findComboboxRowFromId(self.id_anno_articolo_filter_combobox, int(anno))
            self.id_stagione_articolo_filter_combobox.set_active(0)
            if self._idStagione is not None:
                findComboboxRowFromId(self.id_stagione_articolo_filter_combobox, self._idStagione)
            else:
                if hasattr(Environment.conf,'TaglieColori'):
                    stagione = getattr(Environment.conf.TaglieColori,'stagione_default', None)
                    if stagione is not None:
                        findComboboxRowFromId(self.id_stagione_articolo_filter_combobox, int(stagione))
            self.id_genere_articolo_filter_combobox.set_active(0)
            if self._idGenere is not None:
                findComboboxRowFromId(self.id_colore_articolo_filter_combobox, self._idGenere)
            self.taglie_colori_filter_combobox.set_active(0)
            self.id_stato_articolo_filter_combobox.set_active(0)
            if not self._parentObject._taglia_colore:
                self.gruppo_taglia_filter_label.set_no_show_all(True)
                self.gruppo_taglia_filter_label.set_property('visible', False)
                self.id_gruppo_taglia_articolo_filter_combobox.set_property('visible', False)
                self.id_gruppo_taglia_articolo_filter_combobox.set_no_show_all(True)
                self.taglia_articolo_filter_label.set_no_show_all(True)
                self.taglia_articolo_filter_label.set_property('visible', False)
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

        self.denominazione_filter_entry.set_text(self._denominazione or '')
        self.produttore_filter_entry.set_text(self._produttore or '')
        self.codice_filter_entry.set_text(self._codice or '')
        self.codice_a_barre_filter_entry.set_text(self._codiceABarre or '')
        self.codice_articolo_fornitore_filter_entry.set_text(self._codiceArticoloFornitore or '')
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        if self._idFamiglia is not None:
            findComboboxowFromId(self.id_famiglia_articolo_filter_combobox, self._idFamiglia)
        self.id_categoria_articolo_filter_combobox.set_active(0)
        if self._idCategoria is not None:
            findComboboxRowFromId(self.id_categoria_articolo_filter_combobox, self._idCategoria)
        self.id_stato_articolo_filter_combobox.set_active(0)
        if self._idStato is not None:
            findComboboxRowFromId(self.id_stato_articolo_filter_combobox, self._idStato)
        self.cancellato_filter_label.set_property('visible', False)
        self.cancellato_filter_label.set_no_show_all(True)
        self.cancellato_filter_checkbutton.set_property('visible', False)
        self.cancellato_filter_checkbutton.set_no_show_all(True)


    def drawRicercaComplessa(self):
        """ Disegna e imposta i widgets relativi alla sola parte avanzata della ricerca """
        self.collapseAllExpanders()

        self.drawDescrizioneTreeView()
        self.drawProduttoreTreeView()
        self.drawCodiceTreeView()
        self.drawCodiceABarreTreeView()
        self.drawCodiceArticoloFornitoreTreeView()
        self.drawFamigliaTreeView()
        self.drawCategoriaTreeView()
        self.drawStatoTreeView()
        self.drawUnitaBaseTreeView()
        self.includi_eliminati_articolo_filter_checkbutton.set_active(self._cancellato or False)
        self.solo_eliminati_articolo_filter_checkbutton.set_active(False)
        if "PromoWear" in Environment.modulesList:
            self.drawGruppoTagliaTreeView()
            self.drawTagliaTreeView()
            self.drawColoreTreeView()
            self.drawAnnoTreeView()
            self.drawStagioneTreeView()
            self.drawGenereTreeView()
            self.includi_principali_articolo_filter_checkbutton.set_active(True)
            self.includi_varianti_articolo_filter_checkbutton.set_active(True)
            self.includi_normali_articolo_filter_checkbutton.set_active(True)

        self._activeExpander = None
        self.setRiepilogoArticolo()

    def drawGruppoTagliaTreeView(self):
        treeview = self.gruppo_taglia_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str, str)
        self._gruppoTagliaTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(4)

        grts = GruppoTaglia(isList=True).select(offset=None, batchSize=None)


        for g in grts:
            included = excluded = False
            if self._idGruppoTaglia is not None:
                included = self._idGruppoTaglia == g.id

            model.append((included,
                          excluded,
                          g.id,
                          g.denominazione_breve,
                          g.denominazione))

        treeview.set_model(model)


    def drawTagliaTreeView(self):
        treeview = self.taglia_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str, str)
        self._tagliaTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(4)

        tags = Taglia(isList=True).select(offset=None, batchSize=None)

        for t in tags:
            included = excluded = False
            if self._idTaglia is not None:
                included = self._idTaglia == t.id

            model.append((included,
                          excluded,
                          t.id,
                          t.denominazione_breve,
                          t.denominazione))

        treeview.set_model(model)


    def drawColoreTreeView(self):
        treeview = self.colore_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str, str)
        self._coloreTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(4)

        cols = Colore(isList=True).select(offset=None, batchSize=None)


        for c in cols:
            included = excluded = False
            if self._idColore is not None:
                included = self._idColore == c.id

            model.append((included,
                          excluded,
                          c.id,
                          c.denominazione_breve,
                          c.denominazione))

        treeview.set_model(model)


    def drawAnnoTreeView(self):
        treeview = self.anno_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str)
        self._annoTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(3)

        anno = self._idAnno
        if hasattr(Environment.conf.PromoWear,'TaglieColori'):
            default = getattr(Environment.conf.PromoWear.TaglieColori,'anno_default', None)
            if default is not None:
                anno = int(default)


        anns = AnnoAbbigliamento(isList=True).select(offset=None, batchSize=None)
        for a in anns:
            included = excluded = False
            if anno is not None:
                included = anno == a['id']

            model.append((included,
                          excluded,
                          a.id,
                          a.denominazione))

        treeview.set_model(model)

    def getArtsResult(self):
        return self.artsResult or None


    def drawStagioneTreeView(self):
        treeview = self.stagione_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str)
        self._stagioneTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(3)

        stagione = self._idStagione
        if hasattr(Environment.conf,'TaglieColori'):
            default = getattr(Environment.conf.TaglieColori,'stagione_default', None)
            if default is not None:
                stagione = int(default)

        stas = StagioneAbbigliamento(isList=True).select(offset=None, batchSize=None)

        for s in stas:
            included = excluded = False
            if stagione is not None:
                included = stagione == s['id']

            model.append((included,
                          excluded,
                          s.id,
                          s.denominazione))

        treeview.set_model(model)


    def drawGenereTreeView(self):
        treeview = self.genere_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str)
        self._genereTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(3)

        gens = GenereAbbigliamento(isList=True).select(offset=None, batchSize=None)

        for g in gens:
            included = excluded = False
            if self._idGenere is not None:
                included = self._idGenere == g['id']

            model.append((included,
                          excluded,
                          g.id,
                          g.denominazione))

        treeview.set_model(model)


    def drawStatoTreeView(self):
        treeview = self.stato_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str)
        self._statoTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(3)

        stas = promogest.dao.StatoArticolo.select(Environment.connection,
                                                  offset=None, batchSize=None,
                                                  immediate=True)

        for s in stas:
            included = excluded = False
            if self._idStato is not None:
                included = self._idStato == s.id

            model.append((included,
                        excluded,
                          s.id,
                          s.denominazione))

        treeview.set_model(model)


    def drawDescrizioneTreeView(self):
        treeview = self.descrizione_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._descrizioneTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Descrizione', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertDescrizione(self._denominazione)


    def drawProduttoreTreeView(self):
        treeview = self.produttore_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._produttoreTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Produttore', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertProduttore(self._produttore)


    def drawCodiceTreeView(self):
        treeview = self.codice_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._codiceTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Codice', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertCodice(self._codice)


    def drawCodiceABarreTreeView(self):
        treeview = self.codice_a_barre_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._codiceABarreTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Codice a barre', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertCodiceABarre(self._codiceABarre)


    def drawCodiceArticoloFornitoreTreeView(self):
        treeview = self.codice_articolo_fornitore_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._codiceArticoloFornitoreTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Codice articolo fornitore', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertCodiceArticoloFornitore(self._codiceArticoloFornitore)


    def drawFamigliaTreeView(self):
        treeview = self.famiglia_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.TreeStore(bool, bool, int, str, str, str)
        self._famigliaTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('', renderer)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width = 20
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Codice', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(5)

        fams = FamigliaArticolo(isList=True).select()
        def recurse_tree(id_padre, parent_iter=None, max_depth=None, ):
            if parent_iter is None :
                padre = None
                path = 0
                for row in self._famigliaTreeViewModel:
                    if row[0].id == id_padre:
                        padre = self._famigliaTreeViewModel.get_iter(path)
                    else:
                        iter = self._famigliaTreeViewModel.get_iter(path)
                        if self._famigliaTreeViewModel.iter_has_child(iter):
                            new_depth = self._famigliaTreeViewModel.iter_n_children(iter) or 0
                            if new_depth > 0:
                                padre = recurse_tree(id_padre, iter, new_depth)
                    if padre is not None:
                        break
                    else:
                        path += 1
            else:
                padre = None
                child_index = 0
                #if self._treeViewModel.iter_has_child(parent_iter):
                while child_index < max_depth:
                    child_iter = self._famigliaTreeViewModel.iter_nth_child(parent_iter, child_index)
                    if self._famigliaTreeViewModel[child_iter][0].id == id_padre:
                        padre = child_iter
                        break
                    else:
                        if self._famigliaTreeViewModel.iter_has_child(child_iter):
                            new_depth = self._famigliaTreeViewModel.iter_n_children(parent_iter) or 0
                            if new_depth > 0:
                                padre = recurse_tree(id_padre, child_iter, new_depth)
                        if padre is not None:
                            break
                    child_index += 1
            return padre
        for f in fams:
            if f.id_padre is None:
                included = excluded = False
                if self._idFamiglia is not None:
                    included = self._idFamiglia == f.id

                    node = model.append(padre, (included,
                                        excluded,
                                        f.id,
                                        f.codice,
                                        f.denominazione_breve,
                                        f.denominazione))

        for f in fams:
            if f.id_padre is not None:
                padre = recurse_tree(f.id_padre)
                included = excluded = False
                if self._idFamiglia is not None:
                    included = self._idFamiglia == f.id

                    node = model.append(padre, (included,
                                        excluded,
                                        f.id,
                                        f.codice,
                                        f.denominazione_breve,
                                        f.denominazione))
        nodes = []
        #for f in fams:
            #index_padre = int(f.depth - 1)
            #if index_padre < 0:
                #index_padre = 0

            #if f.depth == 0:
                #padre = None
            #else:
                #padre = nodes[index_padre]

            #included = excluded = False
            #if self._idFamiglia is not None:
                #included = self._idFamiglia == f.id

            #node = model.append(padre, (included,
                                        #excluded,
                                        #f.id,
                                        #f.codice,
                                        #f.denominazione_breve,
                                        #f.denominazione))

            #try:
                #nodes[f.depth] = node
            #except IndexError:
                #nodes.insert(f.depth + 1, node)

        treeview.set_model(model)


    def drawCategoriaTreeView(self):
        treeview = self.categoria_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str, str)
        self._categoriaTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(4)

        cats = CategoriaArticolo(isList=True).select(offset=None, batchSize=None)

        for c in cats:
            included = excluded = False
            if self._idCategoria is not None:
                included = self._idCategoria == c.id

            model.append((included,
                          excluded,
                          c.id,
                          c.denominazione_breve,
                          c.denominazione))

        treeview.set_model(model)


    def drawStatoTreeView(self):
        treeview = self.stato_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str)
        self._statoTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(3)

        stas = StatoArticolo(isList=True).select(offset=None, batchSize=None)


        for s in stas:
            included = excluded = False
            if self._idStato is not None:
                included = self._idStato == s.id

            model.append((included,
                          excluded,
                          s.id,
                          s.denominazione))

        treeview.set_model(model)


    def drawUnitaBaseTreeView(self):
        treeview = self.unita_base_articolo_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str, str)
        self._unitaBaseTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(4)

        units=UnitaBase(isList=True).select(batchSize=None,offset=None)
        for u in units:
            model.append((False,
                          False,
                          u.id,
                          u.denominazione_breve,
                          u.denominazione))

        treeview.set_model(model)


    def insertDescrizione(self, value=''):
        """ Inserimento nuova descrizione nella treeview """
        insertTreeViewRow(self.descrizione_articolo_filter_treeview, value)

    def deleteDescrizione(self):
        """ Eliminazione descrizione dalla treeview """
        deleteTreeViewRow(self.descrizione_articolo_filter_treeview)
        self.setRiepilogoArticolo()
        self.complexFilter= clearWhereString(self.complexFilter)


    def on_nuova_descrizione_articolo_filter_button_clicked(self, button=None):
        self.insertDescrizione()


    def on_cancella_descrizione_articolo_filter_button_clicked(self, button=None):
        self.deleteDescrizione()
        self.setRiepilogoArticolo()

    def insertProduttore(self, value=''):
        """ Inserimento nuovo produttore nella treeview """
        insertTreeViewRow(self.produttore_articolo_filter_treeview, value)


    def deleteProduttore(self):
        """ Eliminazione produttore dalla treeview """
        deleteTreeViewRow(self.produttore_articolo_filter_treeview)
        self.setRiepilogoArticolo()

    def on_nuovo_produttore_articolo_filter_button_clicked(self, button=None):
        self.insertProduttore()


    def on_cancella_produttore_articolo_filter_button_clicked(self, button=None):
        self.deleteProduttore()
        self.setRiepilogoArticolo()

    def insertCodice(self, value=''):
        """ Inserimento nuovo codice nella treeview """
        insertTreeViewRow(self.codice_articolo_filter_treeview, value)


    def deleteCodice(self):
        """ Eliminazione codice dalla treeview """
        deleteTreeViewRow(self.codice_articolo_filter_treeview)
        self.setRiepilogoArticolo()

    def on_nuovo_codice_articolo_filter_button_clicked(self, button=None):
        self.insertCodice()


    def on_cancella_codice_articolo_filter_button_clicked(self, button=None):
        self.deleteCodice()
        self.setRiepilogoArticolo()

    def insertCodiceABarre(self, value=''):
        """ Inserimento nuovo codice a barre nella treeview """
        insertTreeViewRow(self.codice_a_barre_articolo_filter_treeview, value)


    def deleteCodiceABarre(self):
        """ Eliminazione codice a barre dalla treeview """
        deleteTreeViewRow(self.codice_a_barre_articolo_filter_treeview)
        self.setRiepilogoArticolo()

    def on_nuovo_codice_a_barre_articolo_filter_button_clicked(self, button=None):
        self.insertCodiceABarre()


    def on_cancella_codice_a_barre_articolo_filter_button_clicked(self, button=None):
        self.deleteCodiceABarre()
        self.setRiepilogoArticolo()

    def insertCodiceArticoloFornitore(self, value=''):
        """ Inserimento nuovo codice articolo fornitore nella treeview """
        insertTreeViewRow(self.codice_articolo_fornitore_articolo_filter_treeview, value)


    def deleteCodiceArticoloFornitore(self):
        """ Eliminazione codice articolo fornitore dalla treeview """
        deleteTreeViewRow(self.codice_articolo_fornitore_articolo_filter_treeview)
        self.setRiepilogoArticolo()

    def on_nuovo_codice_articolo_fornitore_articolo_filter_button_clicked(self, button=None):
        self.insertCodiceArticoloFornitore()


    def on_cancella_codice_articolo_fornitore_articolo_filter_button_clicked(self, button=None):
        self.deleteCodiceArticoloFornitore()
        self.setRiepilogoArticolo()

    def on_descrizione_articolo_filter_treeview_key_press_event(self, widget, event):
        """ Gestione della pressione di tasti all'interno della treeview delle descrizioni """
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertDescrizione,
                                                self.deleteDescrizione,
                                                self.setRiepilogoArticolo)


    def on_produttore_articolo_filter_treeview_key_press_event(self, widget, event):
        """ Gestione della pressione di tasti all'interno della treeview dei produttori """
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertProduttore,
                                                self.deleteProduttore,
                                                self.setRiepilogoArticolo)


    def on_codice_articolo_filter_treeview_key_press_event(self, widget, event):
        """ Gestione della pressione di tasti all'interno della treeview dei codici """
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertCodice,
                                                self.deleteCodice,
                                                self.setRiepilogoArticolo)


    def on_codice_a_barre_articolo_filter_treeview_key_press_event(self, widget, event):
        """ Gestione della pressione di tasti all'interno della treeview dei codici a barre """
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertCodiceABarre,
                                                self.deleteCodiceABarre,
                                                self.setRiepilogoArticolo)


    def on_codice_articolo_fornitore_articolo_filter_treeview_key_press_event(self, widget, event):
        """ Gestione della pressione di tasti all'interno della treeview dei codici articolo fornitore """
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertCodiceArticoloFornitore,
                                                self.deleteCodiceArticoloFornitore,
                                                self.setRiepilogoArticolo)


    def on_descrizione_articolo_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview delle descrizioni """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_descrizione_articolo_filter_button.set_property('sensitive', (iterator is not None))


    def on_produttore_articolo_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview dei produttori """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_produttore_articolo_filter_button.set_property('sensitive', (iterator is not None))


    def on_codice_articolo_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview dei codici """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_codice_articolo_filter_button.set_property('sensitive', (iterator is not None))


    def on_codice_a_barre_articolo_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview dei codici a barre """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_codice_a_barre_articolo_filter_button.set_property('sensitive', (iterator is not None))


    def on_codice_articolo_fornitore_articolo_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview dei codici articolo fornitore """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_codice_articolo_fornitore_articolo_filter_button.set_property('sensitive', (iterator is not None))


    def onColumnEdited(self, cell, path, value, treeview, editNext=False):
        """ Gestione del salvataggio dei valori impostati nelle colonne di una treeview """
        onColumnEdited(cell, path, value, treeview, editNext, self.setRiepilogoArticolo)


    def columnSelectAll(self, column, treeview):
        """
        Gestisce la selezione/deselezione alternata delle colonne
        di inclusione/esclusione valori
        """
        columnSelectAll(column, treeview, self.setRiepilogoArticolo)


    def on_any_expander_expanded(self, expander):
        """ Permette ad un solo expander alla volta di essere espanso """
        if self._activeExpander is not None and self._activeExpander != expander:
            self._activeExpander.set_expanded(False)
        self._activeExpander = expander


    def collapseAllExpanders(self):
        """ Chiude tutti gli expander """
        self.descrizione_articolo_filter_expander.set_expanded(False)
        self.produttore_articolo_filter_expander.set_expanded(False)
        self.codice_articolo_filter_expander.set_expanded(False)
        self.codice_a_barre_articolo_filter_expander.set_expanded(False)
        self.codice_articolo_fornitore_articolo_filter_expander.set_expanded(False)
        self.famiglia_articolo_filter_expander.set_expanded(False)
        self.categoria_articolo_filter_expander.set_expanded(False)
        self.stato_articolo_filter_expander.set_expanded(False)
        self.unita_base_articolo_filter_expander.set_expanded(False)
        self.varie_articolo_filter_expander.set_expanded(False)
        if "PromoWear" in Environment.modulesList:
            self.gruppo_taglia_articolo_filter_expander.set_expanded(False)
            self.taglia_articolo_filter_expander.set_expanded(False)
            self.colore_articolo_filter_expander.set_expanded(False)
            self.anno_articolo_filter_expander.set_expanded(False)
            self.stagione_articolo_filter_expander.set_expanded(False)
            self.genere_articolo_filter_expander.set_expanded(False)


    def on_includi_principali_articolo_filter_checkbutton_toggled(self, widget):
        """ Gestisce l'impostazione della checkbox relativa """
        if not(widget.get_active()) and not(self.includi_varianti_articolo_filter_checkbutton.get_active()):
            self.includi_normali_articolo_filter_checkbutton.set_active(True)
        self.setRiepilogoArticolo()


    def on_includi_varianti_articolo_filter_checkbutton_toggled(self, widget):
        """ Gestisce l'impostazione della checkbox relativa """
        if not(widget.get_active()) and not(self.includi_principali_articolo_filter_checkbutton.get_active()):
            self.includi_normali_articolo_filter_checkbutton.set_active(True)


    def on_includi_normali_articolo_filter_checkbutton_toggled(self, widget):
        """ Gestisce l'impostazione della checkbox relativa """
        if not(widget.get_active()):
            self.includi_principali_articolo_filter_checkbutton.set_active(True)
            self.includi_varianti_articolo_filter_checkbutton.set_active(True)
        self.setRiepilogoArticolo()

    def on_includi_eliminati_articolo_filter_checkbutton_toggled(self, widget):
        """ Gestisce l'impostazione della checkbox relativa """
        if widget.get_active():
            self.solo_eliminati_articolo_filter_checkbutton.set_active(False)
        self.setRiepilogoArticolo()


    def on_solo_eliminati_articolo_filter_checkbutton_toggled(self, widget):
        """ Gestisce l'impostazione della checkbox relativa """
        if widget.get_active():
            self.includi_eliminati_articolo_filter_checkbutton.set_active(False)
        self.setRiepilogoArticolo()


    def on_campo_filter_entry_key_press_event(self, widget, event):
        """ Conferma parametri filtro x ricerca semplice da tastiera """
        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname == 'Return' or keyname == 'KP_Enter':
            self._parentObject.refresh()


    def setRiepilogoArticolo(self):
        """ In base ai filtri impostati costruisce il testo del riepilogo """

        def buildIncludedString(row, index):
            if row[0]:
                self._includedString += '     + ' + row[index] + '\n'

        def buildExcludedString(row, index):
            if row[1]:
                self._excludedString += '     - ' + row[index] + '\n'

        testo = ''

        model = self._descrizioneTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Descrizione:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._produttoreTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Produttore:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._codiceTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Codice:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._codiceABarreTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Codice a barre:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._codiceArticoloFornitoreTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Codice articolo fornitore:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._famigliaTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 5)
        if self._includedString != '':
            testo += '  Famiglia:\n'
            testo += self._includedString

        model = self._categoriaTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 4)
        if self._includedString != '':
            testo += '  Categoria:\n'
            testo += self._includedString

        model = self._statoTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 3)
        if self._includedString != '':
            testo += '  Stato:\n'
            testo += self._includedString

        model = self._unitaBaseTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 3)
        if self._includedString != '':
            testo += '  Unita\' base:\n'
            testo += self._includedString

        if self.includi_eliminati_articolo_filter_checkbutton.get_active():
            testo += '  + Compresi articoli eliminati\n'

        if self.solo_eliminati_articolo_filter_checkbutton.get_active():
            testo += '  + Solo articoli eliminati\n'

        if "PromoWear" in Environment.modulesList:
            model = self._gruppoTagliaTreeViewModel
            self._includedString = ''
            parseModel(model, buildIncludedString, 4)
            if self._includedString != '':
                testo += '  Gruppo taglia:\n'
                testo += self._includedString

            model = self._tagliaTreeViewModel
            self._includedString = ''
            parseModel(model, buildIncludedString, 4)
            if self._includedString != '':
                testo += '  Taglia:\n'
                testo += self._includedString

            model = self._coloreTreeViewModel
            self._includedString = ''
            parseModel(model, buildIncludedString, 4)
            if self._includedString != '':
                testo += '  Colore:\n'
                testo += self._includedString

            model = self._annoTreeViewModel
            self._includedString = ''
            parseModel(model, buildIncludedString, 3)
            if self._includedString != '':
                testo += '  Anno:\n'
                testo += self._includedString

            model = self._stagioneTreeViewModel
            self._includedString = ''
            parseModel(model, buildIncludedString, 3)
            if self._includedString != '':
                testo += '  Stagione:\n'
                testo += self._includedString

            model = self._genereTreeViewModel
            self._includedString = ''
            parseModel(model, buildIncludedString, 3)
            if self._includedString != '':
                testo += '  Genere:\n'
                testo += self._includedString

            if self.includi_principali_articolo_filter_checkbutton.get_active():
                testo += '  + Compresi articoli principali taglia/colore\n'

            if self.includi_varianti_articolo_filter_checkbutton.get_active():
                testo += '  + Comprese varianti taglia/colore\n'

            if self.includi_normali_articolo_filter_checkbutton.get_active():
                testo += '  + Compresi articoli no taglia/colore\n'

        if self.textBefore is not None:
            testo = self.textBefore + testo
        if self.textAfter is not None:
            testo = testo + self.textAfter

        buffer = self.riepilogo_articolo_filter_textview.get_buffer()
        buffer.set_text(testo)
        self.riepilogo_articolo_filter_textview.set_buffer(buffer)


    def getRiepilogoArticolo(self):
        """ Restituisce il testo relativo al riepilogo dei filtri impostati """
        # puo' essere richiamato da una classe derivata o proprietaria per costruire
        # dei riepiloghi globali in caso di ricerche su piu' elementi diversi
        if self._tipoRicerca == 'semplice':
            testo = ''

            value = self.denominazione_filter_entry.get_text()
            if value != '':
                testo += '  Descrizione:\n'
                testo += '       ' + value + '\n'

            value = self.produttore_filter_entry.get_text()
            if value != '':
                testo += '  Produttore:\n'
                testo += '       ' + value + '\n'

            value = self.codice_filter_entry.get_text()
            if value != '':
                testo += '  Codice:\n'
                testo += '       ' + value + '\n'

            value = self.codice_a_barre_filter_entry.get_text()
            if value != '':
                testo += '  Codice a barre:\n'
                testo += '       ' + value + '\n'

            value = self.codice_articolo_fornitore_filter_entry.get_text()
            if value != '':
                testo += '  Codice articolo fornitore:\n'
                testo += '       ' + value + '\n'

            if self.id_famiglia_articolo_filter_combobox.get_active() != -1:
                value = self.id_famiglia_articolo_filter_combobox.get_active_text()
                testo += '  Famiglia:\n'
                testo += '       ' + value + '\n'

            if self.id_categoria_articolo_filter_combobox.get_active() != -1:
                value = self.id_categoria_articolo_filter_combobox.get_active_text()
                testo += '  Categoria:\n'
                testo += '       ' + value + '\n'

            if self.id_stato_articolo_filter_combobox.get_active() != -1:
                value = self.id_stato_articolo_filter_combobox.get_active_text()
                testo += '  Stato:\n'
                testo += '       ' + value + '\n'

            if self.cancellato_filter_checkbutton.get_active():
                testo += '  Compresi articoli eliminati\n'

            return testo
        else:
            buffer = self.riepilogo_articolo_filter_textview.get_buffer()
            return buffer.get_text()


    def clear(self):
        # Annullamento filtro
        if self._tipoRicerca == 'semplice':
            self.drawRicercaSemplice()
        elif self._tipoRicerca == 'avanzata':
            self.drawRicercaComplessa()
        self._parentObject.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        model = self._parentObject.filter.resultsElement.get_model()

        self.complexFilter = self._prepare()

        if self._tipoRicerca == 'semplice':
            denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
            produttore = prepareFilterString(self.produttore_filter_entry.get_text())
            codice = prepareFilterString(self.codice_filter_entry.get_text())
            codiceABarre = prepareFilterString(self.codice_a_barre_filter_entry.get_text())
            codiceArticoloFornitore = prepareFilterString(self.codice_articolo_fornitore_filter_entry.get_text())
            idFamiglia = findIdFromCombobox(self.id_famiglia_articolo_filter_combobox)
            idCategoria = findIdFromCombobox(self.id_categoria_articolo_filter_combobox)
            idStato = findIdFromCombobox(self.id_stato_articolo_filter_combobox)
            cancellato = False
            if "PromoWear" in Environment.modulesList and self._parentObject._taglia_colore:
                idGruppoTaglia = findIdFromCombobox(self.id_gruppo_taglia_articolo_filter_combobox)
                idTaglia = findIdFromCombobox(self.id_taglia_articolo_filter_combobox)
                idColore = findIdFromCombobox(self.id_colore_articolo_filter_combobox)
                idAnno = findIdFromCombobox(self.id_anno_articolo_filter_combobox)
                idStagione = findIdFromCombobox(self.id_stagione_articolo_filter_combobox)
                idGenere = findIdFromCombobox(self.id_genere_articolo_filter_combobox)
                padriTagliaColore = ((self.taglie_colori_filter_combobox.get_active() == 0) or
                                     (self.taglie_colori_filter_combobox.get_active() == 1))
                figliTagliaColore = ((self.taglie_colori_filter_combobox.get_active() == 0) or
                                     (self.taglie_colori_filter_combobox.get_active() == 2))
            else:
                idGruppoTaglia = None
                idTaglia = None
                idColore = None
                idAnno = None
                idStagione = None
                idGenere = None
                padriTagliaColore = None
                figliTagliaColore = None
        elif self._tipoRicerca == 'avanzata':
            # tutti i filtri vengono annullati in modo che nella stored procedure di select
            # venga fatta la join con il risultato della query di filtraggio sugli articoli
            denominazione = None
            produttore = None
            codice = None
            codiceABarre = None
            codiceArticoloFornitore = None
            idFamiglia = None
            idCategoria = None
            idStato = None
            cancellato = None
            idGruppoTaglia = None
            idTaglia = None
            idColore = None
            idAnno = None
            idStagione = None
            idGenere = None
            padriTagliaColore = None
            figliTagliaColore = None
            #if self.complexFilter:
                #self.complexFilter= and_(*self.complexFilter)
        if "Promowear" in Environment.modulesList:
            self.filter.numRecords = Articolo(isList=True).count(denominazione=denominazione,
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
        else:
            self.filter.numRecords = Articolo(isList=True).count(denominazione=denominazione,
                                        codice=codice,
                                        codiceABarre=codiceABarre,
                                        codiceArticoloFornitore=codiceArticoloFornitore,
                                        produttore=produttore,
                                        idFamiglia=idFamiglia,
                                        idCategoria=idCategoria,
                                        idStato=idStato,
                                        cancellato=cancellato,
                                        complexFilter=self.complexFilter)
        self.resultsCount = self.filter.numRecords
        self.filter._refreshPageCount()
        if "PromoWear" in Environment.modulesList:
            arts = Articolo(isList=True).select(orderBy=self.filter.orderBy,
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
                                             offset=self.filter.offset,
                                             batchSize=self.filter.batchSize)
            model.clear()
            for a in arts:
                bgCol = None
                if a.cancellato:
                    bgCol = 'red'
                model.append((a,
                            bgCol,
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
        else:
            arts = Articolo(isList=True).select(orderBy=self.filter.orderBy,
                                                    denominazione=denominazione,
                                                    codice=codice,
                                                    codiceABarre=codiceABarre,
                                                    codiceArticoloFornitore=codiceArticoloFornitore,
                                                    produttore=produttore,
                                                    idFamiglia=idFamiglia,
                                                    idCategoria=idCategoria,
                                                    idStato=idStato,
                                                    cancellato=cancellato,
                                                    offset=self.filter.offset,
                                                    batchSize=self.filter.batchSize,
                                                    complexFilter=self.complexFilter)

            model.clear()

            for a in arts:
                bgCol = None
                if a.cancellato:
                    bgCol = 'red'
                model.append((a,
                            bgCol,
                            (a.codice or ''),
                            (a.denominazione or ''),
                            (a.produttore or ''),
                            (a.codice_a_barre or ''),
                            (a.codice_articolo_fornitore or ''),
                            (a.denominazione_famiglia or ''),
                            (str(a.denominazione_categoria) or '')))

        self.artsResult = arts
    def _prepare(self):
        """
        Viene costruita ed eseguita la query di filtraggio sugli articoli in base
        ai filtri impostati
        """
        stringa= []
        wherestring=[]
        def getDescrizioniIn(row, index):
            if row[0]:
                self._descrizioniIn.append(optimizeString(row[index]))

        def getDescrizioniOut(row, index):
            if row[1]:
                self._descrizioniOut.append(optimizeString(row[index]))

        def getProduttoriIn(row, index):
            if row[0]:
                self._produttoriIn.append(optimizeString(row[index]))

        def getProduttoriOut(row, index):
            if row[1]:
                self._produttoriOut.append(optimizeString(row[index]))

        def getCodiciIn(row, index):
            if row[0]:
                self._codiciIn.append(optimizeString(row[index]))

        def getCodiciOut(row, index):
            if row[1]:
                self._codiciOut.append(optimizeString(row[index]))

        def getCodiciABarreIn(row, index):
            if row[0]:
                self._codiciABarreIn.append(optimizeString(row[index]))

        def getCodiciABarreOut(row, index):
            if row[1]:
                self._codiciABarreOut.append(optimizeString(row[index]))

        def getCodiciArticoloFornitoreIn(row, index):
            if row[0]:
                self._codiciArticoloFornitoreIn.append(optimizeString(row[index]))

        def getCodiciArticoloFornitoreOut(row, index):
            if row[1]:
                self._codiciArticoloFornitoreOut.append(optimizeString(row[index]))

        def getFamiglieIn(row, index):
            if row[0]:
                self._idFamiglieIn.append(row[index])

        def getCategorieIn(row, index):
            if row[0]:
                self._idCategorieIn.append(row[index])

        def getStatiIn(row, index):
            if row[0]:
                self._idStatiIn.append(row[index])

        def getUnitaBaseIn(row, index):
            if row[0]:
                self._idUnitaBaseIn.append(row[index])

        def getGruppiTagliaIn(row, index):
            if row[0]:
                self._idGruppiTagliaIn.append(row[index])

        def getTaglieIn(row, index):
            if row[0]:
                self._idTaglieIn.append(row[index])

        def getColoriIn(row, index):
            if row[0]:
                self._idColoriIn.append(row[index])

        def getAnniIn(row, index):
            if row[0]:
                self._idAnniIn.append(row[index])

        def getStagioniIn(row, index):
            if row[0]:
                self._idStagioniIn.append(row[index])

        def getGeneriIn(row, index):
            if row[0]:
                self._idGeneriIn.append(row[index])



        # eliminazione tabella articoli filtrati

        self.resultsCount = 0
        if self._tipoRicerca == 'avanzata':
            self._descrizioniIn = []
            self._descrizioniOut = []
            self._produttoriIn = []
            self._produttoriOut = []
            self._codiciIn = []
            self._codiciOut = []
            self._codiciABarreIn = []
            self._codiciABarreOut = []
            self._codiciArticoloFornitoreIn = []
            self._codiciArticoloFornitoreOut = []
            self._idFamiglieIn = []
            self._idCategorieIn = []
            self._idStatiIn = []
            self._idUnitaBaseIn = []
            self._idGruppiTagliaIn = []
            self._idTaglieIn = []
            self._idColoriIn = []
            self._idAnniIn = []
            self._idStagioniIn = []
            self._idGeneriIn = []
            self._principaliIn = None
            self._variantiIn = None
            self._normaliIn = None
            self._eliminatiIn = None
            self._soloEliminatiIn = None

            parseModel(self._descrizioneTreeViewModel, getDescrizioniIn, 2)
            parseModel(self._descrizioneTreeViewModel, getDescrizioniOut, 2)
            parseModel(self._produttoreTreeViewModel, getProduttoriIn, 2)
            parseModel(self._produttoreTreeViewModel, getProduttoriOut, 2)
            parseModel(self._codiceTreeViewModel, getCodiciIn, 2)
            parseModel(self._codiceTreeViewModel, getCodiciOut, 2)
            parseModel(self._codiceABarreTreeViewModel, getCodiciABarreIn, 2)
            parseModel(self._codiceABarreTreeViewModel, getCodiciABarreOut, 2)
            parseModel(self._codiceArticoloFornitoreTreeViewModel, getCodiciArticoloFornitoreIn, 2)
            parseModel(self._codiceArticoloFornitoreTreeViewModel, getCodiciArticoloFornitoreOut, 2)
            parseModel(self._famigliaTreeViewModel, getFamiglieIn, 2)
            parseModel(self._categoriaTreeViewModel, getCategorieIn, 2)
            parseModel(self._statoTreeViewModel, getStatiIn, 2)
            parseModel(self._unitaBaseTreeViewModel, getUnitaBaseIn, 2)
            if "PromoWear" in Environment.modulesList:
                parseModel(self._gruppoTagliaTreeViewModel, getGruppiTagliaIn, 2)
                parseModel(self._tagliaTreeViewModel, getTaglieIn, 2)
                parseModel(self._coloreTreeViewModel, getColoriIn, 2)
                parseModel(self._annoTreeViewModel, getAnniIn, 2)
                parseModel(self._stagioneTreeViewModel, getStagioniIn, 2)
                parseModel(self._genereTreeViewModel, getGeneriIn, 2)
                self._principaliIn = self.includi_principali_articolo_filter_checkbutton.get_active()
                self._variantiIn = self.includi_varianti_articolo_filter_checkbutton.get_active()
                self._normaliIn = self.includi_normali_articolo_filter_checkbutton.get_active()

            if self.includi_eliminati_articolo_filter_checkbutton.get_active():
                self._eliminatiIn = True
            if self.solo_eliminati_articolo_filter_checkbutton.get_active():
                self._soloEliminatiIn = True

            #selectString = "SELECT A.id FROM " + Environment.params['schema'] + ".articolo A"
            joinString = ""
            whereString = ""
            wherestring = []

            if len(self._descrizioniIn) >0:
                variabili = []
                for stri in self._descrizioniIn:
                    stringa= and_(Articolo.denominazione.ilike("%"+stri+"%"))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._descrizioniOut) >0:
                variabili = []
                for stri in self._descrizioniOut:
                    stringa= and_(not_(Articolo.denominazione.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus = and_(*variabili)
                wherestring.append(datus)

            if len(self._produttoriIn) >0:
                variabili = []
                for stri in self._produttoriIn:
                    stringa= and_(Articolo.produttore.ilike("%"+stri+"%"))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if  len(self._produttoriOut) >0:
                variabili = []
                for stri in self._produttoriOut:
                    stringa= and_(not_(Articolo.produttore.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus= and_(*variabili)
                wherestring.append(datus)

            if len(self._codiciIn) >0:
                variabili = []
                for stri in self._codiciIn:
                    stringa= and_(Articolo.codice.ilike("%"+stri+"%"))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._codiciOut) >0:
                variabili = []
                for stri in self._codiciOut:
                    stringa= and_(not_(Articolo.codice.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus= and_(*variabili)
                wherestring.append(datus)

            #usata codice barre del mapper in quanto non serve il filtro per predefinito..
            if len(self._codiciABarreIn) >0:
                variabili = []
                for stri in self._codiciABarreIn:
                    quer= Environment.params["session"].query(CodiceABarreArticolo)\
                    .filter(CodiceABarreArticolo.codice.ilike("%"+stri+"%")).all()
                    for q in quer:
                        stringa= and_(Articolo.id == q.id_articolo )
                        #stringa= and_(Articolo.cod_barre.ilike("%"+stri+"%"))
                        variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._codiciABarreOut) >0:
                variabili = []
                for stri in self._codiciABarreOut:
                    quer= Environment.params["session"].query(CodiceABarreArticolo)\
                    .filter(not_(CodiceABarreArticolo.codice.ilike("%"+stri+"%"))).all()
                    for q in quer:
                        stringa= and_(Articolo.id ==q.id_articolo)
                        #stringa= and_(not_(CodiceABarreArticolo.codice.ilike("%"+stri+"%")))
                        variabili.append(stringa)
                datus= and_(*variabili)
                wherestring.append(datus)


            if len(self._codiciArticoloFornitoreIn) > 0:
                variabili = []
                for stri in self._codiciArticoloFornitoreIn:
                    stringa= and_(Articolo.codice_articolo_fornitore.ilike("%"+stri+"%"))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._codiciArticoloFornitoreOut) > 0:
                variabili = []
                for stri in self._codiciArticoloFornitoreOut:
                    stringa= and_(not_(Articolo.codice_articolo_fornitore.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus= and_(*variabili)
                wherestring.append(datus)

            if len(self._idFamiglieIn) > 0:
                variabili = []
                for stri in self._idFamiglieIn:
                    quer= Environment.params["session"].query(FamigliaArticolo)\
                            .filter(FamigliaArticolo.id ==stri).all()
                    for q in quer:
                        stringa= and_(Articolo.id == q.id_articolo)
                        variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._idCategorieIn) > 0:
                variabili = []
                for stri in self._idCategorieIn:
                    quer= Environment.params["session"].query(CategoriaArticolo)\
                            .filter(CategoriaArticolo.id ==stri).all()
                    for q in quer:
                        stringa= and_(Articolo.id == q.id_articolo)
                        variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._idStatiIn) > 0:
                variabili = []
                for stri in self._idStatiIn:
                    quer= Environment.params["session"].query(StatoArticolo)\
                            .filter(StatoArticolo.id ==stri).all()
                    for q in quer:
                        stringa= and_(Articolo.id_stato_articolo == q.id)
                        variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._idUnitaBaseIn) > 0:
                variabili = []
                for stri in self._idUnitaBaseIn:
                    quer= Environment.params["session"].query(UnitaBase)\
                            .filter(UnitaBase.id ==stri).all()
                    for q in quer:
                        stringa= and_(Articolo.id_unita_base == q.id)
                        variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            #if self._principaliIn or self._variantiIn:
                #if self._normaliIn:
                    #joinString += " LEFT OUTER"
                #else:
                    #joinString += " INNER"
                #joinString += " JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo"

                #if not (self._principaliIn and self._variantiIn):
                    #if self._principaliIn:
                        #joinString += " AND ATC.id_articolo_padre IS NULL"
                    #if self._variantiIn:
                        #joinString += " AND ATC.id_articolo_padre IS NOT NULL"

                #if len(self._idGruppiTagliaIn) > 0:
                    #joinString += " LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id"

                    #if len(self._idGruppiTagliaIn) > 0:
                        #condition = ""
                        #for e in self._idGruppiTagliaIn:
                            #if condition != "":
                                #condition += " OR "
                            #condition += "GT.id = " + str(e)
                        #if whereString != "":
                            #whereString += " AND "
                        #whereString += "(" + condition + ")"

                #if len(self._idTaglieIn) > 0:
                    #joinString += " LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id"

                    #if len(self._idTaglieIn) > 0:
                        #condition = ""
                        #for e in self._idTaglieIn:
                            #if condition != "":
                                #condition += " OR "
                            #condition += "T.id = " + str(e)
                        #if whereString != "":
                            #whereString += " AND "
                        #whereString += "(" + condition + ")"

                #if len(self._idColoriIn) > 0:
                    #joinString += " LEFT OUTER JOIN colore C ON ATC.id_colore = C.id"

                    #if len(self._idColoriIn) > 0:
                        #condition = ""
                        #for e in self._idColoriIn:
                            #if condition != "":
                                #condition += " OR "
                            #condition += "C.id = " + str(e)
                        #if whereString != "":
                            #whereString += " AND "
                        #whereString += "(" + condition + ")"

                #if len(self._idAnniIn) > 0:
                    #joinString += " LEFT OUTER JOIN promogest.anno_abbigliamento AA ON ATC.id_anno = AA.id"

                    #if len(self._idAnniIn) > 0:
                        #condition = ""
                        #for e in self._idAnniIn:
                            #if condition != "":
                                #condition += " OR "
                            #condition += "AA.id = " + str(e)
                        #if whereString != "":
                            #whereString += " AND "
                        #whereString += "(" + condition + ")"

                #if len(self._idStagioniIn) > 0:
                    #joinString += " LEFT OUTER JOIN promogest.stagione_abbigliamento SA ON ATC.id_stagione = SA.id"

                    #if len(self._idStagioniIn) > 0:
                        #condition = ""
                        #for e in self._idStagioniIn:
                            #if condition != "":
                                #condition += " OR "
                            #condition += "SA.id = " + str(e)
                        #if whereString != "":
                            #whereString += " AND "
                        #whereString += "(" + condition + ")"

                #if len(self._idAnniIn) > 0:
                    #joinString += " LEFT OUTER JOIN promogest.genere_abbigliamento GA ON ATC.id_genere = GA.id"

                    #if len(self._idGeneriIn) > 0:
                        #condition = ""
                        #for e in self._idGeneriIn:
                            #if condition != "":
                                #condition += " OR "
                            #condition += "GA.id = " + str(e)
                        #if whereString != "":
                            #whereString += " AND "
                        #whereString += "(" + condition + ")"


            if self._soloEliminatiIn:
                variabili = []
                stringa = and_(Articolo.cancellato == True)
                variabili.append(stringa)
                datus= and_(*variabili)
                wherestring.append(datus)
            elif not self._eliminatiIn:
                variabili = []
                stringa = and_(Articolo.cancellato == False)
                variabili.append(stringa)
                datus= and_(*variabili)
                wherestring.append(datus)
            self.complexFilter=and_(*wherestring)
        return self.complexFilter
