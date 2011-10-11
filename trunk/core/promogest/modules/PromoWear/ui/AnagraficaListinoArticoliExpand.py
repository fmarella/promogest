# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni <francesco@promotux.it>
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

from promogest.ui.gtk_compat import *

def drawPromoWearExpand1(analistiarti):
    treeview = analistiarti._anagrafica.anagrafica_filter_treeview
    rendererSx = gtk.CellRendererText()
    rendererDx = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Gruppo taglia', rendererSx, text=7)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'gruppo_taglia')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Taglia', rendererSx, text=8)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'taglia')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(70)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Colore', rendererSx, text=9)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'colore')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(70)
    treeview.append_column(column)


    column = gtk.TreeViewColumn('Anno', rendererSx, text=10)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'anno')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(50)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Stagione', rendererSx, text=11)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.connect("clicked", analistiarti._changeOrderBy, 'stagione')
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Genere', rendererSx, text=12)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
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
