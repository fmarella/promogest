# -*- coding: utf-8 -*-


"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.ui.PromowearUtils import *

def drawPromoWearPart(anaarti, renderer):

    treeview = anaarti.filter.resultsElement
    renderer = gtk.CellRendererText()


    column = gtk.TreeViewColumn('Gruppo taglia', renderer, text=9, background=1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (GruppoTaglia, GruppoTaglia.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Taglia', renderer, text=10, background=1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (Taglia, Taglia.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Colore', renderer, text=11, background=1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (Colore, Colore.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Anno', renderer, text=12, background=1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (AnnoAbbigliamento,AnnoAbbigliamento.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Stagione', renderer, text=13, background=1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (StagioneAbbigliamento,StagioneAbbigliamento.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Genere', renderer, text=14, background=1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (None, "genere"))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)
    model = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    return model

def drawRicercaSemplicePromoWearPart(anaarti):
    anaarti.filter_promowear.set_property('visible', True)
    fillComboboxGruppiTaglia(anaarti.id_gruppo_taglia_articolo_filter_combobox, True)
    fillComboboxTaglie(anaarti.id_taglia_articolo_filter_combobox, True)
    fillComboboxColori(anaarti.id_colore_articolo_filter_combobox, True)
    fillComboboxAnniAbbigliamento(anaarti.id_anno_articolo_filter_combobox, True)
    fillComboboxStagioniAbbigliamento(anaarti.id_stagione_articolo_filter_combobox, True)
    fillComboboxGeneriAbbigliamento(anaarti.id_genere_articolo_filter_combobox, True)
    if anaarti._idGruppoTaglia is not None:
        findComboboxRowFromId(anaarti.id_gruppo_taglia_articolo_filter_combobox, anaarti._idGruppoTaglia)
    anaarti.id_taglia_articolo_filter_combobox.set_active(0)
    if anaarti._idTaglia is not None:
        findComboboxRowFromId(anaarti.id_taglia_articolo_filter_combobox, anaarti._idTaglia)
    anaarti.id_colore_articolo_filter_combobox.set_active(0)
    if anaarti._idColore is not None:
        findComboboxRowFromId(anaarti.id_colore_articolo_filter_combobox, anaarti._idColore)
    anaarti.id_anno_articolo_filter_combobox.set_active(0)
    anaarti.id_anno_articolo_filter_combobox.set_active(0)
    anno = getattr(Environment.conf.PromoWear,'anno_default', None)
    if anno is not None:
        try:
            idAnno = AnnoAbbigliamento().select(denominazione = anno)[0].id
            findComboboxRowFromId(anaarti.id_anno_articolo_filter_combobox, idAnno)
        except:
            pass
    #gestione stagione abbigliamento con prelievo del dato di default dal configure ( nb da usare l'id)
    anaarti.id_stagione_articolo_filter_combobox.set_active(0)
    stagione = getattr(Environment.conf.PromoWear,'stagione_default', None)
    if stagione is not None:
        findComboboxRowFromId(anaarti.id_stagione_articolo_filter_combobox, int(stagione))
    anaarti.id_genere_articolo_filter_combobox.set_active(0)
    if anaarti._idGenere is not None:
        findComboboxRowFromId(anaarti.id_colore_articolo_filter_combobox, anaarti._idGenere)
    anaarti.taglie_colori_filter_combobox.set_active(0)
    anaarti.id_stato_articolo_filter_combobox.set_active(0)