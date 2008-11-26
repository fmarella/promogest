# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import gtk
import gobject
from promogest import Environment
from promogest.ui.utils import *

def treeViewExpand(gtkgui, treeview, renderer):
    """ Expand the normal article treeview """
    if "PromoWear" in Environment.modulesList:
        column = gtk.TreeViewColumn('Gruppo taglia', renderer, text=9, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", gtkgui._changeOrderBy, 'denominazione_gruppo_taglia')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Taglia', renderer, text=10, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", gtkgui._changeOrderBy, 'denominazione_taglia')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Colore', renderer, text=11, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", gtkgui._changeOrderBy, 'denominazione_colore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Anno', renderer, text=12, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", gtkgui._changeOrderBy, 'anno')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Stagione', renderer, text=13, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", gtkgui._changeOrderBy, 'stagione')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Genere', renderer, text=14, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", gtkgui._changeOrderBy, 'genere')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)
        gtkgui._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    else:
        gtkgui.gruppo_taglia_filter_label.set_no_show_all(True)
        gtkgui.gruppo_taglia_filter_label.set_property('visible', False)
        gtkgui.id_gruppo_taglia_articolo_filter_combobox.set_property('visible', False)
        gtkgui.id_gruppo_taglia_articolo_filter_combobox.set_no_show_all(True)
        gtkgui.taglia_filter_label.set_no_show_all(True)
        gtkgui.taglia_filter_label.set_property('visible', False)
        gtkgui.id_taglia_articolo_filter_combobox.set_property('visible', False)
        gtkgui.id_taglia_articolo_filter_combobox.set_no_show_all(True)
        gtkgui.colore_filter_label.set_no_show_all(True)
        gtkgui.colore_filter_label.set_property('visible', False)
        gtkgui.id_colore_articolo_filter_combobox.set_property('visible', False)
        gtkgui.id_colore_articolo_filter_combobox.set_no_show_all(True)
        gtkgui.anno_filter_label.set_no_show_all(True)
        gtkgui.anno_filter_label.set_property('visible', False)
        gtkgui.id_anno_articolo_filter_combobox.set_property('visible', False)
        gtkgui.id_anno_articolo_filter_combobox.set_no_show_all(True)
        gtkgui.stagione_filter_label.set_no_show_all(True)
        gtkgui.stagione_filter_label.set_property('visible', False)
        gtkgui.id_stagione_articolo_filter_combobox.set_property('visible', False)
        gtkgui.id_stagione_articolo_filter_combobox.set_no_show_all(True)
        gtkgui.genere_filter_label.set_no_show_all(True)
        gtkgui.genere_filter_label.set_property('visible', False)
        gtkgui.id_genere_articolo_filter_combobox.set_property('visible', False)
        gtkgui.id_genere_articolo_filter_combobox.set_no_show_all(True)
        gtkgui.taglie_colori_filter_label.set_no_show_all(True)
        gtkgui.taglie_colori_filter_label.set_property('visible', False)
        gtkgui.taglie_colori_filter_combobox.set_property('visible', False)
        gtkgui.taglie_colori_filter_combobox.set_no_show_all(True)


