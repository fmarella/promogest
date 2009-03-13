# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from promogest import Environment
from promogest.ui.utils import *



def setLabels(ui):
    return

def setTreeview(treeview, rendererSx):
    column = gtk.TreeViewColumn('Giorni', rendererSx, text=15)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)