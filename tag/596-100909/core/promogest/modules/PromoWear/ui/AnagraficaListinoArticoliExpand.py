# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

import gtk

def drawPromoWearExpand1(analistiarti):
    treeview = analistiarti._anagrafica.anagrafica_filter_treeview
    rendererSx = gtk.CellRendererText()
    rendererDx = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Gruppo taglia', rendererSx, text=7)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'gruppo_taglia')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Taglia', rendererSx, text=8)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'taglia')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(70)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Colore', rendererSx, text=9)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'colore')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(70)
    treeview.append_column(column)


    column = gtk.TreeViewColumn('Anno', rendererSx, text=10)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'anno')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(50)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Stagione', rendererSx, text=11)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'stagione')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Genere', rendererSx, text=12)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'genere')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(50)
    treeview.append_column(column)
    analistiarti._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str, str)
    
def drawPromoWearExpand2(analistiarti):
    column = analistiarti._anagrafica.anagrafica_filter_treeview.get_column(6)
    column.set_property('visible', False)
    column = analistiarti._anagrafica.anagrafica_filter_treeview.get_column(7)
    column.set_property('visible', False)
    column = analistiarti._anagrafica.anagrafica_filter_treeview.get_column(8)
    column.set_property('visible', False)
    column = analistiarti._anagrafica.anagrafica_filter_treeview.get_column(9)
    column.set_property('visible', False)
    column = analistiarti._anagrafica.anagrafica_filter_treeview.get_column(10)
    column.set_property('visible', False)
    column = analistiarti._anagrafica.anagrafica_filter_treeview.get_column(11)
    column.set_property('visible', False)