def articleTypeGuiManage(anagrafica, dao):
    """ complex manage the new aticles type: plus, father son """
    gtkgui = anagrafica
    if articleType(dao) == "son":
        gtkgui.memo_wear.set_text("""ARTICOLO VARIANTE""")
        gtkgui.frame_promowear.set_sensitive(True)
        # VARIANTE: niente gestione taglie, ma possibilita' di trattare i codici a barre
        gtkgui.senza_taglie_colori_radiobutton.set_active(True)
        gtkgui.con_taglie_colori_radiobutton.set_active(False)
        gtkgui.senza_taglie_colori_radiobutton.set_sensitive(True)
        gtkgui.con_taglie_colori_radiobutton.set_sensitive(False)

        # niente possibilita' di variare gruppo taglie, genere, anno e stagione

        findComboboxRowFromId(gtkgui.id_gruppo_taglia_customcombobox.combobox, gtkgui.dao.id_gruppo_taglia)
        gtkgui.id_gruppo_taglia_customcombobox.set_property('visible', False)
        gtkgui.denominazione_gruppo_taglia_label.set_markup(
                '<span weight="bold">%s</span>'
                % (dao.denominazione_gruppo_taglia,))
        gtkgui.denominazione_gruppo_taglia_label.set_property('visible', True)
        findComboboxRowFromId(gtkgui.id_genere_combobox, dao.id_genere)
        gtkgui.id_genere_combobox.set_property('visible', False)
        gtkgui.denominazione_genere_label.set_markup(
                '<span weight="bold">%s</span>'
                % (dao.genere,))
        gtkgui.denominazione_genere_label.set_property('visible', True)
        findComboboxRowFromId(gtkgui.id_stagione_combobox, dao.id_stagione)
        gtkgui.id_stagione_combobox.set_property('visible', False)
        findComboboxRowFromId(gtkgui.id_anno_combobox, dao.id_anno)
        gtkgui.id_anno_combobox.set_property('visible', False)
        gtkgui.denominazione_stagione_anno_label.set_markup(
                '<span weight="bold">%s - %s</span>'
                % (dao.stagione,dao.anno))
        gtkgui.denominazione_stagione_anno_label.set_property('visible', True)

        # possibilita' di variare taglia e colore solo nella misura in cui non ci sia già una variante
        articoliTagliaColore = dao.articoliTagliaColore
        idTaglie = set(a.id_taglia for a in articoliTagliaColore)
        idTaglie.remove(dao.id_taglia)
        fillComboboxTaglie(gtkgui.id_taglia_customcombobox.combobox,
            idGruppoTaglia=dao.id_gruppo_taglia,
            ignore=list(idTaglie))
        findComboboxRowFromId(gtkgui.id_taglia_customcombobox.combobox,
                            dao.id_taglia)
        gtkgui.id_taglia_customcombobox.set_property('visible', True)
        gtkgui.denominazione_taglia_label.set_markup('-')
        gtkgui.denominazione_taglia_label.set_property('visible', False)
        idColori = set(a.id_colore for a in articoliTagliaColore)
        idColori.remove(dao.id_colore)
        fillComboboxColori(gtkgui.id_colore_customcombobox.combobox, ignore=list(idColori))
        findComboboxRowFromId(gtkgui.id_colore_customcombobox.combobox, dao.id_colore)
        gtkgui.id_colore_customcombobox.set_property('visible', True)
        gtkgui.denominazione_colore_label.set_markup('-')
        gtkgui.denominazione_colore_label.set_property('visible', False)

        #gtkgui.id_aliquota_iva_customcombobox.set_sensitive(False)
        #gtkgui.id_famiglia_articolo_customcombobox.set_sensitive(False)
        #gtkgui.id_categoria_articolo_customcombobox.set_sensitive(False)
        #gtkgui.id_unita_base_combobox.set_sensitive(False)
        #gtkgui.produttore_entry.set_sensitive(False)

    elif articleType(dao) == "father":
        gtkgui.tipoArticoloTagliaColore=True
        # Articolo principale in quando id_articolo_padre è vuoto
        # possibilita' di inserire gruppo taglia, genere, anno, stagione
        gtkgui.frame_promowear.set_sensitive(True)
        gtkgui.senza_taglie_colori_radiobutton.set_active(False)
        gtkgui.con_taglie_colori_radiobutton.set_active(True)
        gtkgui.senza_taglie_colori_radiobutton.set_sensitive(False)
        gtkgui.con_taglie_colori_radiobutton.set_sensitive(True)
        findComboboxRowFromId(gtkgui.id_gruppo_taglia_customcombobox.combobox, dao.id_gruppo_taglia)
        gtkgui.id_gruppo_taglia_customcombobox.set_property('visible', False)
        gtkgui.denominazione_gruppo_taglia_label.set_markup('<span weight="bold">%s</span>'
                                                            % (dao.denominazione_gruppo_taglia,))
        gtkgui.denominazione_gruppo_taglia_label.set_property('visible', True)

        findComboboxRowFromId(gtkgui.id_genere_combobox, dao.id_genere)
        #gtkgui.id_genere_combobox.set_active(-1)
        gtkgui.id_genere_combobox.set_property('visible', True)

        #gtkgui.denominazione_genere_label.set_markup('-')
        gtkgui.denominazione_genere_label.set_property('visible', False)
        findComboboxRowFromId(gtkgui.id_stagione_combobox, dao.id_stagione)
        #gtkgui.id_stagione_combobox.set_active(-1)
        gtkgui.id_stagione_combobox.set_property('visible', True)
        #gtkgui.id_anno_combobox.set_active(-1)
        findComboboxRowFromId(gtkgui.id_anno_combobox, dao.id_anno)
        gtkgui.id_anno_combobox.set_property('visible', True)

        gtkgui.denominazione_stagione_anno_label.set_markup('-')
        gtkgui.denominazione_stagione_anno_label.set_property('visible', False)

        # niente possibilita' di inserire taglia, colore
        gtkgui.id_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.id_taglia_customcombobox.set_property('visible', False)
        gtkgui.denominazione_taglia_label.set_markup('<span weight="bold">-</span>')
        gtkgui.denominazione_taglia_label.set_property('visible', True)
        gtkgui.id_colore_customcombobox.combobox.set_active(-1)
        gtkgui.id_colore_customcombobox.set_property('visible', False)
        gtkgui.denominazione_colore_label.set_markup('<span weight="bold">-</span>')
        gtkgui.denominazione_colore_label.set_property('visible', True)
        varianti = str(len(dao.articoliTagliaColore))
        testo= """ARTICOLO PRINCIPALE CON %s VARIANTI""" %varianti
        gtkgui.memo_wear.set_text(testo)

    elif articleType(dao) == "normal":
        #gtkgui.frame_promowear.set_sensitive(False)
        gtkgui.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.denominazione_genere_label.set_markup('-')
        gtkgui.denominazione_genere_label.set_property('visible', False)
        gtkgui.denominazione_gruppo_taglia_label.set_markup('-')
        gtkgui.denominazione_gruppo_taglia_label.set_property('visible', False)
        gtkgui.denominazione_stagione_anno_label.set_markup('-')
        gtkgui.denominazione_stagione_anno_label.set_property('visible', False)
        gtkgui.denominazione_colore_label.set_markup('-')
        gtkgui.denominazione_colore_label.set_property('visible', False)
        gtkgui.denominazione_taglia_label.set_markup('-')
        gtkgui.denominazione_taglia_label.set_property('visible', False)
        gtkgui.id_anno_combobox.set_active(-1)
        gtkgui.id_genere_combobox.set_active(-1)
        gtkgui.id_stagione_combobox.set_active(-1)
        print "ARTICOLO SEMPLICE"
        return
    elif articleType(dao) == "plus":
        gtkgui.frame_promowear.set_sensitive(True)
        gtkgui.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.denominazione_genere_label.set_markup('-')
        gtkgui.denominazione_genere_label.set_property('visible', False)
        print "ARTICOLO PLUS"
        return
    elif articleType(dao) == "new":
        gtkgui.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.denominazione_genere_label.set_markup('-')
        gtkgui.denominazione_genere_label.set_property('visible', False)
        gtkgui.denominazione_gruppo_taglia_label.set_markup('-')
        gtkgui.denominazione_gruppo_taglia_label.set_property('visible', False)
        gtkgui.denominazione_stagione_anno_label.set_markup('-')
        gtkgui.denominazione_stagione_anno_label.set_property('visible', False)
        gtkgui.denominazione_colore_label.set_markup('-')
        gtkgui.denominazione_colore_label.set_property('visible', False)
        gtkgui.denominazione_taglia_label.set_markup('-')
        gtkgui.denominazione_taglia_label.set_property('visible', False)
        gtkgui.id_anno_combobox.set_active(-1)
        gtkgui.id_genere_combobox.set_active(-1)
        gtkgui.id_stagione_combobox.set_active(-1)
        print "ARTICOLO NEW"
        return

    #else:
        ## articolo principale: gestione codici a barre - taglie - colori
        #gtkgui.senza_taglie_colori_radiobutton.set_active(False)
        #gtkgui.con_taglie_colori_radiobutton.set_active(True)

        ## niente variazione gruppo taglia
        ## possibilita' di variare anno, stagione e genere
        #findComboboxRowFromId(gtkgui.id_gruppo_taglia_customcombobox.combobox, dao.id_gruppo_taglia)
        #gtkgui.id_gruppo_taglia_customcombobox.set_property('visible', False)
        #gtkgui.denominazione_gruppo_taglia_label.set_markup('<span weight="bold">%s</span>'
                                                            #% (dao.denominazione_gruppo_taglia,))
        #findComboboxRowFromId(gtkgui.id_genere_combobox, dao.id_genere)
        #gtkgui.id_genere_combobox.set_property('visible', True)
        #gtkgui.denominazione_genere_label.set_markup('-')
        #gtkgui.denominazione_genere_label.set_property('visible', False)
        #findComboboxRowFromId(gtkgui.id_stagione_combobox, dao.id_stagione)
        #gtkgui.id_stagione_combobox.set_property('visible', True)
        #findComboboxRowFromId(gtkgui.id_anno_combobox, dao.id_anno)
        #gtkgui.denominazione_stagione_anno_label.set_markup('-')
        #gtkgui.denominazione_stagione_anno_label.set_property('visible', False)

        ## niente variazione taglia, colore
        #gtkgui.id_taglia_customcombobox.combobox.set_active(-1)
        #gtkgui.id_taglia_customcombobox.set_property('visible', False)
        #gtkgui.denominazione_taglia_label.set_markup('<span weight="bold">-</span>')
        #gtkgui.denominazione_taglia_label.set_property('visible', True)
        #gtkgui.id_colore_customcombobox.combobox.set_active(-1)
        #gtkgui.id_colore_customcombobox.set_property('visible', False)
        #gtkgui.denominazione_colore_label.set_markup('<span weight="bold">-</span>')
        #gtkgui.denominazione_colore_label.set_property('visible', True)
