# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.modules.VenditaDettaglio.dao.ScontoScontrino import ScontoScontrino
from promogest.modules.VenditaDettaglio.ui.VenditaDettaglioUtils import scontoRigaScontrinoDel


class ScontoRigaScontrino(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':sconto_riga_scontrino.c.id ==v,
        'idRigaScontrino':sconto_riga_scontrino.c.id_riga_scontrino==v,}
        return  dic[k]


sconto_riga_scontrino=Table('sconto_riga_scontrino',
                            params['metadata'],
                            schema = params['schema'],
                            autoload=True)


sconto_scontrino = Table('sconto_scontrino',
                                params['metadata'],
                                schema = params['schema'],
                                autoload=True)

j = join(sconto_scontrino, sconto_riga_scontrino)

std_mapper = mapper(ScontoRigaScontrino,j, properties={
            'id':[sconto_scontrino.c.id, sconto_riga_scontrino.c.id],
            }, order_by=sconto_riga_scontrino.c.id)
