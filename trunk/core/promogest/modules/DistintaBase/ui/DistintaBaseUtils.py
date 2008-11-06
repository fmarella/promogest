# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import gobject, os
import pygtk
pygtk.require('2.0')
import gtk
import time, datetime
from promogest import Environment
import string, re


def fillComboboxDistintaBase(combobox, search_string=None):
    """
    Riempie la combobox di selezione delle associazioni di articoli.
    Se la lista risultante ha un solo elemento, questo viene automaticamente selezionato.
    """
    model = gtk.ListStore(gobject.TYPE_PYOBJECT,str,str,str)
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
