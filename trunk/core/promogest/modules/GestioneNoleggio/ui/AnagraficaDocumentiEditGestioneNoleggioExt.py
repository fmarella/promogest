# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from math import sqrt
from promogest import Environment
from promogest.ui.utils import *

def setLabels(anaedit):
    anaedit.prezzo_aquisto_entry.set_text("0")
    anaedit.coeficente_noleggio_entry.set_text("1")
    anaedit.totale_periodo_label.set_text("0")

def setTreeview(treeview, rendererSx):
    column = gtk.TreeViewColumn('Giorni', rendererSx, text=15)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

def azzeraRiga(anaedit,numero):
    anaedit._righe[numero].update(
                                divisore_noleggio =1,
                                arco_temporale = "NO",
                                prezzo_acquisto = 0,
                                totale_noleggio = 0)


def totaleNoleggio(anagrafica):
    totale = anagrafica._righe[0]["totale"]
    if posso("GN") and anagrafica.noleggio and anagrafica._righe[0]["arco_temporale"] != "NO":
        if str(anagrafica._righe[0]["divisore_noleggio"]).strip() == "1":
            totale = str(mN(float(anagrafica._righe[0]["totale"]) *float(anagrafica._righe[0]["arco_temporale"])))
            anagrafica.totale_periodo_label.set_text(totale)
        else:
            totale = str(mN(float(anagrafica._righe[0]["totale"]) *sqrt(float(anagrafica._righe[0]["arco_temporale"]))))
            anagrafica.totale_periodo_label.set_text(totale)
        anagrafica._righe[0]["totale_periodo"] = anagrafica.totale_periodo_label.get_text()
    return totale
