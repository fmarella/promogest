# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from promogest.ui.utils import *
from SuMisura import CalcolaArea, CalcolaPerimetro


def setLabels(ui):
    ui.altezza_entry.set_text('')
    ui.larghezza_entry.set_text('')
    ui.moltiplicatore_entry.set_text('')


def setTreeview(treeview, rendererSx):
    column = gtk.TreeViewColumn('H', rendererSx, text=5)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('L', rendererSx, text=6)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Pezzi', rendererSx, text=7)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)


def azzeraRiga(anaedit, numero):
    return
    anaedit._righe[numero].update(altezza = '',
                                larghezza = "",
                                molt_pezzi = 0)


def azzeraRigaPartial(anaedit, numero, rigatampone):
    return
    anaedit._righe[numero].update(altezza= rigatampone['altezza'],
                                larghezza = rigatampone['larghezza'],
                                molt_pezzi = rigatampone['molt_pezzi'])


def on_altezza_entry_key_press_eventPart(anaedit, entry, event):
    return
    larghezza = float(anaedit.larghezza_entry.get_text() or 0)
    moltiplicatore = float(anaedit.moltiplicatore_entry.get_text() or 1)
    if larghezza != 0:
        altezza = float(anaedit.altezza_entry.get_text() or 0)
        if altezza != 0:
            if anaedit._righe[0]["unitaBase"] == "Metri Quadri":
                quantita = CalcolaArea(altezza, larghezza)
            elif anaedit._righe[0]["unitaBase"] == "Metri":
                quantita = CalcolaPerimetro(altezza, larghezza)
            else:
                quantita = None
            if quantita is not None:
                da_stamp = float(quantita) * moltiplicatore
                anaedit.quantita_entry.set_text(str(da_stamp))


def on_larghezza_entry_key_press_eventPart(anaedit, entry, event):
    return
    altezza = float(anaedit.altezza_entry.get_text() or 0)
    moltiplicatore = float(anaedit.moltiplicatore_entry.get_text() or 1)
    if altezza != 0:
        larghezza = float(anaedit.larghezza_entry.get_text() or 0)
        if larghezza != 0:
            if anaedit._righe[0]["unitaBase"] == "Metri Quadri":
                quantita = CalcolaArea(altezza, larghezza)

            elif anaedit._righe[0]["unitaBase"] == "Metri":
                quantita = CalcolaPerimetro(altezza, larghezza)
            else:
                quantita = None
            if quantita is not None:
                da_stamp = moltiplicatore * float(quantita)
                anaedit.quantita_entry.set_text(str(da_stamp))