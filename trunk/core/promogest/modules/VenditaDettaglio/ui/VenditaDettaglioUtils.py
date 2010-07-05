# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>
# Author: Francesco Meloni <francescoo@promotux.it>

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
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)


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
