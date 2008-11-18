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
from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit
from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Fornitura
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo
from GladeWidget import GladeWidget
from utils import *
from utilsCombobox import *
if "PromoWear" in Environment.modulesList:
    from promogest.modules.PromoWear.ui.PromowearUtils import *
    from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
    from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
    from promogest.modules.PromoWear.dao.Taglia import Taglia
    from promogest.modules.PromoWear.dao.Colore import Colore
    from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
    #import promogest.modules.PromoWear.dao.ArticoloPromowear
    #from promogest.modules.PromoWear.dao.ArticoloPromowear import ArticoloPromowear as Articolo
#else:

class AnagraficaArticoli(Anagrafica):
    """ Anagrafica articoli """

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

    def on_record_edit_activate(self, widget, path=None, column=None):
        dao = self.filter.getSelectedDao()
        if dao.cancellato:
            msg = "L'articolo risulta eliminato.\nSi desidera riattivare l'articolo ?"
            dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                daoArticolo = Articolo(id= dao.id).getRecord()
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
        self.editElement.dao = Articolo().getRecord()

        if "PromoWear" in Environment.modulesList:
                # le varianti non si possono duplicare !!!
                #articoloTagliaColore = dao.articoloTagliaColore
                if dao.id_articolo_padre is not None:
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
        self.editElement.dao.url_immagine = dao.url_immagine
        self.editElement.dao.cancellato = dao.cancellato
        self.editElement.dao.sospeso = dao.sospeso
        self.editElement.dao.id_stato_articolo = dao.id_stato_articolo
        self.editElement.dao.quantita_minima = dao.quantita_minima

        if self.editElement._codiceByFamiglia:
            self.editElement.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=dao.id_famiglia_articolo)
        else:
            self.editElement.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=None)

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
                                  gladeFile='_anagrafica_articoli_elements.glade')
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
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'codice_a_barre')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', renderer, text=6, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'codice_articolo_fornitore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Famiglia', renderer, text=7, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'denominazione_famiglia')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Categoria', renderer, text=8, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'denominazione_categoria')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)
        if "PromoWear" in Environment.modulesList:
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
            self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
        else:
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
            self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str)
        treeview.set_search_column(2)

        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)
        self.filter_promowear.set_property('visible', "PromoWear" in Environment.modulesList)

        self.clear()


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
            #gestione anno abbigliamento con prelievo del dato di default dal configure
            self.id_anno_articolo_filter_combobox.set_active(0)
            anno = getattr(Environment.conf.PromoWear,'anno_default', None)
            if anno is not None:
                try:
                    idAnno = AnnoAbbigliamento(isList = True).select(denominazione = anno)[0].id
                    findComboboxRowFromId(self.id_anno_articolo_filter_combobox, idAnno)
                except:
                    pass
            #gestione stagione abbigliamento con prelievo del dato di default dal configure ( nb da usare l'id)
            self.id_stagione_articolo_filter_combobox.set_active(0)
            stagione = getattr(Environment.conf.PromoWear,'stagione_default', None)
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
            cancellato = False
        else:
            cancellato = True
        if "PromoWear" in Environment.modulesList:
            padriTagliaColore = ((self.taglie_colori_filter_combobox.get_active() == 0) or
                                 (self.taglie_colori_filter_combobox.get_active() == 1))
            if padriTagliaColore: padriTagliaColore = None
            else:padriTagliaColore = True
            figliTagliaColore = ((self.taglie_colori_filter_combobox.get_active() == 0) or
                                 (self.taglie_colori_filter_combobox.get_active() == 2))
            if figliTagliaColore:figliTagliaColore = None
            else:figliTagliaColore = True
            idGruppoTaglia = findIdFromCombobox(self.id_gruppo_taglia_articolo_filter_combobox)
            idTaglia = findIdFromCombobox(self.id_taglia_articolo_filter_combobox)
            idColore = findIdFromCombobox(self.id_colore_articolo_filter_combobox)
            idAnno = findIdFromCombobox(self.id_anno_articolo_filter_combobox)
            idStagione = findIdFromCombobox(self.id_stagione_articolo_filter_combobox)
            idGenere = findIdFromCombobox(self.id_genere_articolo_filter_combobox)

        def filterCountClosure():
            if "PromoWear" in Environment.modulesList:
                return Articolo(isList=True).count(denominazione=denominazione,
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
                return Articolo(isList=True).count(denominazione=denominazione,
                                                    codice=codice,
                                                    codiceABarre=codiceABarre,
                                                    codiceArticoloFornitore=codiceArticoloFornitore,
                                                    produttore=produttore,
                                                    idFamiglia=idFamiglia,
                                                    idCategoria=idCategoria,
                                                    idStato=idStato,
                                                    cancellato=cancellato)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            if "PromoWear" in Environment.modulesList:
                return Articolo(isList=True).select(orderBy=self.orderBy,
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
            else:
                return Articolo(isList=True).select(orderBy=self.orderBy,
                                        denominazione=denominazione,
                                        codice=codice,
                                        codiceABarre=codiceABarre,
                                        codiceArticoloFornitore=codiceArticoloFornitore,
                                        produttore=produttore,
                                        idFamiglia=idFamiglia,
                                        idCategoria=idCategoria,
                                        idStato=idStato,
                                        cancellato=cancellato,
                                        offset=offset,
                                        batchSize=batchSize)

        self._filterClosure = filterClosure

        arts = self.runFilter()
        self._treeViewModel.clear()
        for a in arts:
            col = None
            if a.cancellato:
                col = 'red'
            if "PromoWear" in Environment.modulesList:
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
            else:
                self._treeViewModel.append((a,
                                        col,
                                        (a.codice or ''),
                                        (a.denominazione or ''),
                                        (a.produttore or ''),
                                        (a.codice_a_barre or ''),
                                        (a.codice_articolo_fornitore or ''),
                                        (a.denominazione_famiglia or ''),
                                        (a.denominazione_categoria or '')))


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
        #FIXME: promogest.dao.Articolo.isNuovoCodiceByFamiglia()
        self._codiceByFamiglia = promogest.dao.Articolo.isNuovoCodiceByFamiglia()
        self._duplicatedDaoId = None
        self.tipoArticoloTagliaColore=False
        if "PromoWear" not in Environment.modulesList:
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
            self.promowear_frame.destroy()


    def draw(self):
        if "PromoWear" in Environment.modulesList:
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

        #combo e draw della parte normale dell'applicazione  ...
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
        fillComboboxUnitaFisica(self.unita_dimensioni_comboboxentry,'dimensioni')
        #Popola comboboxentry unita volume
        fillComboboxUnitaFisica(self.unita_volume_comboboxentry,'volume')
        #Popola comboboxentry unita peso
        fillComboboxUnitaFisica(self.unita_peso_comboboxentry,'peso')


    def setDao(self, dao):
        self.tipoArticoloTagliaColore=False
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Articolo().getRecord()
            # Assegna il codice se ne e' prevista la crazione automatica, ma non per famiglia
            if not self._codiceByFamiglia:
                self.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=None)
                print "STAMPO IL NUOVO CODICE ARTICOLO IN SETDAO GENERATO",self.dao.codice
            # Prova a impostare "pezzi" come unita' di misura base
            self.dao.id_unita_base = 1
            self._oldDaoRicreato = False
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Articolo(id=dao.id).getRecord()
            self._oldDaoRicreato = True
        self._refresh()


    def _refresh(self):
        self._loading = True
        self.codice_entry.set_text(self.dao.codice or '')
        print "STAMPO IL NUOVO CODICE ARTICOLO IN _REFRESH ",self.dao.codice
        if self.dao.codice:
            self.dao.codice = omogeneousCode(section="Articoli", string=self.dao.codice )
        else:
            print " ERRORE BY_PASSATO PER ILARIA :) "
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        findComboboxRowFromId(self.id_aliquota_iva_customcombobox.combobox,
                              self.dao.id_aliquota_iva)
        findComboboxRowFromId(self.id_famiglia_articolo_customcombobox.combobox,
                              self.dao.id_famiglia_articolo)
        findComboboxRowFromId(self.id_categoria_articolo_customcombobox.combobox,
                              self.dao.id_categoria_articolo)
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
        self.url_articolo_entry.set_text(self.dao.url_immagine or '')
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

        if "PromoWear" in Environment.modulesList:
            self.tipoArticoloTagliaColore=False
            #articolo ancora non salvato o articolo senza taglia e colore
            # Articolo in anagrafica già salvato con id_articolo_padre pieno quindi è una variante
            if self.dao.id and self.dao.id_articolo_padre is not None and self.dao.articoloTagliaColore:
                self.memo_wear.set_text("""ARTICOLO VARIANTE""")
                self.frame_promowear.set_sensitive(True)
                # VARIANTE: niente gestione taglie, ma possibilita' di trattare i codici a barre
                self.senza_taglie_colori_radiobutton.set_active(True)
                self.con_taglie_colori_radiobutton.set_active(False)
                self.senza_taglie_colori_radiobutton.set_sensitive(True)
                self.con_taglie_colori_radiobutton.set_sensitive(False)

                # niente possibilita' di variare gruppo taglie, genere, anno e stagione

                findComboboxRowFromId(self.id_gruppo_taglia_customcombobox.combobox, self.dao.id_gruppo_taglia)
                self.id_gruppo_taglia_customcombobox.set_property('visible', False)
                self.denominazione_gruppo_taglia_label.set_markup(
                        '<span weight="bold">%s</span>'
                        % (self.dao.denominazione_gruppo_taglia,))
                self.denominazione_gruppo_taglia_label.set_property('visible', True)
                findComboboxRowFromId(self.id_genere_combobox, self.dao.id_genere)
                self.id_genere_combobox.set_property('visible', False)
                self.denominazione_genere_label.set_markup(
                        '<span weight="bold">%s</span>'
                        % (self.dao.genere,))
                self.denominazione_genere_label.set_property('visible', True)
                findComboboxRowFromId(self.id_stagione_combobox, self.dao.id_stagione)
                self.id_stagione_combobox.set_property('visible', False)
                findComboboxRowFromId(self.id_anno_combobox, self.dao.id_anno)
                self.id_anno_combobox.set_property('visible', False)
                self.denominazione_stagione_anno_label.set_markup(
                        '<span weight="bold">%s - %s</span>'
                        % (self.dao.stagione,self.dao.anno))
                self.denominazione_stagione_anno_label.set_property('visible', True)

                # possibilita' di variare taglia e colore solo nella misura in cui non ci sia già una variante
                articoliTagliaColore = self.dao.articoliTagliaColore
                idTaglie = set(a.id_taglia for a in articoliTagliaColore)
                idTaglie.remove(self.dao.id_taglia)
                fillComboboxTaglie(self.id_taglia_customcombobox.combobox,
                    idGruppoTaglia=self.dao.id_gruppo_taglia,
                    ignore=list(idTaglie))
                findComboboxRowFromId(self.id_taglia_customcombobox.combobox,
                                    self.dao.id_taglia)
                self.id_taglia_customcombobox.set_property('visible', True)
                self.denominazione_taglia_label.set_markup('-')
                self.denominazione_taglia_label.set_property('visible', False)
                idColori = set(a.id_colore for a in articoliTagliaColore)
                idColori.remove(self.dao.id_colore)
                fillComboboxColori(self.id_colore_customcombobox.combobox, ignore=list(idColori))
                findComboboxRowFromId(self.id_colore_customcombobox.combobox, self.dao.id_colore)
                self.id_colore_customcombobox.set_property('visible', True)
                self.denominazione_colore_label.set_markup('-')
                self.denominazione_colore_label.set_property('visible', False)

                #self.id_aliquota_iva_customcombobox.set_sensitive(False)
                #self.id_famiglia_articolo_customcombobox.set_sensitive(False)
                #self.id_categoria_articolo_customcombobox.set_sensitive(False)
                #self.id_unita_base_combobox.set_sensitive(False)
                #self.produttore_entry.set_sensitive(False)

            elif self.dao.id and not self.dao.id_articolo_padre and self.dao.articoloTagliaColore:
                self.tipoArticoloTagliaColore=True
                # Articolo principale in quando id_articolo_padre è vuoto
                # possibilita' di inserire gruppo taglia, genere, anno, stagione
                self.frame_promowear.set_sensitive(True)
                self.senza_taglie_colori_radiobutton.set_active(False)
                self.con_taglie_colori_radiobutton.set_active(True)
                self.senza_taglie_colori_radiobutton.set_sensitive(False)
                self.con_taglie_colori_radiobutton.set_sensitive(True)
                findComboboxRowFromId(self.id_gruppo_taglia_customcombobox.combobox, self.dao.id_gruppo_taglia)
                self.id_gruppo_taglia_customcombobox.set_property('visible', False)
                self.denominazione_gruppo_taglia_label.set_markup('<span weight="bold">%s</span>'
                                                                    % (self.dao.denominazione_gruppo_taglia,))
                self.denominazione_gruppo_taglia_label.set_property('visible', True)

                findComboboxRowFromId(self.id_genere_combobox, self.dao.id_genere)
                #self.id_genere_combobox.set_active(-1)
                self.id_genere_combobox.set_property('visible', True)

                #self.denominazione_genere_label.set_markup('-')
                self.denominazione_genere_label.set_property('visible', False)
                findComboboxRowFromId(self.id_stagione_combobox, self.dao.id_stagione)
                #self.id_stagione_combobox.set_active(-1)
                self.id_stagione_combobox.set_property('visible', True)
                #self.id_anno_combobox.set_active(-1)
                findComboboxRowFromId(self.id_anno_combobox, self.dao.id_anno)
                self.id_anno_combobox.set_property('visible', True)

                self.denominazione_stagione_anno_label.set_markup('-')
                self.denominazione_stagione_anno_label.set_property('visible', False)

                # niente possibilita' di inserire taglia, colore
                self.id_taglia_customcombobox.combobox.set_active(-1)
                self.id_taglia_customcombobox.set_property('visible', False)
                self.denominazione_taglia_label.set_markup('<span weight="bold">-</span>')
                self.denominazione_taglia_label.set_property('visible', True)
                self.id_colore_customcombobox.combobox.set_active(-1)
                self.id_colore_customcombobox.set_property('visible', False)
                self.denominazione_colore_label.set_markup('<span weight="bold">-</span>')
                self.denominazione_colore_label.set_property('visible', True)
                varianti = str(len(self.dao.articoliTagliaColore))
                testo= """ARTICOLO PRINCIPALE CON %s VARIANTI""" %varianti
                self.memo_wear.set_text(testo)

            elif self.dao.articoloTagliaColore is None or self.tipoArticoloTagliaColore==False:
                #self.frame_promowear.set_sensitive(False)
                self.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
                self.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
                self.denominazione_genere_label.set_markup('-')
                self.denominazione_genere_label.set_property('visible', False)
                self.denominazione_gruppo_taglia_label.set_markup('-')
                self.denominazione_gruppo_taglia_label.set_property('visible', False)
                self.denominazione_stagione_anno_label.set_markup('-')
                self.denominazione_stagione_anno_label.set_property('visible', False)
                self.denominazione_colore_label.set_markup('-')
                self.denominazione_colore_label.set_property('visible', False)
                self.denominazione_taglia_label.set_markup('-')
                self.denominazione_taglia_label.set_property('visible', False)
                self.id_anno_combobox.set_active(-1)
                self.id_genere_combobox.set_active(-1)
                self.id_stagione_combobox.set_active(-1)
                print "ARTICOLO SEMPLICE"
                return
            elif self.dao.articoloTagliaColore is None or self.tipoArticoloTagliaColore:
                self.frame_promowear.set_sensitive(True)
                self.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
                self.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
                self.denominazione_genere_label.set_markup('-')
                self.denominazione_genere_label.set_property('visible', False)
                print "ARTICOLO PLUS"
                return

            #else:
                ## articolo principale: gestione codici a barre - taglie - colori
                #self.senza_taglie_colori_radiobutton.set_active(False)
                #self.con_taglie_colori_radiobutton.set_active(True)

                ## niente variazione gruppo taglia
                ## possibilita' di variare anno, stagione e genere
                #findComboboxRowFromId(self.id_gruppo_taglia_customcombobox.combobox, self.dao.id_gruppo_taglia)
                #self.id_gruppo_taglia_customcombobox.set_property('visible', False)
                #self.denominazione_gruppo_taglia_label.set_markup('<span weight="bold">%s</span>'
                                                                    #% (self.dao.denominazione_gruppo_taglia,))
                #findComboboxRowFromId(self.id_genere_combobox, self.dao.id_genere)
                #self.id_genere_combobox.set_property('visible', True)
                #self.denominazione_genere_label.set_markup('-')
                #self.denominazione_genere_label.set_property('visible', False)
                #findComboboxRowFromId(self.id_stagione_combobox, self.dao.id_stagione)
                #self.id_stagione_combobox.set_property('visible', True)
                #findComboboxRowFromId(self.id_anno_combobox, self.dao.id_anno)
                #self.denominazione_stagione_anno_label.set_markup('-')
                #self.denominazione_stagione_anno_label.set_property('visible', False)

                ## niente variazione taglia, colore
                #self.id_taglia_customcombobox.combobox.set_active(-1)
                #self.id_taglia_customcombobox.set_property('visible', False)
                #self.denominazione_taglia_label.set_markup('<span weight="bold">-</span>')
                #self.denominazione_taglia_label.set_property('visible', True)
                #self.id_colore_customcombobox.combobox.set_active(-1)
                #self.id_colore_customcombobox.set_property('visible', False)
                #self.denominazione_colore_label.set_markup('<span weight="bold">-</span>')
                #self.denominazione_colore_label.set_property('visible', True)
        self._loading = False

    def saveDao(self):
        if (self.codice_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.codice_entry,
                            msg='Campo obbligatorio !\n\nCodice')

        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.denominazione_entry,
                            msg='Campo obbligatorio !\n\nDenominazione')

        if findIdFromCombobox(self.id_aliquota_iva_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_aliquota_iva_customcombobox.combobox,
                            msg='Campo obbligatorio !\n\nAliquota IVA')

        if findIdFromCombobox(self.id_famiglia_articolo_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_famiglia_articolo_customcombobox.combobox,
                            msg='Campo obbligatorio !\n\nFamiglia merceologica')

        if findIdFromCombobox(self.id_categoria_articolo_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_categoria_articolo_customcombobox.combobox,
                            msg='Campo obbligatorio !\n\nCategoria articolo')

        if findIdFromCombobox(self.id_unita_base_combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_unita_base_combobox,
                            msg='Campo obbligatorio !\n\nUnita\' base')
        if "PromoWear" in Environment.modulesList and self.tipoArticoloTagliaColore:
            if self.dao is not None:
                articoloTagliaColore = ArticoloTagliaColore(id=self.dao.id).getRecord()
            else:
                articoloTagliaColore = ArticoloTagliaColore().getRecord()
                articoloTagliaColore.id_articolo = self.dao.id

            articoloTagliaColore.id_gruppo_taglia = findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox)
            articoloTagliaColore.id_taglia = findIdFromCombobox(self.id_taglia_customcombobox.combobox)
            articoloTagliaColore.id_colore = findIdFromCombobox(self.id_colore_customcombobox.combobox)
            articoloTagliaColore.id_anno = findIdFromCombobox(self.id_anno_combobox)
            articoloTagliaColore.id_stagione = findIdFromCombobox(self.id_stagione_combobox)
            articoloTagliaColore.id_genere = findIdFromCombobox(self.id_genere_combobox)
            self.dao.articoloTagliaColore = articoloTagliaColore
            articoloTagliaColore = None
        self.dao.codice = self.codice_entry.get_text()
        #if not self._oldDaoRicreato:
            #cod=checkCodiceDuplicato(codice=self.dao.codice, tipo="Articolo")
            #self._oldDaoRicreato=False
            #if not cod:
                #return

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
        try:
            self.dao.lunghezza = float(self.lunghezza_entry.get_text())
        except:
            self.dao.lunghezza = float(0)
        try:
            self.dao.larghezza = float(self.larghezza_entry.get_text())
        except:
            self.dao.larghezza = float(0)
        try:
            self.dao.altezza = float(self.altezza_entry.get_text())
        except:
            self.dao.altezza = float(0)
        try:
            self.dao.volume = float(self.volume_entry.get_text())
        except:
            self.dao.volume = float(0)
        try:
            self.dao.peso_lordo = float(self.peso_lordo_entry.get_text())
        except:
            self.dao.peso_lordo = float(0)
        try:
            self.dao.peso_imballaggio = float(self.peso_imballaggio_entry.get_text())
        except:
            self.dao.peso_imballaggio = float(0)
        try:
            self.dao.quantita_minima = float(self.quantita_minima_entry.get_text() or 0)
        except:
            self.dao.quantita_minima=float(0)
        self.dao.stampa_etichetta = self.stampa_etichetta_checkbutton.get_active()
        self.dao.codice_etichetta = self.codice_etichetta_entry.get_text()
        self.dao.descrizione_etichetta = self.descrizione_etichetta_entry.get_text()
        self.dao.stampa_listino = self.stampa_listino_checkbutton.get_active()
        self.dao.descrizione_listino = self.descrizione_listino_entry.get_text()
        textBuffer = self.note_textview.get_buffer()
        self.dao.note = textBuffer.get_text(textBuffer.get_start_iter(),
                                            textBuffer.get_end_iter())
        self.dao.sospeso = self.sospeso_checkbutton.get_active()
        if self.dao.cancellato == None:
            self.dao.cancellato = False
        if self.dao.aggiornamento_listino_auto == None:
            self.dao.aggiornamento_listino_auto = False
        self.dao.url_immagine = self.url_articolo_entry.get_text()
        self.dao.persist()

        if self._duplicatedDaoId is not None:
            self.duplicaListini()

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

        from promogest.dao.ListinoArticolo import ListinoArticolo
        listini = ListinoArticolo(isList=True).select(idArticolo = self._duplicatedDaoId)
        for listino in listini:
            daoLA = ListinoArticolo().getRecord()
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
            self.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=idFamiglia)
            self.codice_entry.set_text(self.dao.codice)

    def on_senza_taglie_colori_radiobutton_toggled(self, radioButton):
        active = radioButton.get_active()
        self.codici_a_barre_togglebutton.set_sensitive(active)
        self.taglie_colori_togglebutton.set_sensitive(not active)
        if active:
            self.senza_taglie_colori_radiobutton.set_active(True)
            self.frame_promowear.set_sensitive(False)
            self.tipoArticoloTagliaColore=False
        else:
            self.frame_promowear.set_sensitive(True)
            self.tipoArticoloTagliaColore=True

    def on_taglie_colori_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox) is None:
            toggleButton.set_active(False)
            obligatoryField(self.dialogTopLevel, self.id_gruppo_taglia_customcombobox.combobox, 'Specificare il gruppo taglia !')
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

                if self.dao is not None:
                    if self.dao.id_articolo_padre is not None:
                        if findIdFromCombobox(self.id_taglia_customcombobox.combobox) is None:
                            obligatoryField(self.dialogTopLevel,
                                            self.id_taglia_customcombobox.combobox,
                                            msg='Campo obbligatorio !\nTaglia')

                        if findIdFromCombobox(self.id_colore_customcombobox.combobox) is None:
                            obligatoryField(self.dialogTopLevel,
                                            self.id_colore_customcombobox.combobox,
                                            msg='Campo obbligatorio !\nColore')

        if self.dao.id is None or self.dao is None:
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
        articoliTagliaColore = self.dao.articoliTagliaColore
        idTaglie = set(a.id_taglia for a in articoliTagliaColore)
        idTaglie.remove(self.dao.id_taglia)
        on_id_taglia_customcombobox_clicked(widget,
                                            button,
                                            idGruppoTaglia=self.dao.id_gruppo_taglia,
                                            ignore=list(idTaglie))


    def on_id_colore_customcombobox_clicked(self, widget, button):
        articoliTagliaColore = self.dao.articoliTagliaColore
        idColori = set(a.id_colore for a in articoliTagliaColore)
        idColori.remove(self.dao.id_colore)
        on_id_colore_customcombobox_clicked(widget,
                                            button,
                                            ignore=list(idColori))

