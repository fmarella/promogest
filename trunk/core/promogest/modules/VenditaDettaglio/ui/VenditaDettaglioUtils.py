# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012
#by Promotux di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *


def fillComboboxPos(combobox, filter=False, noempty=False):
    """  Crea l'elenco dei magazzini  """
    from promogest.modules.VenditaDettaglio.dao.Pos import Pos
    model = gtk.ListStore(object, int, str)
    mags = Pos().select(offset=None,batchSize=None)
    if not noempty:
        if not filter:
            emptyRow = ''
        else:
            emptyRow = '< Tutti >'
        model.append((None, 0, emptyRow))
    for m in mags:
        model.append((m, m.id, (m.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)


def rigaScontrinoDel(id=None):
    """Cancella le righe associate ad un documento"""
    from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
    row = RigaScontrino().select(idTestataScontrino= id,
                                offset = None,
                                batchSize = None,
                                orderBy=RigaScontrino.id_testata_scontrino)
    for r in row:
        r.delete()
    return True


def scontoRigaScontrinoDel(id=None):
    """Cancella le righe associate ad un documento"""
    from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
    row = ScontoRigaScontrino().select(idRigaScontrino= id,
                                        offset = None,
                                        batchSize = None,
                                        orderBy=ScontoRigaScontrino.id_riga_scontrino)
    for r in row:
        r.delete()
    return True
