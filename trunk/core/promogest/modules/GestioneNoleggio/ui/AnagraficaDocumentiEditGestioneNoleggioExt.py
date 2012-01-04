# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from math import sqrt
from promogest import Environment
from promogest.ui.utils import *
from promogest.ui.gtk_compat import *

def setLabels(anaedit):
    anaedit.prezzo_aquisto_entry.set_text("0")
    anaedit.coeficente_noleggio_entry.set_text("1")
    anaedit.totale_periodo_label.set_text("0")

def setTreeview(treeview, rendererSx):
    column = gtk.TreeViewColumn('Giorni', rendererSx, text=15)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
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
