# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
#    Author: Francesco Marella <francesco.marella@gmail.com>
#
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

from promogest import Environment
from promogest.ui.gtk_compat import *


def fillComboboxDistintaBase(combobox, search_string=None):
    """
    Riempie la combobox di selezione delle associazioni di articoli.
    Se la lista risultante ha un solo elemento, questo viene automaticamente selezionato.
    """
    model = gtk.ListStore(object,str,str,str)
    model.clear()
    liss = promogest.dao.DistintaBase.select(Environment.connection, nodo=True, codice=search_string,
                                                                                                offset=None, batchSize=None, immediate=True)
    # questa combobox mi sa che non può andare a finire in un filter widget
    emptyRow = ''
    model.append((None, None, None, emptyRow))
    for l in liss:
        model.append((l, l.id_articolo,l.codice, l.denominazione))
    
    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 3)
    combobox.set_model(model)
    if len(liss) == 1 and search_string is not None:
        combobox.set_active(1)
    return
