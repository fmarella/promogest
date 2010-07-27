# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

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